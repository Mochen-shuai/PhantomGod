---
name: s-ssrf
description: Unified Server-Side Request Forgery skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Server-Side Request Forgery

## When To Use

Use for SSRF discovery, cloud metadata access checks, URL parser bypasses and callback verification.

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

- `../../security-sources/hack-skills/skills/ssrf-server-side-request-forgery/SKILL.md` — SKILL: Server-Side Request Forgery (SSRF) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/upload-insecure-files/SKILL.md` — SKILL: Upload Insecure Files — Validation Bypass, Storage Abuse, and Processing Chains
- `../../security-sources/hack-skills/skills/open-redirect/SKILL.md` — SKILL: Open Redirect — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/dns-rebinding-attacks/SKILL.md` — SKILL: DNS Rebinding — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/xxe-xml-external-entity/SKILL.md` — SKILL: XML External Entity Injection (XXE) — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/ssrf-methodology/SKILL.md` — SSRF 攻击方法论
- `../../security-sources/AboutSecurity/skills/cloud/cloud-metadata/SKILL.md` — 云元数据利用方法论
- `../../security-sources/AboutSecurity/skills/lateral/oa-system-attack/SKILL.md` — 国产 OA/内网系统漏洞利用
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-injection-audit/SKILL.md` — PHP 注入类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-injection-audit/SKILL.md` — Java 注入类漏洞源码审计

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/ssrf/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/ssrf/payload.txt`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-ssrf.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Server-Side Request Forgery (SSRF) vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: URL parameter, webhook URL, file import, image proxy, PDF generator, or API callback
- Classify the SSRF type: basic (response visible), blind (no response), or semi-blind (error messages only)
- State target internal services: cloud metadata endpoints (169.254.169.254), internal APIs, database connectors, file:// protocol
- Document the decision tree: URL injection point → protocol scheme check → internal address test → cloud metadata → internal service scan
- State expected success indicator: metadata response, internal service banner, DNS callback, HTTP status difference

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在正常URL值中段注入协议/地址测试防护：`file://` `gopher://` `dict://` `127.0.0.1` `169.254.169.254` `@`。每个单独测试。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **SSRF001~003**。
> ⛔ 必须构造内网/云元数据探测 + 至少3种协议混淆。⛔ 无回显不得直接判 `tested_not_found`。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - URL parser confusion: using `@` (userinfo), `#` (fragment), URL-encoded special chars to bypass hostname allowlists
  - DNS rebinding: register domain pointing to 127.0.0.1 → change DNS to internal IP → bypass time-of-check-time-of-use
  - Protocol smuggling: `gopher://` for raw TCP to Redis/MySQL/SMTP, `dict://` for service probing
  - Redirect chaining: external server → 302 → `http://169.254.169.254/` bypasses URL validation that only checks initial host

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by target:
  1. **Cloud metadata** (AWS/Azure/GCP/Alibaba Cloud): `http://169.254.169.254/latest/meta-data/` variants
  2. **Internal service probe**: `http://127.0.0.1:PORT/` / `http://localhost/PATH` common service URLs
  3. **Protocol bypass**: `file:///etc/passwd`, `gopher://127.0.0.1:6379/_*1%0d%0a...` (Redis), `dict://127.0.0.1:3306/` (MySQL banner)
- Each entry format: `[Target Service / Protocol] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/ssrf/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Hostname allowlist bypass**: `http://allowed.com@169.254.169.254/`, `http://169.254.169.254.nip.io/`, IPv6 `http://[::ffff:169.254.169.254]/`, decimal IP `http://2852039166/`
  2. **Protocol restriction bypass**: URL scheme confusion (`file://` → `File://`), redirect chain from http:// to gopher://
  3. **Input validation bypass**: 302 redirect from attacker-controlled server, DNS A record pointing to internal IP, `localhost` → `0.0.0.0` → `[::]` → `0x7f000001`
  4. **Response filtering bypass**: Use DNS exfiltration for blind SSRF, encode response in subdomain query to attacker DNS

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
