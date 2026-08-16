---
name: s-prototype-pollution
description: Unified Prototype Pollution skill linking hack-skills methodology with AboutSecurity execution resources. Covers JS/Node.js client-side and server-side prototype pollution, Python class pollution, and gadget discovery.
---

# Unified Prototype Pollution

## When To Use

Use for JavaScript/Node.js prototype pollution discovery, client-side DOM prototype pollution, server-side prototype pollution to RCE, Python class pollution (Flask/Jinja2), and CTF prototype pollution challenges.

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

- `../../security-sources/hack-skills/skills/prototype-pollution/SKILL.md` — SKILL: Prototype Pollution — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/prototype-pollution-advanced/SKILL.md` — SKILL: Advanced Prototype Pollution — Deep Dive Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/prototype-pollution-exploit/SKILL.md` — JS 原型链污染攻击方法论
- `../../security-sources/AboutSecurity/skills/exploit/web-method/python-prototype-pollution/SKILL.md` — Python 原型链污染（Flask/Jinja2）

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/rce/unix.txt`

## Related AboutSecurity Dictionaries

- No match found.

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Prototype Pollution vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the pollution context: URL query string / JSON body / multipart form / WebSocket message / postMessage handler
- Classify the pollution type: client-side DOM pollution / server-side Node.js pollution / Python class pollution
- Identify the vulnerable operation: `Object.assign()`, `_.merge()` / `_.defaultsDeep()` (lodash), `extend()`, `JSON.parse()` + spread, recursive merge without hasOwnProperty check, or parsed query string assignment (`qs.parse()`)
- Fingerprint the framework/libraries: lodash (`_.merge` / `_.defaultsDeep`), jQuery `$.extend`, Hoek `merge`, custom recursive merge, Express `req.body` handling, Jinja2/Flask template rendering
- Document the decision tree: input parsing identification → recursive merge detection → `__proto__` / `constructor.prototype` access test → property injection verification → gadget discovery → escalation to RCE/XSS
- State expected success indicator: injected property persists on `{}`, template injection triggered, command execution confirmed

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在 JSON/query 参数中插入探测键测试防护：
- `__proto__` — 最直接的 prototype 访问
- `constructor.prototype` — 绕过 `__proto__` 黑名单
- `["__proto__"]` — 数组索引变体
- 嵌套：`{"__proto__": {"polluted": true}}` → 验证 `{}.polluted === true`
- 宽字符：`__proto__` — Unicode 编码绕过

每个元素单独测试，记入 `{符号: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

**禁止**把完整 exploit chain 当 key。**禁止**在 filter_probe 为空时进入 Module 3。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **PROTO001~003**。
> ⛔ 必须执行 `{} === Object.prototype` 污染验证，不可仅凭 parse 错误判 `tested_not_found`。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Property injection confirmation**: create a fresh `{}` after injection and check if `{}.polluted === "yes"` — confirms the global prototype was modified, not just the local object
  - **Gadget chain in Node.js**: prototype pollution with `child_process.fork()` or `child_process.execSync()` via `NODE_OPTIONS` / `--require` / `--eval` injection on `process.env`; universal gadget: `opts.shell` + `opts.env` in `spawn()`
  - **Client-side gadget escalation**: pollution → `innerHTML` bypass → XSS; pollution → `fetch()` parameter tampering → SSRF; pollution → `onerror`/`onload` handler injection → script execution
  - **Python class pollution**: unlike JS `__proto__`, Python uses `__class__.__init__.__globals__` traversal; common in Jinja2 template context where `Flask.secret_key` can be overwritten for session forgery
  - **qs.parse() bypass**: `a[__proto__][polluted]=yes` with `allowPrototypes: false` (default in qs v6+) still passes — `qs.parse()` is a common first step in Express middleware

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Detection payload**: `{"__proto__":{"polluted":"yes"}}` → check `{}.polluted`; `{"constructor":{"prototype":{"polluted":"yes"}}}` → check `{}.polluted`
  2. **Client-side XSS escalation**: `{"__proto__":{"innerHTML":"<img src=x onerror=alert(1)>"}}` (when polluted property is assigned to `.innerHTML`)
  3. **Server-side RCE escalation**: `{"__proto__":{"shell":"/bin/sh","env":{"NODE_OPTIONS":"--require=/tmp/evil.js"}}}` (when `child_process.spawn()` uses polluted options)
- Each entry format: `[Type / Target] <payload>` → expected behavior
- Source payloads from upstream references when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Key filtering bypass**: `constructor.prototype` (instead of `__proto__`), `__pro__` + `__to__` concatenation in two separate merges, Unicode escapes (`__proto__`), dot-path notation (`a.b.c.__proto__`)
  2. **Object.freeze / Object.seal bypass**: pollution before sealing (client-side race condition), `Object.create(null)` bypass via `constructor.prototype` which is always writable
  3. **Input preprocessing bypass**: when JSON keys are sanitized, use nested array indexers `["__proto__"]`, or put pollution in values when the merge function copies values to prototype chain
  4. **Library-specific bypass**: lodash v4.17.11 CVE-2019-10744 (prototype defaults), jQuery < 3.4.0 CVE-2019-11358, handlebars prototype access for template compilation

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
- ⛔ RCE escalation via prototype pollution requires prior reporting before executing commands on the server.
