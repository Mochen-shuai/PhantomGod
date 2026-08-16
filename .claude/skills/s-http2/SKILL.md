---
name: s-http2
description: Unified HTTP/2 Attack Surface skill linking hack-skills methodology with AboutSecurity execution resources. Covers HTTP/2-specific attacks, HPACK bomb, stream multiplexing abuse, server push exploitation, and HTTP/2 downgrade smuggling.
---

# Unified HTTP/2 Attack Surface

## When To Use

Use for HTTP/2-specific vulnerability assessment, stream multiplexing abuse, HPACK header compression attacks, HTTP/2 server push exploitation, H2C upgrade smuggling, and HTTP/2 → HTTP/1.1 downgrade attacks.

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

- `../../security-sources/hack-skills/skills/http2-specific-attacks/SKILL.md` — SKILL: HTTP/2-Specific Attacks — Expert Attack Playbook

## Matched AboutSecurity Skills

- (See also request smuggling for H2C downgrade attacks)
- `../../security-sources/AboutSecurity/skills/exploit/advanced/http-smuggling-advanced/SKILL.md`

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

When you discover an HTTP/2-specific attack surface and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the HTTP/2 context: server identifies as supporting H2 (ALPN `h2`), CDN/proxy layer (Cloudflare, AWS ALB, nginx), origin server HTTP version
- Classify the attack surfaces: stream multiplexing abuse (concurrent streams to bypass rate limiting), HPACK bomb (header compression DoS), server push exploitation, H2C (HTTP/2 Cleartext) upgrade smuggling, HTTP/2 → HTTP/1.1 downgrade header injection, pseudo-header manipulation (`:method`, `:path`, `:authority`, `:scheme`)
- Fingerprint the infrastructure: `curl --http2-prior-knowledge -v`, response headers indicating H2 processing, `:status` pseudo-header behavior
- Document the decision tree: H2 support detection → stream multiplexing test → pseudo-header injection → H2C upgrade smuggling → HPACK DoS test
- State expected success indicator: resource exhaustion, smuggled request to internal endpoints, header injection in downgraded request

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

发送 HTTP/2 特定的探测帧/头部：
- 双 `:authority` pseudo-header — 测试 Host 覆盖
- 双 `:path` pseudo-header — 测试路径覆盖
- `content-length` (lowercase, in H2 headers) + `content-length` (pseudo) — 测试长度混淆
- 超长 header name (HPACK Huffman encoded) — 测试 header 大小限制
- 100 concurrent streams — 测试并发限制

每个单独测试，记入 `{操作: [防护情况, 说明]}`。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **H2001~003**。
> ⛔ 异于 HTTP/1.1 — H2 的许多攻击向量来自协议转换层，必须理解 downgrade 流程。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **H2C smuggling**: `curl --http2-prior-knowledge http://target/` — if the origin accepts H2C directly, you can bypass the front-end's HTTP/1.1 WAF by connecting with H2 directly to the origin (if reachable)
  - **HPACK bomb**: HPACK uses Huffman coding for compression — craft headers with maximum compression ratio (all `A`s → extreme compression) causing the server to allocate massive decompression buffers, leading to memory exhaustion (CVE-2019-9511 "Data Dribble", CVE-2019-9513 "Resource Loop")
  - **Pseudo-header injection at downgrade**: when CDN downgrades H2→HTTP/1.1, pseudo-headers like `:method` `:path` `:authority` are converted to HTTP/1.1 request line. Injecting `\r\n` in a pseudo-header value can inject an entire smuggled HTTP/1.1 request after downgrade
  - **Stream priority abuse**: manipulating stream priority/dependency tree to cause head-of-line blocking on critical resources or starve legitimate streams

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Pseudo-header injection**: `:path: /index.html HTTP/1.1\r\nHost: attacker.com\r\n\r\nGET /admin` — injected into downgraded request
  2. **H2C smuggling**: connect via H2C directly to origin, bypassing front-end WAF entirely, then send malicious HTTP/1.1 request
  3. **HPACK bomb**: single header with 16KB of repeating characters → observe response time/memory (non-destructive probe first)
- Each entry format: `[Attack Type] <payload/command>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **H2 detection evasion**: when target only exposes H2 on specific paths, use `Upgrade: h2c` header on HTTP/1.1 to probe; some servers enable H2 only for specific `:authority` values
  2. **Stream limit bypass**: CDN caps concurrent streams but counts differently from origin — open streams up to CDN limit, then let them idle while opening more directly to origin
  3. **Header size limit bypass**: split large headers across CONTINUATION frames, each within the per-frame limit but cumulative exceeding the max header list size
  4. **WAF bypass via H2**: many WAFs inspect downgraded HTTP/1.1 — use H2 features not present in HTTP/1.1 (trailers as headers, pseudo-header ordering variations) to bypass signature-based detection

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- ⛔ H2C smuggling can cause connection pool poisoning affecting other users — test with extreme caution.
- Only operate in authorized environments.
