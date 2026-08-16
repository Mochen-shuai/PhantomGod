---
name: s-cms-middleware
description: Unified CMS and Middleware Security skill. Covers CMS (WordPress/Drupal/Joomla) vulnerability assessment, middleware (Nginx/Apache/Tomcat/IIS) misconfiguration testing, default credentials, and known CVE exploitation.
---

# Unified CMS / Middleware Security

## When To Use

Use for CMS fingerprinting and CVE assessment (WordPress, Drupal, Joomla), middleware misconfiguration testing (Nginx, Apache, Tomcat, IIS), default credential checking, and known CVE validation against common deployment stacks.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | AboutSecurity |
| Ctf | AboutSecurity |
| Bug Bounty | hack-skills |
| Resources | AboutSecurity |

## Source Strategy

- Use hack-skills for methodology and attack playbooks.
- Use AboutSecurity for CVE database (`AboutSecurity/Vuln/middleware/`) and framework audit skills.
- This skill provides a unified entry point; per-CMS detail lives in AboutSecurity Vuln files.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/401-403-bypass-techniques/SKILL.md` — 401/403 Bypass Techniques
- `../../security-sources/hack-skills/skills/waf-bypass-techniques/SKILL.md` — WAF Bypass Techniques

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/code-audit/php/php-framework-audit/SKILL.md` — PHP 框架审计
- `../../security-sources/AboutSecurity/Vuln/middleware/` — 中间件漏洞库（Spring/Tomcat/GitLab/Jenkins/JumpServer/Kibana/Portainer/n8n/Skywalking/Laravel）

## Related AboutSecurity Tools / Payloads / Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/directory/main.txt`
- `../../security-sources/AboutSecurity/Dic/web/directory/common.txt`

## References

See `references/SOURCES.md`.

## CMS/Middleware Testing Workflow

### Step 1: 指纹识别
- Use WhatWeb, Wappalyzer, or manual header/cookie analysis
- Check: `X-Powered-By`, `Server`, `Set-Cookie` (PHPSESSID, JSESSIONID, etc.)
- File presence checks: `/wp-admin`, `/administrator`, `/sites/default/settings.php`
- Version detection: README.html, CHANGELOG.txt, generator meta tags

### Step 2: 已知 CVE 检测
- Cross-reference detected CMS/middleware + version with NVD/AboutSecurity Vuln database
- Check for unpatched critical CVEs within the target's version range
- Verify using nuclei or manual PoC (non-destructive first)

### Step 3: 配置错误检测
| 中间件 | 常见配置错误 |
|--------|------------|
| Nginx | 路径穿越（alias trailing slash），CRLF injection，raw backend exposure |
| Apache | Directory listing enabled, `.htaccess` bypass, mod_status public |
| Tomcat | `/manager` `/host-manager` default creds, AJP secret leak (Ghostcat) |
| IIS | WebDAV PUT allowed, Tilde shortname enumeration, MS15-034 HTTP.sys |
| WordPress | `wp-json/wp/v2/users` user enumeration, `xmlrpc.php` brute force, plugin/theme file disclosure |

### Step 4: 加固绕过
- See `knowledge/bypass-catalogue.md` for WAF/403/404 bypass techniques
- Default admin paths: `/admin` → `/Admin` → `/administrator` → `/wp-admin`
- Trailing slash normalization: `/admin` → `/admin/` → `/admin/.` → `/admin;.js`

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files and AboutSecurity Vuln database.
- ⛔ CMS plugin/theme exploitation can lead to full server compromise — verify on authorized targets only.
- Only operate in authorized environments.
