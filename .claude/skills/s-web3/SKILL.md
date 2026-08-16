---
name: s-web3
description: Unified Web3 and Smart Contract Security skill linking hack-skills methodology with AboutSecurity execution resources.
---

# Unified Web3 and Smart Contract Security

## When To Use

Use for smart contract audit methodology, DeFi attack pattern review and Web3 security testing.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | hack-skills |
| Execution | hack-skills |
| Ctf | hack-skills |
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

- `../../security-sources/hack-skills/skills/smart-contract-vulnerabilities/SKILL.md` — SKILL: Smart Contract Vulnerabilities — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/defi-attack-patterns/SKILL.md` — SKILL: DeFi Attack Patterns — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/sqli-sql-injection/SKILL.md` — SKILL: SQL Injection — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/lattice-crypto-attacks/SKILL.md` — SKILL: Lattice-Based Cryptanalysis — Expert Attack Playbook
- `../../security-sources/hack-skills/skills/classical-cipher-analysis/SKILL.md` — SKILL: Classical Cipher Analysis — Expert Cryptanalysis Playbook

## Matched AboutSecurity Skills

- No match found.

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

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- Avoid unnecessary brute force or destructive testing.
- Only operate in authorized environments.
