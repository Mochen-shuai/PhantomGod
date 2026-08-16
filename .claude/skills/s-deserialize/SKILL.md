---
name: s-deserialize
description: Unified Deserialization Attack skill linking hack-skills methodology with AboutSecurity execution resources. Covers PHP/Java/Python/.NET deserialization, POP chains, ysoserial gadgets, and blind exploitation.
---

# Unified Deserialization Attacks

## When To Use

Use for PHP/Java/Python/.NET deserialization discovery, gadget chain construction, blind deserialization exploitation, CTF deserialization challenges, and framework-specific deserialization (Fastjson/Jackson/Shiro/Pickle).

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

- `../../security-sources/hack-skills/skills/deserialization-insecure/SKILL.md` — SKILL: Insecure Deserialization — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/deserialization-methodology/SKILL.md` — 反序列化漏洞攻击方法论（PHP/Python/.NET）
- `../../security-sources/AboutSecurity/skills/exploit/web-method/java-deserialization-methodology/SKILL.md` — Java 反序列化漏洞方法论（ysoserial/Fastjson/Jackson/JNDI）
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-serialization-audit/SKILL.md` — PHP 反序列化源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-serialization-audit/SKILL.md` — Java 反序列化源码审计

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/rce/unix.txt`
- `../../security-sources/AboutSecurity/Payload/rce/_meta.yaml`

## Related AboutSecurity Dictionaries

- No match found.

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Deserialization vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the deserialization context: HTTP parameter (GET/POST/Cookie/Header), serialized session data, JWT claims, pickled cookies, Base64-encoded body
- Classify the deserialization type: PHP `unserialize()` / Java `ObjectInputStream` / .NET `BinaryFormatter` / Python `pickle.loads()` / Node.js `node-serialize` / YAML `yaml.load()`
- Identify the framework: PHP (Laravel/Symfony/WordPress), Java (Spring/WebLogic/Tomcat/JBoss), Python (Flask/Django), Node.js (Express)
- Fingerprint evidence: error messages revealing class names, `java.io.ObjectInputStream` stack traces, `__PHP_Incomplete_Class`, `pickle` error messages
- Document the decision tree: serialized data identification → format fingerprinting → encoding detection (Base64/Hex/Gzip) → gadget chain discovery → payload generation → delivery method
- State expected success indicator: RCE confirmation (DNS callback/time delay), file read, SSRF callback

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在序列化数据中插入探测标记测试防护：
- 格式标记：`O:` `a:` (PHP), `ac ed 00 05` (Java magic bytes), `rO0` (Base64 Java), `gASV` (pickle)
- 修改探测：篡改Base64/Hex编码中的单个字符 → 观察是否报错（反序列化是否发生）
- 类名注入：在预期类名位置插入 `java.lang.Runtime` `com.sun.org.apache.xalan` `python.os.system`
- 空payload：替换为合法但空的序列化对象 → 观察行为差异

每个元素单独测试，记入结构化 `filter_probe`：`{符号/操作: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

**禁止**把完整 gadget chain 当 key。**禁止**在 filter_probe 为空时进入 Module 3。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **DESER001~003**。
> `tested_not_found` / `doubtful` / `filtered` 时**必须逐条应答** checkpoint_response。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Blind deserialization detection**: modify serialized bytes and observe error type changes — different error classes confirm deserialization occurred vs. rejected before deserialization. Use `java.net.URL` with DNS callback for blind RCE verification.
  - **Gadget chain discovery by classpath mapping**: list all jars/libs on classpath → cross-reference with known gadget chains rather than blindly trying ysoserial payloads
  - **PHP Phar deserialization**: `phar://` stream wrapper triggers deserialization on any file operation (`file_get_contents`, `include`, `file_exists`) — not just `unserialize()` calls
  - **Python pickle RCE**: `__reduce__` method in pickle opcodes — many frameworks accept pickle from cookies/sessions; use `pickle.dumps(Payload())` or `pickora` for standalone generation

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Detection payload** (confirm deserialization): PHP `O:8:"stdClass":0:{}` base64 variant, Java `rO0ABX...` (empty ArrayList), Python `gASVAAAAAAAA...` (empty dict)
  2. **RCE payload** (gadget chain): PHP (Monolog/Guzzle/RubyGems chain), Java (CommonsCollections 1-7 / CommonsBeanutils / Spring), .NET (TextFormattingRunProperties/DataSet), Python (`pickle.__reduce__` + `os.system`)
  3. **Exfiltration payload** (blind): DNS callback via `java.net.URL` gadget, SSRF via `java.net.URLConnection`, file read descriptor
- Each entry format: `[Language/Framework / Chain Name] <payload generation command>` → expected behavior
- Source payloads from upstream AboutSecurity deserialization references when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Input validation bypass**: Base64 nested encoding, Gzip compression to hide magic bytes, string concatenation in serialized formats, encoding the payload into multiple layers
  2. **Deny-list bypass**: when specific classes are blocked, use equivalent gadgets from different libraries (CommonsCollections 4 vs 7 vs CommonsBeanutils vs Spring), unconventional entry points (JNDI, JMS, JMX)
  3. **WAF/IDS bypass**: split payload across multiple parameters, use binary protocols (Hessian, Kryo) with different signatures, fragment and reassemble via header injection
  4. **Sandbox/Runtime bypass**: `@Dependent` annotations in Java, `__wakeup()` bypass in PHP (`CVE-2016-7124` with modified property count), `__reduce_ex__` in Python for pickle protocol 2+

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
- ⛔ RCE verification: prefer DNS/time-delay callbacks. Writing files or executing shell commands requires prior reporting.
- ⛔ Do NOT read sensitive data with deserialization gadgets unless in an authorized CTF/sandbox.
