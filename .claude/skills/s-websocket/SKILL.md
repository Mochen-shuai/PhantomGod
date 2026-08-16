---
name: s-websocket
description: Unified WebSocket Security skill linking hack-skills methodology with AboutSecurity execution resources. Covers WebSocket handshake hijacking, Cross-Site WebSocket Hijacking (CSWSH), message tampering, injection via WebSocket frames, and authorization bypass.
---

# Unified WebSocket Security

## When To Use

Use for WebSocket endpoint discovery, handshake security assessment, Cross-Site WebSocket Hijacking (CSWSH), WebSocket message injection, authorization in WebSocket channels, and WebSocket-based smuggling/tunneling.

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

- `../../security-sources/hack-skills/skills/websocket-security/SKILL.md` — SKILL: WebSocket Security — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/websocket-attack/SKILL.md` — WebSocket 安全测试方法论

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- No match found.

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-extended.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a WebSocket endpoint and begin active security testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the WebSocket context: endpoint URL (`wss://` or `ws://`), handshake headers, authentication mechanism (cookie-based, token in query param, custom header, JWT), message format (JSON, msgpack, protobuf, custom binary)
- Classify the attack surfaces: Cross-Site WebSocket Hijacking (CSWSH), missing per-message authentication, injection via WebSocket messages (SQLi/XSS/SSTI on messages processed by server), authorization bypass via message parameter manipulation, WebSocket tunneling
- Fingerprint the framework: Socket.IO (Engine.IO polling upgrade), SignalR, Phoenix Channels, ActionCable, ws (Node.js), Gorilla WebSocket (Go), Django Channels
- Document the decision tree: endpoint discovery → handshake analysis (Origin/Cookie check) → CSWSH test → per-message auth bypass → message injection → server-side processing abuse
- State expected success indicator: unauthorized handshake from attacker origin, message injection confirmed in backend processing, data leakage from other user's channel

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

对 WebSocket 握手和消息层进行探测：
- **Origin 头修改**：`Origin: http://evil.com` / `Origin: null` / 无 Origin 头
- **Cookie 检查**：不带 Cookie 进行握手
- **消息注入**：`{"id":1,"sql":"' OR 1=1--"}` `{"__proto__":{"admin":true}}` `{{7*7}}`
- **通道劫持**：连接到同一 WebSocket URL，发送其他用户的消息格式

每个单独测试，记入 `{操作: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **WS001~003**。
> ⛔ 必须先确认 Origin 检查缺失（CSWSH 的前提），再进入注入测试。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **CSWSH with `Origin: null`**: when the server checks `Origin` loosely (regex or allowlist), sending `Origin: null` (which browsers set for sandboxed iframes, `file://`, and `data://` URLs) may bypass the check — null origin is a valid Same-Origin Policy edge case
  - **Socket.IO `sid` parameter session hijack**: Socket.IO sends `sid` in the query string — if the transport upgrades from polling to WebSocket, the `sid` is exposed in the initial HTTP request and may be logged in proxy/CDN logs
  - **Message-layer authorization bypass**: WebSocket handshake passes auth, but server only validates auth on handshake — subsequent messages to modify/delete another user's resources are trusted because the "channel is authenticated"
  - **WebSocket tunneling**: when WebSocket is used as a proxy/gateway (e.g. `wss://target/connect?url=internal:8080`), the WebSocket endpoint becomes an SSRF vector through the handshake parameter

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **CSWSH PoC**: JavaScript `new WebSocket("wss://target/ws")` from attacker origin → if handshake succeeds without Origin check, attacker can send/receive messages as the victim
  2. **Message injection**: `{"action":"search","query":"' UNION SELECT credit_card FROM users--"}` → SQL injection through WebSocket message handler
  3. **Authorization bypass**: connect to `wss://target/ws` as User A, send `{"action":"read_message","msg_id":"other_users_msg_id"}` → IDOR through WebSocket message parameter
- Each entry format: `[Attack Type] <PoC JavaScript/Message>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Origin check bypass**: use `Origin: null` (sandboxed iframe / data: URI), `Origin: https://target.com.evil.com` (loose suffix matching), `Origin: https://target.com` with embedded null byte
  2. **CSRF token in WebSocket**: when the handshake requires a CSRF token, the token is often sent in the query string or header — extractable via XSS on the parent page, or leaked in `Referer` header
  3. **Message format obfuscation**: when server validates message schema, add extra fields that are ignored; nest the attack payload inside a valid wrapper; send binary frames (msgpack/protobuf) to bypass text-based WAF inspection
  4. **Reconnection abuse**: when the server auto-reconnects dropped WebSocket connections, use race condition between disconnect and reconnect to inject a malicious message as the first in the new connection's queue

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- ⛔ WebSocket connections are persistent — limit test duration and close connections immediately after confirmation.
- Only operate in authorized environments.
