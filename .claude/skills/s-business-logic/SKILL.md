---
name: s-business-logic
description: Unified Business Logic Vulnerability skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Business Logic Vulnerabilities

## When To Use

Use for business logic flaw discovery: payment manipulation, coupon/points bypass, parameter tampering, race conditions, workflow abuse, negative quantity, privilege escalation via logic gaps.

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

- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/SKILL.md` — Business Logic Vulnerabilities: payment bypass, coupon manipulation, workflow abuse, race conditions, negative quantity
- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/CHECKLIST.md` — Business Logic testing checklist
- `../../security-sources/hack-skills/skills/business-logic-vulnerabilities/SCENARIOS.md` — Real-world business logic exploit scenarios

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/web-method/business-logic-attack/SKILL.md` — 业务逻辑漏洞攻击方法论

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

When you discover a potential business logic vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 0: 约束条件分析（⛔ 必须先行）

梳理业务流程约束条件来源：页面文案（隐性约束如"优惠已过期"）、前端校验代码、报错信息。
确定测试方向：**导致自身非法获利或他人利益受损**，不测仅导致自身损失的方向。

> 编号化测试要点见 `../pentest-windftsy/references/test-checkpoints.md`：
> 竞态 **RACE001~003**、重放 **REPLAY001**、优惠复用 **PRIZE001**、验证码绕过 **SMS001~002**、用户枚举 **ENUM001~002**。

### Module 1: 测试思路 (Testing Approach)
- Describe the business flow: steps, actors, state transitions
- Identify check-then-act patterns vulnerable to TOCTOU
- Identify client-controllable values that should be server-determined (price, quantity, discount, role)
- State expected success indicator: unauthorized benefit, state bypass, double redemption

### Module 2: 关键技巧 (Key Techniques)
- State machine diagram: draw legitimate transitions, test illegal ones
- Race window identification: find time gap between check and act
- Negative/zero value injection: try `-1`, `0`, `0.01`, `999999` on numeric fields
- Parameter removal: omit the parameter entirely, test default values
- Concurrent request: new payloads (not replay), parallel send

### Module 3: Payload字典 (Payload Dictionary)
1. **金额/数量篡改**: negative, zero, extreme values, string type coercion
2. **状态机绕过**: skip prerequisites, jump to final state, reverse transitions
3. **竞态双花**: new request × N concurrent, verify server-side state
4. **验证码绕过**: empty, omit param, reuse, brute force, response leak

### Module 4: 绕过方法 (Bypass Methods)
1. **客户端校验**: remove HTML attributes, override JS validation functions
2. **签名保护**: test key predictability, timestamp reuse, algorithm downgrade
3. **幂等性缺失**: resubmit identical request, replay with modified timestamp

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
