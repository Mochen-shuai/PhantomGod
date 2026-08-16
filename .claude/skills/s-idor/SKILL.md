---
name: s-idor
description: Unified Insecure Direct Object Reference skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Insecure Direct Object Reference (IDOR)

## When To Use

Use for IDOR/BAC discovery: horizontal privilege escalation, vertical privilege escalation, cross-tenant access, GUID enumeration, mass assignment, HTTP method tampering.

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

- `../../security-sources/hack-skills/skills/authbypass-authentication-flaws/SKILL.md` — SKILL: Authentication Bypass — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/api-auth-and-jwt-abuse/SKILL.md` — SKILL: API Auth and JWT Abuse — Token Trust, Header Tricks, and Rate Limits
- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/SKILL.md` — SKILL: Business Logic Vulnerabilities — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/auth/idor-methodology/SKILL.md` — IDOR/越权攻击方法论

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-idor.txt`

## Vulnerability Testing Output Template

When you discover a potential IDOR vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe target object: user profile, order, invoice, document, message, API resource
- Classify IDOR type: horizontal (same-role cross-user), vertical (lower-role → higher-role), cross-tenant (org A → org B), GUID-based
- Document identifier format: sequential integer, UUID v1/v4, Base64 encoded, hashed, composite key
- State decision tree: identify object ID parameter → create test accounts (A + B) → capture A's request → swap to B's session → replace ID with A's resource → observe access
- Expected success indicator: B can read/modify/delete A's resource, admin-only endpoint accessible by normal user

### Module 0: 会话有效性确认（⛔ 必须先于越权测试）

越权测试前**必须**正向确认会话有效：用该会话访问本角色专属页面，确认返回本人数据。**防会话失效被重定向到登录页冒充"权限拦截"**。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **AUTHZ001~003**。
> ⛔ 遇302必须跟踪跳转。⛔ 越权成立须以读到他人真实数据坐实。⛔ 不能仅凭状态码差异判定。

### Module 2: 关键技巧 (Key Techniques)
- GUID IDOR is NOT safe: find the endpoint that leaks GUIDs (user search, share dialog, email notification) — chain with IDOR for full exploitation
- HTTP method switch: GET `/users/123` returns 403 → try PATCH/PUT/DELETE on same endpoint — different auth checks per method
- JSON body IDOR: `{"user_id": 123}` in POST body not reflected in URL — test by replacing with victim ID in request body
- Export function abuse: export "my data" → returns CSV/PDF with ALL users' data if backend doesn't scope the query
- Mass assignment chaining: PATCH `/api/profile` with `{"role":"admin","verified":true,"plan":"enterprise"}` — hidden fields accepted

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Sequential ID enumeration**: `id=1` → `id=2` → `id=3` — increment/decrement, negative values, `id=0` (often admin)
  2. **UUID manipulation**: swap UUID between A↔B accounts; test `/api/users/me` → change to `/api/users/<victim-uuid>`
  3. **Parameter addition**: add `user_id=<victim>` to a request that doesn't normally have it; add `&admin=true` or `&role=admin`
  4. **HTTP method bypass**: GET `/admin/users` → 403; try POST `/admin/users` → 200; use PATCH/PUT/DELETE on protected resources

### Module 4: 绕过方法 (Bypass Methods)
1. **ID encoding**: Base64-decode the ID → increment → re-encode; hash-based IDs — test multiple hashing algorithms
2. **Access check only on collection, not item**: `/api/orders` shows only user's orders, but `/api/orders/999` shows anyone's
3. **Cache poisoning for IDOR**: if response is cached by CDN without user-scoped cache key → access A's cached response as B
4. **Bulk/batch endpoint**: `/api/users/batch` with `{"ids":[123,456]}` may skip per-item auth checks

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ 越权读取不超过 5 组真实用户数据，严禁批量读取
- ⛔ 发现后仅做概念验证，不下载/保存/传播业务数据
- Only operate in authorized environments.
