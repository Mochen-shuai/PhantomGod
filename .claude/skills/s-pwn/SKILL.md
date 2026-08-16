---
name: s-pwn
description: Unified Binary Exploitation skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Binary Exploitation

## When To Use

Use for binary exploitation, stack/heap exploitation, format string, kernel and sandbox pwn learning.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | hack-skills |
| Ctf | hack-skills |
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

- `../../security-sources/hack-skills/skills/binary-protection-bypass/SKILL.md` — SKILL: Binary Protection Bypass — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/format-string-exploitation/SKILL.md` — SKILL: Format String Exploitation — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/stack-overflow-and-rop/SKILL.md` — SKILL: Stack Overflow & ROP — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/heap-exploitation/SKILL.md` — SKILL: Heap Exploitation — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/deserialization-insecure/SKILL.md` — SKILL: Insecure Deserialization — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/ctf/ctf-pwn/SKILL.md` — CTF 二进制漏洞利用 (Pwn)
- `../../security-sources/AboutSecurity/skills/exploit/binary/binary-exploitation-tools/SKILL.md` — 二进制漏洞利用工具集
- `../../security-sources/AboutSecurity/skills/exploit/binary/binary-exploitation-methodology/SKILL.md` — 二进制漏洞利用基础方法论
- `../../security-sources/AboutSecurity/skills/mobile/ios-exploiting/SKILL.md` — iOS 系统级漏洞利用方法论
- `../../security-sources/AboutSecurity/skills/exploit/auth/cookie-analysis/SKILL.md` — Cookie Analysis & Forgery Methodology

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- No match found.

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
