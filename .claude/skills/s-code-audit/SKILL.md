---
name: s-code-audit
description: Unified Code Audit skill linking hack-skills methodology with AboutSecurity execution resources. Covers PHP/Java/Python source code security audit methodology, dangerous function tracing, data flow analysis, and automated auditing with Semgrep/CodeQL.
---

# Unified Code Audit

## When To Use

Use for PHP/Java/Python web application source code security audit, dangerous function identification, taint analysis (source→sink tracing), framework-specific vulnerability patterns, and automated static analysis.

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

- (No direct match — methodology distributed across per-vuln-type Skills)

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/code-audit/php/php-audit-pipeline/SKILL.md` — PHP 代码审计流水线
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-injection-audit/SKILL.md` — PHP 注入类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-serialization-audit/SKILL.md` — PHP 反序列化源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-file-audit/SKILL.md` — PHP 文件操作源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-auth-config-audit/SKILL.md` — PHP 认证配置源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-framework-audit/SKILL.md` — PHP 框架源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-frontend-audit/SKILL.md` — PHP 前端源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/php/php-exploit-chain/SKILL.md` — PHP 漏洞利用链
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-audit-pipeline/SKILL.md` — Java 代码审计流水线
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-injection-audit/SKILL.md` — Java 注入类漏洞源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-serialization-audit/SKILL.md` — Java 反序列化源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-file-audit/SKILL.md` — Java 文件操作源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-auth-config-audit/SKILL.md` — Java 认证配置源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-framework-audit/SKILL.md` — Java 框架源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-frontend-audit/SKILL.md` — Java 前端源码审计
- `../../security-sources/AboutSecurity/skills/code-audit/java/java-exploit-chain/SKILL.md` — Java 漏洞利用链

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

When you conduct a source code security audit, ⛔ **MUST** structure findings using this fixed output template.

### Module 1: 审计思路 (Audit Approach)
- Describe the audit scope: codebase overview (framework, language version, dependencies), entry points (routes, controllers, API handlers), authentication/authorization mechanism
- Choose the audit methodology: forward trace (user input → sink) or reverse trace (dangerous function → user input) → document the choice with justification
- Identify the key attack surfaces: auth flow, file operations, database queries, deserialization points, template rendering, external API calls, file uploads
- Document the decision tree: entry point enumeration → parameter tracking → middleware bypass check → dangerous function mapping → taint analysis per sink type
- State the output format: vulnerability location (file:line), taint path, exploitability assessment

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Middle-man method tracing**: trace indirect dangerous function calls through framework wrappers — e.g. Laravel `DB::raw()` calls `PDO::query()` internally; the developer may not recognize the wrapper as a sink
  - **Global state injection**: language-specific globals like PHP `$_SERVER['HTTP_HOST']`, `$_REQUEST`, `$GLOBALS`, Java `ThreadLocal`, Python `flask.g` — often missed by grep-based audits because the source is implicit
  - **Autoloader and dynamic instantiation**: PHP `class_exists($userInput)`, Java `Class.forName()` + reflection, Python `importlib.import_module()` — when class/function names are user-controlled, they create injection vectors no grep-based audit catches
  - **ORM bypass patterns**: ORMs can't parameterize table/column names, `ORDER BY`, `GROUP BY`, `LIMIT` — but developers assume ORM = safe. Audit for dynamic table/column names from user input.

### Module 3: 危险函数全景 (Dangerous Function Atlas)
- ⛔ Per-language dangerous function mapping (load per-language AboutSecurity audit skill for full atlas):

**PHP:**
- RCE: `eval()`, `assert()`, `preg_replace(/e)`, `create_function()`, `call_user_func()`, `system()`, `exec()`, `shell_exec()`, `passthru()`, `popen()`, `proc_open()`, `` `backticks` ``
- File: `include/require`, `file_get_contents()`, `file_put_contents()`, `fopen()`, `unlink()`, `move_uploaded_file()`
- SQL: `mysql_query()`, `mysqli_query()`, `PDO::query()`, `DB::raw()`, `DB::select()`
- Deserialization: `unserialize()`, `phar://` stream wrapper

**Java:**
- RCE: `Runtime.exec()`, `ProcessBuilder`, `ScriptEngine.eval()`, `SpEL ExpressionParser`
- JNDI: `InitialContext.lookup()`
- Deserialization: `ObjectInputStream.readObject()`, `XMLDecoder.readObject()`, `Yaml.load()`
- SQL: `Statement.executeQuery()` (non-PreparedStatement), `MyBatis ${}` notation

**Python:**
- RCE: `eval()`, `exec()`, `compile()`, `os.system()`, `os.popen()`, `subprocess.Popen(shell=True)`, `pickle.loads()`
- SSTI: `render_template_string()`, `jinja2.Template()`, `mako.template.Template()`
- File: `open()`, `pathlib.Path.read_text()` with user-controlled path

### Module 4: 审计 Checklist (Audit Checklist)
- ⛔ Per-audit checklist:
  1. All user input sources enumerated (GET/POST/Cookie/Header/File upload/WebSocket/Message queue)
  2. All authentication filters traced — any unauthenticated access paths?
  3. All authorization checks traced — any IDOR-prone direct object references?
  4. All SQL queries checked — any concatenation/interpolation? ORM dynamic column/table names?
  5. All deserialization calls checked — any user-controlled serialized data?
  6. All template renders checked — any user-controlled template content or variables in non-autoescaped context?
  7. All file operations checked — any user-controlled path? Upload directory traversal?
  8. All external HTTP calls checked — any user-controlled URL? (SSRF)
  9. All command executions checked — any user-controlled command/arguments?
  10. All cryptographic operations checked — any hardcoded keys/salts? Weak algorithm?

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task (per-language AboutSecurity audit skills).
- Preserve and obey upstream mandatory execution rules.
- ⛔ Source code audit must be on authorized codebases only (open source, CTF, or authorized engagement).
- ⛔ Do not retain or distribute audited source code after the engagement.
