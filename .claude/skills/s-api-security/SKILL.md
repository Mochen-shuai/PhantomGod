---
name: s-api-security
description: Unified API Security skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified API Security

## When To Use

Use for API enumeration, BOLA/BFLA, mass assignment, GraphQL and REST security testing.

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

- `../../security-sources/hack-skills/skills/api-sec/SKILL.md` — API Security Router
- `../../security-sources/hack-skills/skills/graphql-and-hidden-parameters/SKILL.md` — SKILL: GraphQL and Hidden Parameters — Introspection, Batching, and Undocumented Fields
- `../../security-sources/hack-skills/skills/api-recon-and-docs/SKILL.md` — SKILL: API Recon and Docs — Endpoints, Schemas, and Version Surface
- `../../security-sources/hack-skills/skills/api-auth-and-jwt-abuse/SKILL.md` — SKILL: API Auth and JWT Abuse — Token Trust, Header Tricks, and Rate Limits
- `../../security-sources/hack-skills/skills/api-authorization-and-bola/SKILL.md` — SKILL: API Authorization and BOLA — Object Access, Function Access, and Mass Assignment

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/cloud/huawei-pentesting/SKILL.md` — 华为云渗透测试方法论
- `../../security-sources/AboutSecurity/skills/exploit/web-method/api-fuzz/SKILL.md` — API 安全测试方法论
- `../../security-sources/AboutSecurity/skills/exploit/web-method/graphql-methodology/SKILL.md` — GraphQL 攻击方法论
- `../../security-sources/AboutSecurity/skills/recon/js-api-extract/SKILL.md` — JavaScript API 端点提取方法论
- `../../security-sources/AboutSecurity/skills/exploit/auth/mobile-backend/SKILL.md` — 移动 App 后端 API 安全测试方法论

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/api.txt`
- `../../security-sources/AboutSecurity/Dic/web/directory/api.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-lfi.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-rce.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-xss.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-json.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-sqli.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-ssrf.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-login.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-common.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-captcha.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-callback.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-extended.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-redirect.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-register.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-imagesize.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/top100-param-get.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/top100-param-post.txt`
- `../../security-sources/AboutSecurity/Dic/web/api-param/param-findpassword.txt`

## Related AboutSecurity Docs

- No match found.

## Webpack SPA & JS Audit Enhancement

This bridge supplements upstream `js-api-extract` and `api-fuzz` with SPA build-tool identification, JS file triage, and async chunk authorization testing. Load `references/spa-js-audit.md` BEFORE running endpoint extraction.

⛔ **Mandatory**: Grade JS files (A/B/C) BEFORE extraction. Do not blindly process all files.

**Key supplements** (details in reference file):
- **SPA Framework Identification**: Webpack (`webpackJsonp`/`__webpack_require__`/chunk naming), Vite (`type="module"`/`import.meta.env`), Hash-route SPA (`/#/`)
- **JS File Grading System**: Grade A (app/main/config/api/router/utils/backup, >500KB, WayBack historical), Grade B (named route chunks, 50–500KB, axios/fetch references), Grade C (polyfills/vendor/runtime/worker, <2KB — SKIP)
- **Async Chunk Unauthorized Access**: Admin/dashboard/setup chunks are publicly downloadable → endpoint discovery without authentication
- **Triage Automation**: Bash script for automated JS grading

## References

- See `references/SOURCES.md`.
- Webpack SPA identification and JS audit rules → `references/spa-js-audit.md`

## Vulnerability Testing Output Template

When you discover a potential API Security vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the API context: REST endpoint, GraphQL query/mutation, JSON-RPC, gRPC, or WebSocket
- Classify the vulnerability: IDOR (Insecure Direct Object Reference), BOLA (Broken Object Level Authorization), mass assignment, excessive data exposure, or injection via API parameters
- State the endpoint: full URL, method, required headers, parameter structure
- Document the decision tree: endpoint discovered → auth requirement analysis → parameter enumeration → role comparison (User A accessing User B's data) → parameter injection → response analysis
- State expected success indicator: unauthorized data access, privilege escalation, data modification, or information leak

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - IDOR via GUID/UUID: even "unguessable" UUIDs are not authorization — enumerate from other endpoints (public profile → private data via same UUID), check if UUIDs appear in email notifications, logs, or WebSocket messages
  - Mass assignment: add `role:admin`, `isAdmin:true`, `plan:enterprise`, `credit:999999` to POST/PUT body — many ORMs auto-bind request body to model without field allowlisting
  - GraphQL introspection bypass: if `__schema` is blocked, try field suggestion (`{ _typename }`), GET-based introspection, alias-based field discovery, fragment brute-force for type names
  - Parameter discovery: compare mobile app API params vs. web API (often different validation), check API docs for "deprecated" fields (still accepted), test Content-Type switching (JSON vs. XML vs. form-encoded)

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by attack type:
  1. **IDOR enumeration**: sequential/pattern ID iteration (`/api/users/1` → `/api/users/2`), UUID rotation from related endpoints, encoded ID variants (base64, hash)
  2. **Mass assignment fields**: `role:admin`, `isAdmin:true`, `is_superuser:1`, `plan:enterprise`, `balance:999999`, `verified:true`, `email:attacker@evil.com`, `organizations:[99999]`
  3. **Rate limit / auth bypass headers**: `X-Forwarded-For: 127.0.0.1`, `X-Real-IP: 10.0.0.1`, `X-Original-URL: /admin`, `X-Rewrite-URL: /admin`, `Authorization: Bearer null`, `Authorization: Bearer undefined`
- Each entry format: `[Attack Type] <payload>` → expected behavior
- Source payloads from upstream AboutSecurity API dictionaries when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Authorization bypass**: HTTP method switch (GET→POST→PUT→PATCH→OPTIONS), path case variants (`/api/Admin` vs `/api/admin`), path traversal from API path (`/api/users/../admin/users`), double URL encoding
  2. **Rate limiting bypass**: header rotation (`X-Forwarded-For`, `X-Real-IP`), User-Agent rotation, path parameterization (`/api/users/1` → `/api/users/1?random=123`), session token cycling
  3. **Input validation bypass**: type juggling (`"true"` vs `true`, `"0"` vs `0`), nested object injection, array wrapping (`{"id":1}` → `{"id":[1,2,3]}`), JSON comment/padding bypass
  4. **GraphQL-specific**: query depth/nesting bypass (inline fragments), alias overloading for rate limiting, persisted queries abuse, batching for authorization check circumvention

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
