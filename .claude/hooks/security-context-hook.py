#!/usr/bin/env python3
"""UserPromptSubmit hook for security research scene routing.

v4.0 — LLM intent classification with keyword fallback:
- Default mode (auto): LLM (Haiku) intent classification, fallback to keyword
- CLAUDE_HOOK_MODE=llm|keyword|auto env var to control
- Graceful degradation: any failure passes through original input
- API config read from environment (same as Claude Code settings)
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from functools import lru_cache
from urllib.parse import urlsplit

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HOOK_MODE = os.getenv("CLAUDE_HOOK_MODE", "keyword")

API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
API_BASE = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
LLM_MODEL = os.getenv("ANTHROPIC_DEFAULT_HAIKU_MODEL", "claude-haiku-4-5-20251001")
LLM_TIMEOUT_S = int(os.getenv("CLAUDE_HOOK_LLM_TIMEOUT", "8"))

DEBUG = os.getenv("CLAUDE_HOOK_DEBUG") == "1"
ALLOWED_API_HOSTS = {h.strip().lower() for h in
                     os.getenv("CLAUDE_HOOK_ALLOWED_API_HOSTS", "api.anthropic.com,api.deepseek.com").split(",")
                     if h.strip()}

# ---------------------------------------------------------------------------
# Scene hints (shared by both modes)
# ---------------------------------------------------------------------------

SCENE_HINTS = {
    "ctf": "[security:ctf] 按 CTF 题解流程输出：题型判断、利用思路、验证步骤、必要脚本。",
    "vuln": "[security:vuln] 按漏洞研究流程输出：根因、触发条件、影响、PoC/复现与修复建议。",
    "pentest": "[security:pentest] 按授权测试流程输出：攻击面、验证步骤、结果记录与风险说明。",
    "tool": "[security:tool] 按安全工具开发流程输出：目标、输入输出、模块划分、验证方式。",
    "audit": "[security:audit] 按代码审计流程输出：入口点、危险流、漏洞点、修复建议。",
    "ir": "[security:ir] 按应急响应流程输出：证据保全、时间线、IOC、处置建议。",
    "crypto": "[security:crypto] 按密码学分析流程输出：算法、缺陷、利用条件、验证思路。",
    "reverse": "[security:reverse] 按逆向分析流程输出：关键函数、保护点、行为推断、验证步骤。",
}

AUTO_PENTEST_HINT = (
    "[security:pentest] 按授权测试流程输出：攻击面、验证步骤、结果记录与风险说明。\\n\\n"
    "AUTO-TRIGGER: 用户输入中包含目标域名/URL。自动调用 /pentest-windftsy 启动端到端渗透流水线"
    "（准备→侦察→广度建模→漏洞挖掘→威胁收敛→报告）。不要只做单类测试，走完整五阶段流程。"
)

GENERAL_HINT = "[security:general] 安全研究语境；优先给出技术分析、验证路径与防御视。"

# ---------------------------------------------------------------------------
# LLM classifier
# ---------------------------------------------------------------------------

_CLASSIFY_PROMPT = (
    "判断用户输入是否属于安全研究场景。\n\n"
    "安全研究场景：CTF竞赛、漏洞分析、渗透测试、代码安全审计、"
    "应急响应/取证/溯源、逆向工程、安全工具开发。\n\n"
    "重要：以下情况不是安全研究，应输出 PASS：\n"
    "- 日常开发任务（优化SQL、部署、调试、重构）\n"
    "- \"exploit\" 表示\"利用机会\"而非漏洞利用（如 exploit caching for performance）\n"
    "- \"audit\" 表示\"数据库审计/查询审计\"而非安全审计（如 audit query plan）\n"
    "- \"payload\" 表示\"HTTP载荷/数据载荷\"而非攻击载荷（如 HTTP request payload）\n"
    "- \"challenge\" 表示\"困难任务\"而非 CTF（如 this challenge is difficult）\n\n"
    "如果是安全研究，输出：INJECT <场景>\n"
    "场景：ctf, vuln, pentest, audit, ir, reverse, tool\n"
    "如果不是安全研究，输出：PASS\n\n"
    "用户输入：{prompt}"
)


def _call_llm(prompt_text: str) -> dict | None:
    """Call LLM API for intent classification. Returns {scene, raw} or None."""
    if not API_KEY:
        return None
    endpoint = urlsplit(API_BASE)
    if endpoint.scheme != "https" or (endpoint.hostname or "").lower() not in ALLOWED_API_HOSTS:
        return None

    # 最小化外发：限制长度，并移除常见凭据/JWT；默认 keyword 模式不会外发任何 prompt。
    prompt_text = re.sub(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*\S+", r"\1=[REDACTED]", prompt_text)
    prompt_text = re.sub(r"eyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}",
                         "[REDACTED_JWT]", prompt_text)[:4000]

    body = json.dumps({
        "model": LLM_MODEL,
        "max_tokens": 32,
        "messages": [{"role": "user", "content": _CLASSIFY_PROMPT.format(prompt=prompt_text)}],
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE.rstrip('/')}/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT_S) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw = data["content"][0]["text"].strip().upper()

            m = re.fullmatch(r"INJECT\s+(ctf|vuln|pentest|audit|ir|reverse|tool)", raw)
            if m:
                scene = m.group(1).lower()
                return {"inject": True, "scene": scene, "raw": raw}

            return {"inject": False, "scene": None, "raw": raw}
    except Exception:
        return None


def classify_llm(prompt_text: str) -> dict | None:
    """Returns {hint: str, mode: str, raw: str} or None on failure."""
    result = _call_llm(prompt_text)
    if result is None:
        return None

    if not result["inject"]:
        return None  # not security research

    scene = result.get("scene")
    hint = SCENE_HINTS.get(scene, GENERAL_HINT) if scene else GENERAL_HINT
    if scene == "pentest" and URL_PATTERNS.search(prompt_text):
        hint = AUTO_PENTEST_HINT
    return {"hint": hint, "mode": "llm", "scene": scene, "raw": result["raw"]}


# ---------------------------------------------------------------------------
# Keyword classifier (fallback)
# ---------------------------------------------------------------------------

# 显式目标信号：明确的 http(s) URL，或 目标:/target:/域名:/domain: 标记后跟内容。
# 不再用宽泛的「域名样式」匹配，避免把 SKILL.md / recon-pipeline.py 等架构讨论路径误判成目标。
URL_PATTERNS = re.compile(
    r'https?://[^\s]+'
    r'|(?:目标|target|域名|domain)[：:]\s*\S+'
    r'|测试[：:]\s*https?://',
    re.IGNORECASE
)

SECURITY_PATTERNS = [
    r"\bctf\b", r"\bpwn\b",
    r"\bcve-?\d{4}-\d+\b", r"\bexploit\b", r"\bpoc\b", r"\brce\b",
    r"\bxss\b", r"\bssrf\b", r"\bsqli\b", r"\bdeserialization\b",
    r"sql\s*注入", r"sql\s+injection", r"反序列化", r"漏洞", r"注入", r"复现",
    r"\bpentest\b", r"渗透", r"靶场", r"提权", r"privilege\s*escalation",
    r"域控", r"domain\s*controller",
    r"\baudit\b", r"\bsemgrep\b", r"\bcodeql\b", r"审计", r"白盒", r"静态分析", r"源码审计",
    r"\bforensic\b", r"\bmalware\b", r"\bioc\b",
    r"应急", r"取证", r"溯源", r"木马", r"后门", r"\bbackdoor\b", r"恶意样本",
    r"\bghidra\b", r"\bida\b", r"反汇编",
    r"\bpayload\b", r"\bscanner\b", r"\bfuzzer\b", r"逆向",
    r"密钥",
    r"挖洞", r"挖漏洞", r"漏洞挖掘", r"SRC", r"src", r"赏金", r"漏洞赏金",
    r"补天", r"教育SRC", r"eduSRC",
    r"授权测试", r"授权评估",
    r"子域名", r"信息搜集", r"信息收集", r"资产", r"侦察",
    r"越权", r"IDOR", r"idor",
    r"弱口令", r"爆破", r"暴力破解",
    r"文件上传", r"文件包含", r"文件读取",
    r"CSRF", r"csrf", r"CORS", r"cors",
    r"逻辑漏洞", r"支付漏洞", r"优惠券", r"验证码绕过",
    r"XXE", r"xxe", r"SSRF", r"ssrf",
    r"API", r"api安全", r"接口",
    r"OA", r"oa系统", r"办公系统",
    r"内网", r"横向", r"域渗透",
]

SCENE_PATTERNS = {
    "ctf": [r"\bctf\b", r"\bflag\b", r"\bchallenge\b", r"\bpwn\b", r"\bmisc\b", r"web题", r"逆向", r"解密"],
    "vuln": [r"\bcve-?\d{4}-\d+\b", r"漏洞", r"\bvuln\b", r"\bpoc\b", r"\bexploit\b", r"复现",
            r"\brce\b", r"\bsqli\b", r"\bxss\b", r"\bssrf\b", r"注入", r"挖洞", r"挖漏洞", r"漏洞挖掘",
            r"SRC", r"src", r"赏金", r"漏洞赏金", r"补天", r"教育SRC"],
    "pentest": [r"渗透", r"\bpentest\b", r"靶场", r"红队", r"提权", r"privilege\s*escalation",
                r"后渗透", r"横向", r"域控", r"domain\s*controller", r"\bactive directory\b",
                r"内网", r"域渗透", r"信息搜集", r"信息收集", r"侦察", r"子域名",
                r"授权测试", r"授权评估"],
    "tool": [r"扫描器", r"\bscanner\b", r"\bfuzzer\b", r"自动化", r"\bpayloads?\b", r"生成器", r"安全工具"],
    "audit": [r"审计", r"\baudit\b", r"代码审计", r"白盒", r"静态分析", r"\bsemgrep\b", r"\bcodeql\b",
             r"源码", r"sql\s*注入", r"sql\s+injection"],
    "ir": [r"应急", r"\bincident\b", r"取证", r"\bforensic\b", r"溯源", r"\bioc\b",
          r"恶意样本", r"\bmalware\b", r"木马", r"后门", r"\bbackdoor\b"],
    "crypto": [r"加密", r"\bcrypto\b", r"\brsa\b", r"\baes\b", r"\bdes\b", r"\bhash\b", r"签名", r"密钥"],
    "reverse": [r"逆向", r"\breverse\b", r"反汇编", r"\bghidra\b", r"\bida\b", r"调试", r"二进制", r"\bbinary\b"],
}

SCENE_PRIORITY = ["pentest", "vuln", "audit", "ir", "reverse", "crypto", "ctf", "tool"]


@lru_cache(maxsize=1)
def _compiled_security_patterns():
    return [re.compile(p, re.IGNORECASE) for p in SECURITY_PATTERNS]


@lru_cache(maxsize=1)
def _compiled_scene_patterns():
    return {s: [re.compile(p, re.IGNORECASE) for p in ps] for s, ps in SCENE_PATTERNS.items()}


def classify_keyword(prompt_text: str) -> dict | None:
    """Returns {hint, mode, scene} or None if not security."""
    if not any(p.search(prompt_text) for p in _compiled_security_patterns()):
        return None

    compiled = _compiled_scene_patterns()
    scene = None
    for s in SCENE_PRIORITY:
        if any(p.search(prompt_text) for p in compiled.get(s, [])):
            scene = s
            break

    hint = SCENE_HINTS[scene] if scene else GENERAL_HINT
    # Auto-trigger WindFtsy when URL/domain detected in pentest context
    if scene == "pentest" and URL_PATTERNS.search(prompt_text):
        hint = AUTO_PENTEST_HINT
    return {"hint": hint, "mode": "keyword", "scene": scene}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def classify(prompt_text: str) -> dict | None:
    """Unified classifier. Returns {hint, mode, scene} or None."""
    if HOOK_MODE == "llm":
        result = classify_llm(prompt_text)
        if result:
            return result
        return classify_keyword(prompt_text)  # fallback

    if HOOK_MODE == "keyword":
        return classify_keyword(prompt_text)

    # auto: LLM first, keyword fallback
    if API_KEY:
        result = classify_llm(prompt_text)
        if result is not None:
            return result
    return classify_keyword(prompt_text)


def _write_out(s: str) -> None:
    """Write to stdout as UTF-8 bytes — bypasses Windows console encoding issues."""
    sys.stdout.buffer.write(s.encode("utf-8", errors="replace") + b"\n")
    sys.stdout.buffer.flush()


def main() -> None:
    try:
        raw_bytes = sys.stdin.buffer.read()
        raw = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        raw = ""

    try:
        if not raw.strip():
            _write_out(raw)
            return

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            _write_out(raw)
            return

        prompt = payload if isinstance(payload, str) else payload.get("prompt", "")
        if not isinstance(prompt, str) or not prompt.strip():
            _write_out(raw)
            return

        result = classify(prompt)
        if result is None:
            _write_out(raw)
            return

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": result["hint"],
            }
        }

        if DEBUG:
            output["hookSpecificOutput"]["debug"] = (
                f"mode={result['mode']}, scene={result.get('scene', 'general')}"
            )

        _write_out(json.dumps(output, ensure_ascii=False))

    except Exception:
        if raw:
            _write_out(raw)
        sys.exit(0)


if __name__ == "__main__":
    main()
