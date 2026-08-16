---
name: s-frontend-reverse
description: Unified Frontend Reverse Engineering skill. Covers Webpack SourceMap reconstruction, JS bundle deobfuscation, minified code analysis, API endpoint extraction from frontend code, and modern SPA (Vue/React/Angular) source recovery.
---

# Unified Frontend Reverse Engineering

## When To Use

Use for reverse engineering minified/obfuscated JavaScript, SourceMap extraction and reconstruction, API endpoint discovery from frontend bundles, Webpack chunk analysis, and SPA component structure recovery.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | hack-skills |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

- Use hack-skills for methodology and broader patterns.
- Use AboutSecurity for JS API extraction and SPA audit patterns.
- Many techniques draw from general reverse engineering patterns — adapt as needed.

## Recommended Loading Order

1. Read `../../security-sources/hack-skills/skills/code-obfuscation-deobfuscation/SKILL.md` for deobfuscation patterns.
2. Read `../../security-sources/AboutSecurity/skills/recon/js-api-extract/SKILL.md` for JS API extraction.
3. Read `../../security-sources/AboutSecurity/skills/exploit/web-method/api-fuzz/SKILL.md` for API fuzzing discovered endpoints.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/code-obfuscation-deobfuscation/SKILL.md` — SKILL: Code Obfuscation & Deobfuscation — Expert Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/recon/js-api-extract/SKILL.md` — JS API 端点提取
- `../../security-sources/AboutSecurity/skills/exploit/web-method/api-fuzz/SKILL.md` — API 模糊测试

## Related AboutSecurity Tools / Payloads / Dictionaries

- No match found.

## References

See `references/SOURCES.md`.

## Frontend Reverse Engineering Workflow

### Step 1: SourceMap 发现与提取
- Load target site in Chrome DevTools → Sources tab → look for `webpack://` entries
- If SourceMap URL is present in JS files (`//# sourceMappingURL=app.js.map`), download directly
- Check robots.txt for excluded `.map` files
- Use `source-map` NPM package or `unwebpack-sourcemap` to reconstruct source tree from `.map`

### Step 2: Webpack Bundle 解构
- Identify Webpack chunks: look for `webpackJsonp`, `__webpack_require__`, module ID patterns
- Extract individual modules: use `webpack-bundle-analyzer` or manual regex extraction
- Map module IDs to functions: identify entry points, route definitions, API service modules

### Step 3: API 端点提取
- Grep for URL patterns: `/(api|graphql|v[0-9])\/[a-zA-Z/-]+/g`
- Grep for HTTP methods wrapped in framework calls: `axios.get(` `fetch(` `$http.post`
- Extract endpoint paths, methods, expected parameters, and authentication headers
- Cross-reference with actual network traffic (Burp history) for gaps

### Step 4: 去混淆
- Identify obfuscation type: Webpack/rollup minification only, or deliberate obfuscation (obfuscator.io, JSFuck)
- Use AST-based deobfuscation (Babel plugins) for control-flow flattening, string array extraction
- Manual analysis: identify the initialization function that populates string tables

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- ⛔ JS source reconstruction from SourceMap recovers original source code — treat as intellectual property, do not redistribute.
- Only operate in authorized environments.
