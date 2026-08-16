---
name: s-sop-bypass
description: Same-Origin Policy Deep Dive and Bypass skill. Covers SOP restriction matrix, cross-origin data access techniques, postMessage misconfiguration, document.domain relaxation, CORS bypass chaining, and browser-specific SOP quirks.
---

# Unified Same-Origin Policy Bypass

## When To Use

Use for understanding and testing SOP restrictions, discovering cross-origin information leakage, auditing postMessage handlers, exploiting document.domain relaxation, and browser-specific SOP edge cases.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | hack-skills |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

SOP concepts are distributed across multiple existing skills (CORS, XSS, CSRF, Clickjacking). This skill provides a unified SOP mental model and cross-references those skills for specific exploitation techniques.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/cors-cross-origin-misconfiguration/SKILL.md` — CORS Misconfiguration
- `../../security-sources/hack-skills/skills/clickjacking/SKILL.md` — Clickjacking (frame boundary)
- (postMessage patterns distributed across XSS and client-side skills)

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/auth/cors-misconfiguration/SKILL.md` — CORS 错误配置
- `../../security-sources/AboutSecurity/skills/exploit/web-method/xss-methodology/SKILL.md` — XSS (postMessage exploitation)

## References

See `references/SOURCES.md`.

## SOP 核心概念

### SOP 限制矩阵
| 资源 | 读 | 写 | 特殊规则 |
|------|:--:|:--:|---------|
| Cookie | 同源 only | domain/path 限定 | `SameSite` 收紧 |
| LocalStorage/SessionStorage | 同源 only | 同源 only | 完全隔离 |
| DOM (iframe) | 同源 only | 子域可 `document.domain` 放松 | 端口号也参与判定 |
| XHR/Fetch | CORS | 无预检的简单请求可跨域写 | 读由 ACAO 头控制 |
| WebSocket | 无同源限制 | 无同源限制 | 由服务器 `Origin` 检查保护 |
| postMessage | 任意源可发送 | 接收方必须验证 `event.origin` | 无验证 = SOP 完全绕过 |

### 核心 bypass 向量
1. **postMessage 无 origin 验证**：接收方不检查 `event.origin` → 任意页面可向目标发送消息
2. **document.domain 放松**：`a.example.com` 和 `b.example.com` 同时设置 `document.domain = "example.com"` → 相互访问 DOM
3. **CORS 配置错误**：`Access-Control-Allow-Origin: null` + 沙盒 iframe
4. **浏览器 quirks**：IE/旧 Edge 的 SOP 边界差异（端口不在 SOP 中）

## Important Agent Rules

- SOP 是浏览器安全的基础 — 理解其边界比单点利用更重要
- postMessage handler 审计是最高价值的 SOP 相关测试
- 现代浏览器持续收紧 SOP（SameSite=Lax 默认、Origin-Agent-Cluster）— 绕过方法随版本变化
