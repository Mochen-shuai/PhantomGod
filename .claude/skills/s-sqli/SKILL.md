---
name: s-sqli
description: Unified SQL Injection skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified SQL Injection

## When To Use

Use for authorized SQL injection assessment, CTF SQLi tasks, database error-based/blind/time-based/OOB scenarios.

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

- `../../security-sources/hack-skills/skills/sqli-sql-injection/SKILL.md` — SKILL: SQL Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/nosql-injection/SKILL.md` — SKILL: NoSQL Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/ghost-bits-cast-attack/SKILL.md` — SKILL: Ghost Bits / Cast Attack — Java char to byte Narrowing Playbook
- `../../security-sources/hack-skills/skills/jwt-oauth-token-attacks/SKILL.md` — SKILL: JWT and OAuth 2.0 Token Attacks — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/authbypass-authentication-flaws/SKILL.md` — SKILL: Authentication Bypass — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/sql-injection-methodology/SKILL.md` — SQL 注入完整方法论
- `../../security-sources/AboutSecurity/skills/exploit/web-method/nosql-injection/SKILL.md` — NoSQL 注入方法论
- `../../security-sources/AboutSecurity/skills/exploit/network-service/sqlserver-attack/SKILL.md` — SQL Server 渗透测试与利用
- `../../security-sources/AboutSecurity/skills/exploit/network-service/postgresql-pentesting/SKILL.md` — PostgreSQL 渗透测试方法论 (5432)
- `../../security-sources/AboutSecurity/skills/exploit/network-service/mysql-pentesting/SKILL.md` — MySQL 渗透测试方法论 (3306)

## Related AboutSecurity Tools

- No match found.

## Related AboutSecurity Payloads

- `../../security-sources/AboutSecurity/Payload/sqli/table.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/_meta.yaml`
- `../../security-sources/AboutSecurity/Payload/sqli/column.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/sql-inj.md`
- `../../security-sources/AboutSecurity/Payload/sqli/payload.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/database.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/payload-ldap.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/payload-blind.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/payload-mssql.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/payload-mysql.txt`
- `../../security-sources/AboutSecurity/Payload/sqli/payload-oracle.txt`
- `../../security-sources/AboutSecurity/Payload/prompt-injection/prompt.md`
- `../../security-sources/AboutSecurity/Payload/prompt-injection/_meta.yaml`

## Related AboutSecurity Dictionaries

- `../../security-sources/AboutSecurity/Dic/web/api-param/param-sqli.txt`
- `../../security-sources/AboutSecurity/Dic/web/ctf/sql.txt`
- `../../security-sources/AboutSecurity/Dic/port/mysql/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/mysql/user.txt`
- `../../security-sources/AboutSecurity/Dic/auth/password/sql.txt`
- `../../security-sources/AboutSecurity/Dic/port/mysql/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/port/sqlserver/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/sqlserver/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/postgresql/pass.txt`
- `../../security-sources/AboutSecurity/Dic/port/postgresql/user.txt`
- `../../security-sources/AboutSecurity/Dic/port/sqlserver/_meta.yaml`
- `../../security-sources/AboutSecurity/Dic/port/postgresql/_meta.yaml`

## Related AboutSecurity Docs

- No match found.

## References

See `references/SOURCES.md`.

## Vulnerability Testing Output Template

When you discover a potential SQL Injection vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template. This applies regardless of which upstream methodology you use.

### Module 1: 测试思路 (Testing Approach)
- Describe the injection context: GET/POST parameter, cookie header, JSON body, or blind/OOB
- Classify the injection type: error-based / UNION-based / boolean blind / time blind / stacked / OOB
- State the DBMS fingerprint evidence (error messages, version strings, behavioral quirks)
- Document the decision tree: parameter tampering → syntax error detection → injection type determination → DBMS identification → extraction method selection
- State expected success indicator: data exfiltration, time delay, DNS callback, error message content

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

**在任何 exploit payload 之前**，在正常参数值**中间**插入单一特殊字符/关键字，探测防护规则：
- 空白符：` ` `\t` `\n`
- 注释符：`#` `-- ` `/**/`
- 关键字：`AND` `OR` `SELECT` `UNION` `SLEEP` `BENCHMARK`
- 符号：`'` `"` `(` `)` `%` `;` `=` `+`

每个元素单独测试，记入结构化 `filter_probe`：`{符号: [防护情况, 说明]}`。
防护情况枚举：`放行` / `过滤` / `替换` / `拦截` / `转义`。

**禁止**把完整 payload 当 key。**禁止**在 filter_probe 为空时进入 Module 3。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md` — **SQL001~004**。
> `tested_not_found` / `doubtful` / `filtered` 时**必须逐条应答** checkpoint_response。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - Column count discovery: ORDER BY binary search (not linear), NULL padding matching
  - EXTRACTVALUE/UPDATEXML 32-character truncation trap — use mid()/substr() for long data
  - Second-order injection: payload stored in one place, executed in another (profile name → admin view)
  - Ghost bits / cast attacks (Java char→byte narrowing): `CAST(0x... AS CHAR)`
- Note: ⛔ Never manually substring flag data — use scripted extraction

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Detection payload** (confirm injection): `' OR '1'='1` / `' AND SLEEP(5)--` / `' UNION SELECT NULL--`
  2. **Extraction payload** (data retrieval): DBMS-specific UNION/error-based/blind payload
  3. **Escalation payload** (if applicable): `xp_cmdshell` (MSSQL), `INTO OUTFILE` (MySQL), `UTL_HTTP` (Oracle OOB)
- Each entry format: `[Injection Type / DBMS] <payload>` → expected behavior
- Source payloads from upstream `AboutSecurity/Payload/sqli/` files when applicable

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Input validation bypass**: keyword splitting (UN/**/ION), case mutation (sElEcT), hex/char encoding, whitespace alternatives (/**/, %09, %0a)
  2. **WAF rule bypass**: comment injection (`/*!50000SELECT*/`), parameter pollution (`?id=1&id=2 UNION SELECT`), HTTP method override, Content-Type manipulation
  3. **Prepared statement edge cases**: ORDER BY/GROUP BY injection (cannot parameterize), LIKE clause injection, table/column name from user input
  4. **Rate limiting bypass**: time-based with randomized delays, multi-IP rotation, session token cycling

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
