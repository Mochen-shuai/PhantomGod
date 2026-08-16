---
name: s-recon
description: Unified Reconnaissance skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Reconnaissance

## When To Use

Use for asset discovery, subdomain enumeration, port scanning, fingerprinting and attack surface mapping.

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

- `../../security-sources/hack-skills/skills/recon-and-methodology/SKILL.md` — SKILL: Recon and Methodology — Expert Bug Bounty Playbook
- `../../security-sources/hack-skills/skills/subdomain-takeover/SKILL.md` — SKILL: Subdomain Takeover — Detection & Exploitation Playbook
- `../../security-sources/hack-skills/skills/api-recon-and-docs/SKILL.md` — SKILL: API Recon and Docs — Endpoints, Schemas, and Version Surface
- `../../security-sources/hack-skills/skills/cors-cross-origin-misconfiguration/SKILL.md` — SKILL: CORS Misconfiguration — Credentialed Origins, Reflection, and Trust Boundary Errors
- `../../security-sources/hack-skills/skills/recon-for-sec/SKILL.md` — Recon and Methodology Router

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/lateral/internal-recon/SKILL.md` — 内网信息收集方法论
- `../../security-sources/AboutSecurity/skills/tool/ksubdomain-brute/SKILL.md` — ksubdomain 无状态子域名爆破方法论
- `../../security-sources/AboutSecurity/skills/tool/fingerprintx-probe/SKILL.md` — fingerprintx 服务指纹识别方法论
- `../../security-sources/AboutSecurity/skills/recon/subdomain-deep/SKILL.md` — 深度子域名挖掘方法论
- `../../security-sources/AboutSecurity/skills/recon/recon-full/SKILL.md` — 主动式全流程侦察方法论
- `../../security-sources/AboutSecurity/skills/recon/js-api-extract/SKILL.md` — JavaScript API 端点提取方法论 [Supplementary — primary source for SPA/Webpack JS analysis]

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/port/port.txt`
- `../../security-sources/AboutSecurity/Dic/port/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/port/db2/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/db2/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/ftp/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/ftp/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/port-list.md`
- `../../security-sources/AboutSecurity/Dic/port/rdp/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/rdp/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/svn/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/svn/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/vnc/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/esxi/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/esxi/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/pop3/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/pop3/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/smtp/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/smtp/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/snmp/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/db2/_meta.yaml`

## Related AboutSecurity Docs

- No match found.

## JS Source Acquisition Enhancement

This bridge file supplements the upstream `js-api-extract` Phase 1 (JS File Collection) with additional techniques not covered upstream. Load `references/js-source-acquisition.md` AFTER the upstream Phase 1 methodology.

**Key supplements** (details in reference file):
- **Mini-Program Reverse Engineering**: WeChat `.wxapkg` / Alipay `.apkg` unpacking → JS extraction → API endpoints not exposed in web SPA
- **Async Chunk Discovery**: Webpack runtime chunk analysis, Vite dynamic import discovery, automated chunk enumeration
- **Wayback Machine Enhanced CDX**: Full JS history (all MIME types), differential endpoint analysis (compare old vs. new), time-range priority strategy
- **Backup/Legacy JS Files**: `.bak/.old/.map/.gz` patterns, build tool leftovers, version control leaks in static directories

## References

- See `references/SOURCES.md`.
- JS source acquisition enhancements (mini-program, async chunks, Wayback, backups) → `references/js-source-acquisition.md`

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
