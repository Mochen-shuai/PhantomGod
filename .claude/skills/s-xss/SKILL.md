---
name: s-xss
description: Unified Cross-Site Scripting skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Cross-Site Scripting

## When To Use

Use for reflected, stored and DOM XSS analysis, payload selection, filter bypass and verification.

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

- `../../security-sources/hack-skills/skills/xss-cross-site-scripting/SKILL.md` — SKILL: Cross-Site Scripting (XSS) — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/crlf-injection/SKILL.md` — SKILL: CRLF Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/csrf-cross-site-request-forgery/SKILL.md` — SKILL: CSRF — Cross-Site Request Forgery — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/cors-cross-origin-misconfiguration/SKILL.md` — SKILL: CORS Misconfiguration — Credentialed Origins, Reflection, and Trust Boundary Errors
- `../../security-sources/hack-skills/skills/websocket-security/SKILL.md` — SKILL: WebSocket Security
- `../../security-sources/hack-skills/skills/csp-bypass-advanced/SKILL.md` — SKILL: CSP Bypass Advanced (DOM Clobbering section)

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/xss-methodology/SKILL.md` — XSS 跨站脚本完整方法论
- `../../security-sources/AboutSecurity/skills/tool/dalfox-xss/SKILL.md` — DalFox XSS 漏洞扫描方法论
- `../../security-sources/AboutSecurity/skills/exploit/auth/csrf-methodology/SKILL.md` — CSRF 跨站请求伪造方法论
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-frontend-audit/SKILL.md` — PHP 前端交互类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-frontend-audit/SKILL.md` — Java 前端安全类漏洞源码审计

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/xss/pdf/1.pdf`
- `../../security-sources/AboutSecurity/Payload/xss/readme.md`
- `../../security-sources/AboutSecurity/Payload/xss/svg/1.svg`
- `../../security-sources/AboutSecurity/Payload/xss/svg/2.svg`
- `../../security-sources/AboutSecurity/Payload/xss/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xss/html/1.html`
- `../../security-sources/AboutSecurity/Payload/xss/xml/xml.txt`
- `../../security-sources/AboutSecurity/Payload/xss/xml/xss.xml`
- `../../security-sources/AboutSecurity/Payload/xss/js-event.txt`
- `../../security-sources/AboutSecurity/Payload/xss/pdf/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xss/svg/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xss/xml/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xss/html/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/xss/js-function.txt`
- `../../security-sources/AboutSecurity/Payload/xss/js-tag-full.txt`
- `../../security-sources/AboutSecurity/Payload/xss/js-tag-half.txt`
- `../../security-sources/AboutSecurity/Payload/xss/xss-payload1.txt`
- `../../security-sources/AboutSecurity/Payload/xss/xss-payload2.txt`
- `../../security-sources/AboutSecurity/Payload/xss/svg/sanitised.svg`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-xss.txt`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential Cross-Site Scripting (XSS) vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: reflected / stored / DOM-based, HTML tag context, attribute context, or JS context
- State the entry point (parameter name, URL path, POST body field)
- Explain WHY this specific payload type was chosen (e.g., "`<img onerror>` chosen because `<script>` is blocked")
- Document the decision tree path: context analysis → encoding behavior → payload selection
- State expected success indicator (alert popup, cookie exfiltration to callback, DOM modification visible)

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

在正常参数值中间插入单一标签/事件/协议测试防护：`<img` `<svg` `<script` `onerror` `onload` `javascript:` `data:`。每个元素单独测试，记入 `filter_probe`。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **XSS001~002**。
> ⛔ 存储型必须到实际渲染页验证执行。⛔ 不因个别标签被拦即判安全。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - Encoding tricks: HTML entity encoding, URL encoding, JS unicode escapes, template literal bypass
  - Parser differentials: browser quirks mode vs. strict mode, innerHTML vs. createElement behavior
  - Framework-specific exploits: Vue `v-html` bypass, React `dangerouslySetInnerHTML` alternatives, Angular `bypassSecurityTrustHtml`
  - Multi-reflection chaining: reflect in two different contexts → combine to form valid injection
  - DOM Clobbering: HTML injection without JS execution → override global variables via `id`/`name` attributes (HTMLCollection, form.name.input), bypass script-src CSP via clobbered script loading variables → see `s-dom-clobbering` skill for full methodology
- Note fallback techniques: if primary fails, what to try next

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads, each labeled with context and expected result:
  1. **Primary payload** (highest confidence for this context): raw payload + encoding notes
  2. **Bypass variant** (WAF/filter evasion): mutated payload + which filter it evades
  3. **Minimal variant** (shortest effective, for length-constrained inputs): compact payload
- Each entry format: `[Context] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/xss/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Input validation bypass**: encoding variants, case mutation, tag/attribute alternatives (e.g., `<img>` for blocked `<script>`, `onpointerenter` for blocked `onerror`)
  2. **WAF rule bypass**: fragmentation (`"><script>`, line breaks, comment injection), parameter pollution, alternative event handlers
  3. **CSP bypass**: JSONP endpoints on same origin, Angular sandbox escape, `strict-dynamic` + DOM XSS gadget, base-uri hijacking
  4. **Output encoding bypass**: context-specific encoding differences (SVG vs. HTML, `src` vs. `href` attribute quoting)

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
