---
name: s-clickjacking
description: Unified Clickjacking and XS-Leaks skill linking hack-skills methodology with AboutSecurity execution resources. Covers clickjacking (UI redressing), XS-Leaks (cross-site leak) techniques, frame busting bypass, and postMessage-based attacks.
---

# Unified Clickjacking / XS-Leaks

## When To Use

Use for clickjacking/UI redressing assessment, frame busting script evaluation, X-Frame-Options/CSP frame-ancestors bypass, XS-Leaks detection (frame count, redirect timing, CSS injection), and cross-origin information leakage.

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

- `../../security-sources/hack-skills/skills/clickjacking/SKILL.md` — SKILL: Clickjacking — Expert Attack Playbook

## Matched AboutSecurity Skills

- (Clickjacking techniques referenced in XSS methodology)
- `../../security-sources/AboutSecurity/skills/exploit/web-method/xss-methodology/SKILL.md`

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

When you discover a potential Clickjacking or XS-Leaks vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the target context: sensitive action page (account deletion, password change, fund transfer, OAuth authorization), frame embedding behavior
- Classify the attack type: standard clickjacking (transparent iframe overlay), double-clickjacking (rapid double-click sequence), drag-and-drop jacking, or XS-Leaks (cross-site information leakage via side channels)
- Check anti-framing defenses: `X-Frame-Options` (DENY/SAMEORIGIN/ALLOW-FROM), `Content-Security-Policy: frame-ancestors`, frame busting JavaScript (`if (top !== self) top.location = self.location`)
- Document the decision tree: framing check → anti-frame bypass assessment → overlay PoC construction → XS-Leaks: side-channel identification (frame count, redirect timing, CSS :visited, cache probing, performance API)
- State expected success indicator: victim's click on attacker's page triggers action on target site (clickjacking), or attacker's page extracts cross-origin information from target (XS-Leaks)

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

对目标页面进行框架嵌入测试：
- 直接 `<iframe src="target">` — 检查是否可嵌入
- `<iframe sandbox="allow-forms allow-scripts" src="target">` — sandbox iframe 是否绕过 frame busting
- `X-Frame-Options` 头值检查：DENY / SAMEORIGIN / ALLOW-FROM uri / 缺失
- `CSP: frame-ancestors` 指令检查
- Frame busting JS 检查：`if(top != self)` / `if(top.location != document.location)`

每个单独测试，记入 `{操作: [结果, 说明]}`。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **CLICK001~003**。
> ⛔ 不可仅凭 X-Frame-Options 存在判 `tested_not_found` — CSP frame-ancestors 可与 XFO 共存但不一致。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Mobile-specific double-clickjacking**: attacker page has a button that moves on first click (revealing the target iframe underneath just as the second click lands) — the double-click timing window bypasses mobile tap-highlight and delay defenses
  - **sandbox iframe frame-busting bypass**: `<iframe sandbox="allow-forms allow-scripts allow-top-navigation">` — sandbox without `allow-top-navigation` prevents `top.location = ...` in the framed page, neutering frame-busting scripts
  - **XS-Leaks via frame count**: `frames.length` in a cross-origin popup/window — different response states produce different sub-frame counts; use this to infer boolean information (e.g. "user is admin" based on admin panel sub-frame presence)
  - **CSS-based XS-Leaks**: `:visited` color history sniffing (patched), but modern variants use `mix-blend-mode` with scroll-to-text-fragment or lazy loading image dimensions as oracle

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Classic clickjacking PoC**: transparent iframe overlaid on a deceptive button, CSS `opacity: 0` + `z-index` trick, double-clickjacking with `onmousedown` handler
  2. **Frame busting bypass**: use `<iframe sandbox="allow-forms allow-scripts">` (no `allow-top-navigation`), or `onbeforeunload` event to block the busting redirect
  3. **XS-Leaks probe**: `window.open("target.com/settings", "leak")` → measure `frames.length` or `history.length`, or use `performance.getEntriesByType("resource")` timing oracle
- Each entry format: `[Attack Type] <PoC structure>` → expected behavior

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **X-Frame-Options bypass**: CSP `frame-ancestors` overrides XFO in modern browsers; if both are set but CSP is weaker (e.g. `frame-ancestors *`), the weaker CSP wins. Also: old IE versions support `ALLOW-FROM` but not `frame-ancestors`.
  2. **Frame busting script bypass**: `onbeforeunload` + `event.returnValue = ''` prevents navigation; `sandbox` attribute without `allow-top-navigation`; multiple nested iframes where inner iframe bounces back
  3. **CSP frame-ancestors bypass**: check if the CSP is only partially deployed (e.g. `frame-ancestors 'self'` but subdomain takeover allows attacker to host on a sibling subdomain)
  4. **XS-Leaks detection evasison**: when `SameSite=Lax` cookies prevent framing, use `window.open` + `postMessage` timing, or `fetch` with `mode: "no-cors"` timing side-channels

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- ⛔ Clickjacking/XS-Leaks PoC pages must not be deployed to public-accessible URLs without authorization.
- Only operate in authorized environments.
