import sys
import json
import re
import unicodedata


def _decision(allow, message=""):
    out = {"allow": allow}
    if message:
        out["message"] = message
    out["hookSpecificOutput"] = {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow" if allow else "deny",
    }
    if message:
        out["hookSpecificOutput"]["permissionDecisionReason"] = message
    sys.stdout.buffer.write((json.dumps(out, ensure_ascii=False) + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()


def _command(tool_input):
    if isinstance(tool_input, dict):
        return str(tool_input.get("command") or tool_input.get("cmd") or "")
    return str(tool_input or "")

def main():
    # 读取 Claude Code 传入的参数
    try:
        input_data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except Exception:
        _decision(False, "🚫 [安全拦截] PreToolUse 输入无法解析，按失败关闭处理。")
        return
    tool_name = input_data.get("tool_name")
    tool_input = input_data.get("tool_input", "")

    # 🚫 禁令清单检查
    forbidden_patterns = [
        (r"(?:^|[;&|]\s*)rm\s+(?:-[^\s]*[rf][^\s]*\s+){1,}", "递归/强制 rm"),
        (r"\b(?:mkfs(?:\.[a-z0-9]+)?|shutdown|reboot|poweroff|halt)\b", "系统破坏/关机命令"),
        (r"\bdd\s+[^\n]*\bof\s*=", "块设备/文件覆写 dd"),
        (r"\bformat(?:\.com)?\s+[a-z]:", "磁盘格式化"),
        (r"\bremove-item\b[^\n]*(?:-recurse|-r\b)[^\n]*(?:-force|-f\b)", "PowerShell 递归强制删除"),
        (r"\b(?:invoke-expression|iex)\b", "动态执行下载/拼接代码"),
        (r"\b(?:irm|invoke-restmethod|iwr|invoke-webrequest|curl)\b[^\n|]*\|\s*(?:iex|invoke-expression|sh|bash|pwsh|powershell)\b",
         "下载内容直接送入解释器"),
    ]
    if tool_name == "Bash":
        command = unicodedata.normalize("NFKC", _command(tool_input)).lower()
        command = command.replace("`\n", "").replace("\\\n", "")
        for pattern, label in forbidden_patterns:
            if re.search(pattern, command, re.I):
                _decision(False, f"🚫 [安全拦截] 检测到高危命令模式：{label}。")
                return

    # ✅ 允许执行
    _decision(True)

if __name__ == "__main__":
    main()
