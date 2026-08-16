---
name: s-auth
description: Unified Authentication and Authorization skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Authentication and Authorization

## When To Use

Use for authentication bypass, authorization flaws, JWT/OAuth/session security review.

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

- `../../security-sources/hack-skills/skills/jwt-oauth-token-attacks/SKILL.md` — SKILL: JWT and OAuth 2.0 Token Attacks — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/authbypass-authentication-flaws/SKILL.md` — SKILL: Authentication Bypass — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/api-auth-and-jwt-abuse/SKILL.md` — SKILL: API Auth and JWT Abuse — Token Trust, Header Tricks, and Rate Limits
- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/SKILL.md` — SKILL: Business Logic Vulnerabilities — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/auth-sec/SKILL.md` — Authentication and Authorization Router
- `../../security-sources/hack-skills/skills/saml-sso-assertion-attacks/SKILL.md` — SKILL: SAML SSO Assertion Attacks — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/auth/oauth-sso-attack/SKILL.md` — OAuth/SSO 攻击方法论
- `../../security-sources/AboutSecurity/skills/exploit/auth/jwt-attack-methodology/SKILL.md` — JWT 攻击方法论
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-auth-config-audit/SKILL.md` — Java 认证与配置安全源码审计
- `../../security-sources/AboutSecurity/skills/cloud/gcp-workspace-pivot/SKILL.md` — GCP 到 Google Workspace 穿越攻击方法论
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-auth-config-audit/SKILL.md` — PHP 认证配置与逻辑类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/exploit/auth/oauth-sso-attack/SKILL.md` — SSO 攻击（含 SAML）

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/auth/password/sql.txt`
- `../../security-sources/AboutSecurity/Dic/auth/credential-pair.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/auth/username/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/auth/username/user-us.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/cn-email.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/cn-phone.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/user-web.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/user-mail.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/pass-admin.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/wpa/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/auth/password/complex/readme.md`
- `../../security-sources/AboutSecurity/Dic/auth/password/wpa/top62-wpa.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/pinyin/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/auth/password/complex/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/auth/password/password-top10.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/wpa/top447-wpa.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/password-top100.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/wpa/top4800-wpa.txt`
- `../../security-sources/AboutSecurity/Dic/auth/username/pinyin/lastname.txt`

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
