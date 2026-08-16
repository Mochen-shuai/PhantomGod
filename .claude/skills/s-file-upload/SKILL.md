---
name: s-file-upload
description: Unified File Upload Security skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified File Upload Security

## When To Use

Use for upload validation analysis, extension/content-type bypass, image/polyglot upload checks.

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

- `../../security-sources/hack-skills/skills/upload-insecure-files/SKILL.md` — SKILL: Upload Insecure Files — Validation Bypass, Storage Abuse, and Processing Chains
- `../../security-sources/hack-skills/skills/xxe-xml-external-entity/SKILL.md` — SKILL: XML External Entity Injection (XXE) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/SKILL.md` — SKILL: Business Logic Vulnerabilities — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/ghost-bits-cast-attack/SKILL.md` — SKILL: Ghost Bits / Cast Attack — Java char to byte Narrowing Playbook
- `../../security-sources/hack-skills/skills/reverse-shell-techniques/SKILL.md` — SKILL: Reverse Shell Techniques — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/file-upload-methodology/SKILL.md` — 文件上传漏洞方法论
- `../../security-sources/AboutSecurity/skills/cloud/oss-bucket-exploit/SKILL.md` — 对象存储 Bucket 误配利用方法论
- `../../security-sources/AboutSecurity/skills/cloud/k8s-ingress-nightmare/SKILL.md` — IngressNightmare — CVE-2025-1974
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-file-audit/SKILL.md` — PHP 文件操作类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-file-audit/SKILL.md` — Java 文件操作类漏洞源码审计

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/upload/1.doc`
- `../../security-sources/AboutSecurity/Payload/upload/1.pdf`
- `../../security-sources/AboutSecurity/Payload/upload/1.png`
- `../../security-sources/AboutSecurity/Payload/upload/1.svg`
- `../../security-sources/AboutSecurity/Payload/upload/1.txt`
- `../../security-sources/AboutSecurity/Payload/upload/1.zip`
- `../../security-sources/AboutSecurity/Payload/upload/1.html`
- `../../security-sources/AboutSecurity/Payload/upload/1.xlsx`
- `../../security-sources/AboutSecurity/Payload/upload/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/upload/upload.html`
- `../../security-sources/AboutSecurity/Payload/upload/upload2.html`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/upload/asp.txt`
- `../../security-sources/AboutSecurity/Dic/web/upload/jsp.txt`
- `../../security-sources/AboutSecurity/Dic/web/upload/php.txt`
- `../../security-sources/AboutSecurity/Dic/web/upload/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/web/upload/htaccess.txt`
- `../../security-sources/AboutSecurity/Dic/web/upload/content-type.txt`
- `../../security-sources/AboutSecurity/Dic/web/upload/upload-suffix.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential File Upload vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the upload context: avatar upload, document import, backup restore, plugin/theme upload, or API file attachment
- Classify the vulnerability type: unrestricted file type, extension bypass, content-type bypass, image polyglot, or path traversal in filename
- State the target: RCE via webshell, XSS via SVG/HTML, SSRF via server-side fetch of uploaded file
- Document the decision tree: normal upload → extension fuzzing → content-type mutation → magic byte insertion → filename path traversal → race condition (TOCTOU)
- State expected success indicator: uploaded file accessible at predictable path, code execution confirmed, file content rendered as HTML

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

探测上传校验规则：后缀白/黑名单、Content-Type校验、魔术字节检查、文件大小限制。逐个测试。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **UPLOAD001~002**。
> ⛔ 必须遍历所有可解析后缀 + 大小写/双扩展/截断/多MIME。⛔ 上传成功不解析时联动路径穿越。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - Image polyglot: embed PHP/JSP payload in EXIF metadata or after valid image magic bytes (GIF89a, \xFF\xD8\xFF for JPEG) — bypasses `getimagesize()` and image validation
  - Extension blacklist gaps: `.phtml`, `.pht`, `.php5`, `.shtml`, `.jspx`, `.ashx`, `.asa` — OS/framework-specific extensions often missed
  - Content-Type manipulation: change `Content-Type: application/x-php` to `image/jpeg` — many servers trust client-provided MIME over file content inspection
  - Race condition (TOCTOU): upload → file written → server validates → attacker accesses before deletion — works on temp-file upload patterns

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by attack type:
  1. **Extension bypass**: `.php.jpg`, `.php%00.jpg` (null byte), `.php.` (trailing dot Windows), `.pHp` (case), `.php::$DATA` (NTFS stream)
  2. **Webshell payload** (minimal): `<?php system($_GET['cmd']);?>`, `<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>` (JSP), `<?=exec($_GET[0])?>` (short PHP)
  3. **Non-RCE attack**: SVG XSS (`<svg/onload=alert(1)>`), HTML with CSRF form, server-side XML injection via DOCX/XLSX
- Each entry format: `[Attack Type / Target Tech Stack] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/upload/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Extension validation bypass**: double extension, null byte injection, NTFS alternate data stream, trailing dot/space (Windows), MIME type mismatch
  2. **Content inspection bypass**: image polyglot with payload in EXIF, GIF89a header prefix, SVG with embedded script (valid XML), PDF with /OpenAction
  3. **Server-side processing bypass**: zip/tar with path traversal filenames, symlink upload, .htaccess/.config override to enable code execution
  4. **Access control bypass**: guess upload directory (common paths: `/uploads/`, `/files/`, `/temp/`, `/media/`), predictable filename (timestamp-based, sequential ID)

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
