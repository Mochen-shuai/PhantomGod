---
name: s-cache-poisoning
description: Unified Web Cache Poisoning and Cache Deception skill linking hack-skills methodology with AboutSecurity execution resources. Covers cache key manipulation, unkeyed input injection, cache deception, and smuggling-based cache attacks.
---

# Unified Web Cache Poisoning / Cache Deception

## When To Use

Use for web cache poisoning discovery, unkeyed input injection (headers/cookies), cache deception attacks, cache key normalization bypass, and smuggling-chained cache attacks.

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

- `../../security-sources/hack-skills/skills/web-cache-deception/SKILL.md` — SKILL: Web Cache Deception — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/cache-poisoning-smuggling/SKILL.md` — Web 缓存投毒及请求走私攻击方法论

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

When you discover a potential Web Cache Poisoning vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the cache infrastructure: CDN identified (Cloudflare, Fastly, Akamai, CloudFront), origin server, cache key components (method, host, path, query string)
- Classify the attack type: unkeyed header injection (`X-Forwarded-Host`/`X-Forwarded-Scheme`/`X-Original-URL`), unkeyed cookie injection, cache key normalization bypass, cache deception (path confusion), or smuggling-chained
- Identify cache behavior: `X-Cache: HIT/MISS`, `Age`, `CF-Cache-Status`, `Cache-Control` directives — determine which response components are cached and for how long
- Document the decision tree: cache key identification → unkeyed input discovery → injection test → cache hit verification → impact escalation (XSS/redirect to malicious resource)
- State expected success indicator: poisoned response served on cache HIT, persistent across multiple requests from different IPs

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在 HTTP header 中插入非标准值测试缓存行为：
- `X-Forwarded-Host: attacker.com` — 测试 Host 反射
- `X-Forwarded-Scheme: http` — 测试协议降级
- `X-Forwarded-Port: 1337` — 测试端口注入
- `X-Original-URL: /admin` — 测试路径覆盖
- `Accept: text/evil` — 测试 Content-Type 影响

每个 header 单独发送 → 等待缓存 → 不带 header 重新请求 → 检查响应差异。
记入 `{header: [是否被缓存, 是否反射, 防护情况]}`。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **CP001~003**。
> ⛔ 必须验证缓存 HIT（非 MISS），不可仅凭响应差异判 `tested_not_found`。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Cache key oracle**: use `Pragma: x-get-cache-key` (Fastly) or `X-Cache-Key` response header to learn exactly what the cache key includes — the complement is the unkeyed attack surface
  - **Path confusion for cache deception**: `https://target/profile.php/.css` — some caches store as `.css` MIME type, but the origin still returns HTML (the authenticated profile page). Victim visits the cached URL and their sensitive page is served as a static cache HIT to the attacker.
  - **Fat GET attack**: some caches cache GET responses but ignore the body — send a GET with a body containing malicious parameters that the back-end processes, poisoning the cached GET response
  - **Parameter cloaking**: send `?key=value&key=poison` — front-end and back-end disagree on which duplicate wins, allowing cache key (value) to differ from cached content source (poison)

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **XSS via header injection**: `X-Forwarded-Host: "><img src=x onerror=alert(1)>` → target page reflects `X-Forwarded-Host` in JS resource URLs → XSS on cache HIT
  2. **Open redirect via scheme injection**: `X-Forwarded-Scheme: http` → cached HTTPS page redirects to `http://target` → attacker intercepts MITM
  3. **Cache deception via path extension**: `GET /account.php.css HTTP/1.1` → cached as CSS but contains authenticated HTML
- Each entry format: `[Header/Path / Attack Type] <payload>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Cache key hardening bypass**: when `Vary` header limits caching, find headers NOT in `Vary` but still parsed by the origin; use fat GET body (not in cache key) to smuggle state-changing params
  2. **Cache-Control bypass**: when `Cache-Control: private/no-store` prevents caching, find CDN-specific override headers (`Surrogate-Control`, `Edge-Control`), or exploit mismatch between CDN and origin Cache-Control parsing
  3. **WAF header filtering bypass**: when WAF blocks malicious header values, encode payload in less-monitored headers (`X-Amz-Cf-Id`, `CF-Connecting-IP`, `True-Client-IP`), or use header folding to split payload across lines
  4. **Dynamic content caching**: exploit `stale-while-revalidate` or `stale-if-error` directives to prolong poison; use timing attacks to land poison during revalidation window

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ Cache poisoning affects all users for the duration of cache TTL. Test with extreme caution, use `Cache-Control: max-age=0` when possible, and purge poisoned cache entries immediately after verification.
- Only operate in authorized environments.
