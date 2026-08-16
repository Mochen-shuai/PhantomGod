---
name: s-security-hub
description: Unified security skill router combining yaklang/hack-skills methodology with wgpsec/AboutSecurity execution resources.
---

# Security Hub

Use this as the first entry point for security-related Agent tasks.

## Design

This is a federated skill hub, not a fork merge.

- hack-skills: methodology, domain routing, deep playbooks, scenario reasoning.
- AboutSecurity: execution constraints, dictionaries, payloads, tool YAML configs, CTF/K8s fine-grained resources.

## Loading Policy

1. Start here.
2. Pick the closest unified topic.
3. For broad reasoning, prefer hack-skills unless the topic priority says otherwise.
4. For execution constraints and tools, prefer AboutSecurity.
5. For CTF-style tasks, prioritize AboutSecurity unless the topic is mainly pwn/crypto/web3/LLM.
6. For bug bounty or real-world assessment methodology, prioritize hack-skills.
7. Only perform security testing in authorized environments.

## Unified Topics

| Topic | Use When | Skill |
|---|---|---|
| SQL Injection | Use for authorized SQL injection assessment, CTF SQLi tasks, database error-based/blind/time-based/OOB scenarios. | `unified-sqli` |
| Cross-Site Scripting | Use for reflected, stored and DOM XSS analysis, payload selection, filter bypass and verification. | `unified-xss` |
| Server-Side Request Forgery | Use for SSRF discovery, cloud metadata access checks, URL parser bypasses and callback verification. | `unified-ssrf` |
| File Upload Security | Use for upload validation analysis, extension/content-type bypass, image/polyglot upload checks. | `unified-file-upload` |
| Path Traversal and File Inclusion | Use for path traversal, LFI/RFI, arbitrary file read and path normalization bypass. | `unified-path-traversal` |
| Command Injection | Use for OS command injection analysis, shell metacharacter testing and safe verification. | `unified-command-injection` |
| Authentication and Authorization | Use for authentication bypass, authorization flaws, JWT/OAuth/session security review. | `unified-auth` |
| API Security | Use for API enumeration, BOLA/BFLA, mass assignment, GraphQL and REST security testing. | `unified-api-security` |
| Reconnaissance | Use for asset discovery, subdomain enumeration, port scanning, fingerprinting and attack surface mapping. | `unified-recon` |
| Kubernetes and Cloud Native Security | Use for Kubernetes, container, ingress, admission webhook, sidecar and cloud-native security assessment. | `unified-k8s-cloud-native` |
| Binary Exploitation | Use for binary exploitation, stack/heap exploitation, format string, kernel and sandbox pwn learning. | `unified-pwn` |
| Cryptography Attacks | Use for CTF and practical cryptography attack methodology. | `unified-crypto` |
| Web3 and Smart Contract Security | Use for smart contract audit methodology, DeFi attack pattern review and Web3 security testing. | `unified-web3` |
| LLM and AI Security | Use for LLM prompt injection, model security, AI application security and agent safety review. | `unified-llm-security` |

## Penetration Test Report Format

When delivering a FULL penetration test report (multiple vulnerability findings), use this standardized structure. For individual single-vulnerability reports, follow the CLAUDE.md format instead.

### 1. 执行摘要 (Executive Summary)
- Assessment scope: target domain(s), IP ranges, time period
- Testing methodology: recon → asset classification → JS/API extraction → vulnerability testing → verification
- Overall risk rating: Critical (P0) / High (P1-P2) / Medium (P3) / Low (P4) / Informational
- Top 3-5 findings summary with severity and business impact
- Remediation priority roadmap (what to fix first)

### 2. 资产清单 (Asset Inventory)
- Discovered subdomains and their classification (web, API, admin, dev, CDN, internal)
- Technology stack fingerprinting results per asset
- Extracted API endpoints (even those not found vulnerable)
- JS file inventory with grade classification (A/B/C)
- Third-party components and identified CVE matches

### 3. 测试方法论 (Testing Methodology)
- Reconnaissance approach: tools used, scope, phases executed
- JS source acquisition: Wayback Machine, mini-program, async chunks, backup files
- Vulnerability testing: which unified-* skills were applied and in what order
- Limitations: out-of-scope items, testing constraints, time/resource limitations

### 4. 漏洞发现 (Vulnerability Findings)
For each finding, include the following fixed fields (compatible with CLAUDE.md single-report format):

| Field | Content |
|-------|---------|
| **Finding ID** | `VULN-001`, `VULN-002`, etc. |
| **Severity** | P0 (Critical) to P4 (Informational) |
| **Title** | `[P等级] 漏洞类型 @ 目标位置` |
| **Location** | Full URL, endpoint, parameter, method |
| **Description** | Technical details of the vulnerability and its root cause |
| **PoC** | One-click curl command or Python script (from CLAUDE.md requirement) |
| **Reproduction Steps** | Step-by-step with exact requests and responses |
| **Impact** | What an attacker can achieve, with business context |
| **Remediation** | Specific, actionable fix recommendation |

### 5. 技术附录 (Technical Appendices)
- Full asset discovery output (subdomains, ports, services)
- Complete API endpoint enumeration results
- Vulnerability scanning tool output (nuclei, sqlmap, etc.)
- JS file grading detail (Grade A/B/C classification with rationale)
- Self-check results for each finding (from CLAUDE.md checklist)

### Interaction with CLAUDE.md

| Scope | Use This Format | Use CLAUDE.md Format |
|-------|----------------|---------------------|
| Single vulnerability | ✗ | ✓ (PoC + steps + self-checklist) |
| Multi-vulnerability assessment | ✓ (use CLAUDE.md format for each VULN-xxx entry) | ✗ |
| Recon-only output | ✗ | ✗ (free-form asset list) |

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
