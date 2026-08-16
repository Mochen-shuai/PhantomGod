---
name: s-path-traversal
description: Unified Path Traversal and File Inclusion skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Path Traversal and File Inclusion

## When To Use

Use for path traversal, LFI/RFI, arbitrary file read and path normalization bypass.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | AboutSecurity |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

- Use hack-skills for methodology, scenario classification, domain coverage and deeper playbooks.
- Use AboutSecurity for execution constraints, mandatory rules, payload files, dictionaries, tool YAML configs, CTF and K8s fine-grained resources.
- Do not duplicate upstream content here. Load upstream files when needed.

## Recommended Loading Order

### High-Level Analysis

1. Read matched hack-skills files first unless Source Priority says otherwise.
2. Then read matched AboutSecurity files for constraints and execution details.

### Execution

1. Read matched AboutSecurity skill files first.
2. Check related Tools YAML.
3. Check related Payload/Dic/Doc files.
4. Fall back to hack-skills for scenario variants and methodology.

### CTF

1. Prefer AboutSecurity when this topic has matching AboutSecurity skills/resources.
2. Use hack-skills for broader theory or missing coverage.

### Bug Bounty / Authorized Assessment

1. Prefer hack-skills methodology and scenario files.
2. Use AboutSecurity tools/resources for execution support.

## Conflict Resolution

1. Safety and authorization rules always have highest priority.
2. AboutSecurity `NEVER`, `ALWAYS`, `禁止`, `必须`, `⛔` rules override general methodology during execution.
3. hack-skills is preferred for scenario classification, knowledge depth and real-world methodology.
4. AboutSecurity is preferred for tools, payloads, dictionaries, CTF and automated execution constraints.
5. For CTF tasks, prefer AboutSecurity unless this topic is mainly covered by hack-skills.
6. For bug bounty or authorized assessment, prefer hack-skills for strategy and AboutSecurity for resources.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/path-traversal-lfi/SKILL.md` — SKILL: Path Traversal / Local File Inclusion (LFI) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/upload-insecure-files/SKILL.md` — SKILL: Upload Insecure Files — Validation Bypass, Storage Abuse, and Processing Chains
- `../../security-sources/hack-skills/skills/memory-forensics-volatility/SKILL.md` — SKILL: Memory Forensics — Expert Analysis Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/lfi-rfi-methodology/SKILL.md` — 文件包含漏洞方法论 (LFI/RFI)
- `../../security-sources/AboutSecurity/skills/ctf/ctf-flag-hunting/SKILL.md` — CTF Flag 搜索策略
- `../../security-sources/AboutSecurity/skills/dfir/memory-forensics-evasion/SKILL.md` — 内存取证与反内存取证
- `../../security-sources/AboutSecurity/skills/exploit/web-method/webshell-deploy/SKILL.md` — Webshell 部署与利用方法论

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/lfi/traversal.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/log.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/linux.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/lfi/windows.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/java-path.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/linux-path.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/properties.txt`
- `../../security-sources/AboutSecurity/Payload/lfi/java-properties.txt`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/file-backup/db.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/py.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/bak.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/cfm.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/cgi.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/txt.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/misc.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/suffix.txt`
- `../../security-sources/AboutSecurity/Dic/web/directory/redteam-file.txt`
- `../../security-sources/AboutSecurity/Dic/web/service/xxljob/xxl-path.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/db-directory.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/bak-directory.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/cfm-directory.txt`
- `../../security-sources/AboutSecurity/Dic/web/file-backup/cgi-directory.txt`
- `../../security-sources/AboutSecurity/Dic/web/directory/redteam-file-suffix.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-lfi.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Path Traversal or File Inclusion vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: file path parameter, template name, language file include, log file path, or export filename
- Classify the vulnerability: path traversal (read arbitrary files), LFI (include + execute local files), RFI (include + execute remote files)
- State the target files: `/etc/passwd`, `/proc/self/environ`, web app source code, configuration files, log files for poisoning
- Document the decision tree: path parameter identified → traversal depth estimation → encoding variant testing → file read confirmed → escalation to RCE (LFI→log poisoning, /proc/self/environ, PHP wrappers)
- State expected success indicator: file content in response, error message revealing path, code execution confirmed

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

探测穿越序列：`../` `..\` `..%2f` `..%252f` `%2e%2e/` `....//`，中段注入，记 filter_probe。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **PATH001~003**。
> ⛔ 必须以已知文件（/etc/passwd, win.ini）坐实。⛔ 遇过滤至少3种绕过。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - Path normalization bypass: `....//....//` (Windows), `..%252f..%252f` (double URL decode), `..\/..\/` (mixed slash), Unicode `..%c0%af..%c0%af`
  - LFI-to-RCE chains: `/proc/self/environ` via User-Agent, PHP session file poisoning, `/var/log/nginx/access.log` injection, `php://input` wrapper for raw POST body
  - Filter bypass: absolute paths when relative blocked (`/etc/passwd` directly), null byte termination for older PHP (`%00`), path truncation via long paths (4096+ chars)
  - Java/Ruby specific: `WEB-INF/web.xml` → Spring config → DB credentials; `Gemfile` → app dependencies and paths

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by OS/target:
  1. **Linux file read**: `../../../../etc/passwd`, `....//....//....//....//etc/passwd`, `/proc/self/environ` (for LFI-to-RCE)
  2. **Windows file read**: `..\..\..\..\windows\win.ini`, `....\\....\\....\\....\\windows\\win.ini`, `C:\windows\system32\drivers\etc\hosts`
  3. **Application config**: `WEB-INF/web.xml` (Java), `.env` (Laravel), `wp-config.php` (WordPress), `settings.py` (Django), `config/database.yml` (Rails)
  4. **PHP wrappers (escalation)**: `php://filter/convert.base64-encode/resource=index.php`, `php://input` (POST body execution), `expect://id` (if expect module loaded)
- Each entry format: `[Target OS / Framework] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/lfi/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Path filtering bypass**: encoding variants (URL encode, double encode, UTF-8 overlong, Unicode normalization), path truncation, symlink indirection
  2. **Extension appending bypass**: null byte (`%00`), path separator truncation (`?` query, `#` fragment on backend), ZIP/SVN internal file paths
  3. **Allowlist bypass**: path traversal from allowed directory (`/var/www/images/../../../etc/passwd`), symlink within allowed directory pointing to target
  4. **WAF bypass**: multipart encoding, chunked transfer encoding, parameter placement in POST body vs. query string vs. cookie

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
