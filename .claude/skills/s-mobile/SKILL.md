---
name: s-mobile
description: Unified Mobile Security skill linking hack-skills methodology with AboutSecurity execution resources. Covers Android/iOS app pentesting, SSL pinning bypass, Frida/objection instrumentation, Burp proxy setup, and mobile API security testing.
---

# Unified Mobile Security

## When To Use

Use for Android/iOS application security assessment, mobile API traffic interception, SSL pinning bypass, runtime instrumentation (Frida/objection), reverse engineering (jadx/apktool), and mobile-specific attack surfaces (deep links, WebView, app-to-app communication).

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

## Conflict Resolution

1. Safety and authorization rules always have highest priority.
2. AboutSecurity `NEVER`, `ALWAYS`, `禁止`, `必须`, `⛔` rules override general methodology during execution.
3. hack-skills is preferred for scenario classification, knowledge depth and real-world methodology.
4. AboutSecurity is preferred for tools, payloads, dictionaries, CTF and automated execution constraints.

## Matched hack-skills Skills

- `../../security-sources/hack-skills/skills/android-pentesting-tricks/SKILL.md` — SKILL: Android Pentesting Tricks — Expert Playbook
- `../../security-sources/hack-skills/skills/ios-pentesting-tricks/SKILL.md` — SKILL: iOS Pentesting Tricks — Expert Playbook
- `../../security-sources/hack-skills/skills/mobile-ssl-pinning-bypass/SKILL.md` — SKILL: Mobile SSL Pinning Bypass — Expert Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/mobile/android-app-pentesting/SKILL.md` — Android APP 渗透测试方法论
- `../../security-sources/AboutSecurity/skills/mobile/ios-pentesting/SKILL.md` — iOS 渗透测试方法论
- `../../security-sources/AboutSecurity/skills/mobile/ios-exploiting/SKILL.md` — iOS 漏洞利用

## Related AboutSecurity Tools / Payloads / Dictionaries

- No match found.

## References

See `references/SOURCES.md`.

## Mobile Security Testing Workflow

### Step 1: 环境准备
- Android: Genymotion/Android Studio AVD (rooted), Burp Suite proxy, Frida server, objection
- iOS: jailbroken device / Corellium, Burp + certificate trust, Frida/objection
- Set up proxy: `adb reverse tcp:8080 tcp:8080` (Android) or WiFi proxy (iOS)

### Step 2: APK/IPA 分析
- Decompile: `jadx-gui target.apk`, `apktool d target.apk`
- Extract hardcoded secrets: API keys, tokens, endpoints, cryptographic keys
- Analyze AndroidManifest.xml: exported components, permissions, intent filters, deep links
- Map API endpoints from decompiled code

### Step 3: 流量拦截
- SSL pinning bypass with Frida scripts or objection (`android sslpinning disable`)
- Capture all API calls and analyze for: auth token handling, parameter patterns, API versioning
- Test same API endpoints with different auth contexts (horizontal/vertical privilege escalation)

### Step 4: 专项测试
- Deep link exploitation (custom scheme → WebView → XSS/file access)
- WebView JavaScript Interface injection
- Local storage analysis (SharedPreferences, SQLite, Keychain, plist)
- Intent/Broadcast hijacking (Android), URL Scheme hijacking (iOS)

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- ⛔ Mobile app testing requires the app to be installed on a controlled device — never install modified versions on production devices.
- Only operate in authorized environments.
