---
name: s-graphql
description: Unified GraphQL Security skill linking hack-skills methodology with AboutSecurity execution resources. Covers introspection abuse, query batching/aliasing attacks, field-level authorization bypass, GraphQL injection, and DoS via resource-intensive queries.
---

# Unified GraphQL Security

## When To Use

Use for GraphQL endpoint discovery, introspection analysis, field-level authorization testing, query depth/batching abuse, GraphQL injection (NoSQL/SQL via resolvers), and mutation permission bypass.

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

- `../../security-sources/hack-skills/skills/graphql-and-hidden-parameters/SKILL.md` — SKILL: GraphQL and Hidden Parameters — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/graphql-methodology/SKILL.md` — GraphQL 安全测试方法论

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/directory/main.txt`
- `../../security-sources/AboutSecurity/Dic/web/directory/common.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a GraphQL endpoint and begin active security testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the GraphQL context: endpoint path (`/graphql`, `/api/graphql`, `/v1/query`), transport (POST/GET/WebSocket subscription), authentication mechanism
- Classify the attack surfaces: introspection exposure, field suggestion leakage, query depth/cost abuse, batching + alias-based rate-limit bypass, resolver-level injection (SQL/NoSQL/OS command), mutation authorization bypass
- Fingerprint the framework: Apollo Server, Graphene (Python), graphql-js, Hasura, GraphQL Yoga, Hot Chocolate (.NET), Absinthe (Elixir), GraphQL Java (Spring)
- Document the decision tree: endpoint discovery → introspection check → schema analysis → field/auth mapping → targeted injection per field argument → batching/alias abuse → DoS evaluation
- State expected success indicator: sensitive field data exposed, authorization bypass, injection confirmed, or resource exhaustion demonstrated

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在 GraphQL 查询中插入探测操作测试防护：
- `{__schema{types{name}}}` — 完整 introspection 查询
- `{__type(name:"User"){fields{name}}}` — 单类型 introspection
- `query Q1{user(id:1)} query Q2{user(id:2)}` — 批量查询（非 Apollo 批处理）
- `[{"query":"..."},{"query":"..."}]` — Apollo 批量查询数组
- `query{user(id:"' OR '1'='1"){name}}` — 注入探测

每个单独测试，记入 `{操作: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **GQL001~003**。
> ⛔ 不可仅凭 introspection disabled 判安全 — 需继续检测字段建议(field suggestions)、错误消息泄露。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Introspection bypass when disabled**: many frameworks return schema via field suggestions in error messages (`"Cannot query field 'X' on type 'Y'. Did you mean 'Z'?"`) — use this to reconstruct schema even with `introspection: false`; also try `__type(name: "Query")` which is often not blocked
  - **Alias-based rate limit bypass**: `query{a:user(id:1) b:user(id:2) ... z:user(id:26)}` — one HTTP request but 26 resolver calls, bypassing per-request rate limiting. Use this for brute-force (OTP/reset tokens) and enumeration
  - **Circular fragment DoS**: `query { q1: ...F q2: ...F } fragment F on Query { ...F }` — exponential field expansion, one query can trigger millions of resolver invocations
  - **Batching authorization confusion**: Apollo Link batching sends multiple operations in one POST body array; the server may authenticate only the first operation while executing all of them

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Introspection & schema exfiltration**: `{__schema{types{name,fields{name,args{name,type{name}}}}}}` (full schema), `{__schema{ directives{name,args{name}} }}` (custom directives reveal custom auth logic)
  2. **Authorization bypass via alias**: `query{me{id} admin_me:user(id:"admin_id"){email}}` — querying another user's data via direct ID parameter, bypassing the `me` resolver
  3. **Injection via field arguments**: `query{search(term:"' OR 1=1--"){results}}` — SQL injection through search resolver; `query{user(id:"1){name}__typename}` — try `__typename` on every type to map schema without introspection
- Each entry format: `[Attack Type] <query>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Query depth limit bypass**: fragment flattening (decompose deep query into flat fragments), inline fragment arrays, `__typename` chain at arbitrary depth — some depth counters don't count fragments
  2. **Query cost analysis bypass**: use many cheap fields to mask one expensive field, field aliasing to repeat cheap field and hide expensive one, type-hopping via `__typename` and union types
  3. **Persisted query bypass**: when only persisted queries are allowed, try `/graphql?query={...}` (GET), `/graphql?operationName=...` with a known document, or register a new persisted document if the mutation is exposed
  4. **Authorization bypass via interface/union**: `query{node(id:"user:admin"){... on User{email}}}` — global node ID parsing may bypass per-type authorization checks

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- ⛔ GraphQL DoS testing (circular fragments, deeply nested queries) can crash the server — test with low-cost queries first and escalate gradually.
- Only operate in authorized environments.
