---
name: s-request-smuggling
description: Unified HTTP Request Smuggling skill linking hack-skills methodology with AboutSecurity execution resources. Covers CL.TE / TE.CL / TE.TE desync, HTTP/2 downgrade smuggling, and cache poisoning via smuggling.
---

# Unified HTTP Request Smuggling

## When To Use

Use for HTTP request smuggling discovery, front-end/back-end desync detection, CL.TE/TE.CL/TE.TE testing, HTTP/2 downgrade attacks, and smuggling-based cache poisoning/session hijacking.

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

- `../../security-sources/hack-skills/skills/request-smuggling/SKILL.md` — SKILL: HTTP Request Smuggling — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/cache-poisoning-smuggling/SKILL.md` — Web 缓存投毒及请求走私攻击方法论
- `../../security-sources/AboutSecurity/skills/exploit/advanced/http-smuggling-advanced/SKILL.md` — HTTP 请求走私高级利用

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

## Vulnerability Testing Output Template

When you discover a potential HTTP Request Smuggling vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the scanning context: front-end proxy/CDN identified (Cloudflare, AWS ALB, nginx, HAProxy, Envoy), target origin server type, HTTP version support
- Classify the smuggling type: CL.TE (front-end uses Content-Length, back-end uses Transfer-Encoding), TE.CL (reverse), TE.TE (both use Transfer-Encoding, different parsing), HTTP/2 downgrade (H2C smuggling)
- Fingerprint the infrastructure: `Server` header, response header ordering, `Via` header, error page signatures, load balancer cookie patterns
- Document the decision tree: infrastructure fingerprinting → CL.TE probe → TE.CL probe → TE.TE probe → timing technique confirmation → impact escalation
- State expected success indicator: time delay, differential response, poisoned content served to other users, backend request queue desync

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在 HTTP 请求中插入协议歧义探测：
- `Transfer-Encoding: chunked` header（单独，看是否被接受）
- 双 `Content-Length` header（不同值，看哪个生效）
- `Transfer-Encoding` + `Content-Length` 同时存在
- `Transfer-Encoding: identity` vs `Transfer-Encoding: chunked` 同请求
- 空 chunk size `0\r\n\r\n` 探针

每个单独测试，记入 `{操作: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

**禁止**把完整 smuggling payload 当 key。**禁止**在 filter_probe 为空时进入 Module 3。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **SMUG001~004**。
> ⛔ 必须先确认前后端存在差异解析，不可仅凭 400 错误判 `tested_not_found`。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Timing technique for blind detection**: send a request that will queue on the back-end (e.g. smuggled incomplete chunk) immediately followed by a normal request — timing difference > threshold indicates desync
  - **CL.TE differential**: front-end reads `Content-Length: X`, back-end reads `Transfer-Encoding: chunked` — the smuggled bytes in the body become the next request's prefix; use `0\r\n\r\n` chunk terminator to close the smuggled prefix cleanly
  - **HTTP/2 downgrade smuggling**: H2C (HTTP/2 Cleartext) downgrade when front-end HTTP/2 → back-end HTTP/1.1; inject `Host` header override to poison routing, inject `Content-Length: 0` to truncate back-end's view
  - **Response queue poisoning**: rather than attacking other users directly, poison the response queue by smuggling a request whose response gets returned to a different user's connection — enables credential theft

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by type:
  1. **CL.TE probe payload**: `POST / HTTP/1.1\r\nHost: target\r\nContent-Length: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nG` — the `G` prefix causes the next legitimate request to be malformed if desync exists
  2. **TE.CL probe payload**: `POST / HTTP/1.1\r\nHost: target\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n5c\r\nGPOST / HTTP/1.1\r\nHost: target\r\n\r\n0\r\n\r\n` — front-end reads 4 bytes from Content-Length, back-end reads chunked prefix `GPOST...`
  3. **H2C downgrade payload**: `POST / HTTP/1.1\r\nHost: internal-admin\r\nContent-Length: 0\r\n\r\nGET /admin HTTP/1.1\r\nHost: internal-admin\r\n\r\n` — smuggled via HTTP/2 downgrade
- Each entry format: `[CL.TE / TE.CL / H2C] <key header structure>` → expected behavior
- Use Turbo Intruder for race-condition based probes (single-packet attack)

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **WAF blocking TE header**: use `Transfer-encoding: chunked` (lowercase), `Transfer-Encoding: xchunked` (some parsers accept), `Transfer-Encoding:\tchunked` (tab separator), `Transfer-Encoding : chunked` (space before colon)
  2. **Front-end normalization**: when front-end strips duplicate headers, use header folding (obsolete line continuation with space/tab prefix), or embed TE in `TE` + `Transfer-Encoding` combo
  3. **Connection-specific bypass**: HTTP/2 → HTTP/1.1 downgrade through different intermediary chains (CDN→origin vs. WAF→origin), `Via` header manipulation to bypass WAF inspection of smuggled prefix
  4. **Detection avoidance**: use non-blocking detection (timing-only probes), avoid 400-error-emitting payloads, vary smuggled prefix position (start of body vs. mid-chunk), rotate target endpoints

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ Request smuggling testing can poison the connection pool and affect other users — test during low-traffic periods, use dedicated test endpoints when possible, and reset connections after testing.
- ⛔ Only test against authorized targets.
- Avoid unnecessary brute force or destructive testing.
