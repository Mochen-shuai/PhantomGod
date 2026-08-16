# CLAUDE.md - Pentest-WindFtsy 工作规则

## 当前主流程

本工作目录以 `.claude/skills/pentest-windftsy` 作为唯一主控 Skill。所有 Web/SRC 安全评估、攻击面测绘、代理取证、门禁校验、漏洞登记和报告生成，均优先使用该 Skill 内的 `scripts/` 与 `references/`。

不要再把根目录旧脚本当成主门禁或主流程。根目录 `knowledge/` 只作为按需参考，不能覆盖 Skill 内的 registry/config/tooling。

## 正式路径

- 主 Skill：`.claude/skills/pentest-windftsy`
- 主脚本：`.claude/skills/pentest-windftsy/scripts`
- 主规则源：`.claude/skills/pentest-windftsy/references`
- 数据根：`pentest-data/{project-id}`
- 代理日志：`pentest-data/{project-id}/proxy-logs`
- 侦察台账：`pentest-data/{project-id}/recon-ledger.jsonl`

## 规则源

- 漏洞检查点：`references/coverage-registry.json`
- 厂商 SRC 策略：`references/src-policies/*.json`
- 国内 SRC 赏金手册：`references/src-cn-bounty-manual.md`
- 敏感信息规则：`references/secret-rules.yaml`
- 数据结构：`references/data-schemas.md`
- 质量门禁说明：`references/quality-gates.md`
- 漏洞链升级映射：`references/chain-map.md`

根目录 `knowledge/test-checkpoints.md`、`knowledge/payloads/`、`knowledge/dicts/`、`knowledge/vulns/` 仅在需要补充背景、payload 或字典时读取。若发现长期有用的规则，应收敛进 Skill 的 registry/config，而不是在对话里重复粘贴。

## 标准流程

1. 初始化项目
   `python .claude\skills\pentest-windftsy\scripts\init_project.py --target <url> --mode <src|enterprise> --policy-profile <profile>`

2. 补齐 `pentest-data/{project-id}/config.json`
   写入 scope、exclude、测试账号、角色、限制、频率、目标说明和工作守则。

3. 环境预检
   `python .claude\skills\pentest-windftsy\scripts\doctor.py --project <id> --json`

4. 启动代理并检查健康
   `python .claude\skills\pentest-windftsy\scripts\proxy\start.py --config pentest-data\{id}\config.json --log-dir pentest-data\{id}\proxy-logs`
   `python .claude\skills\pentest-windftsy\scripts\check_proxy_health.py --project <id> --json`

5. 侦察与台账
   `python .claude\skills\pentest-windftsy\scripts\recon-pipeline.py --domain <domain> --project-id <id> --data-root pentest-data`
   默认做泛解析检测+过滤；主动枚举加 `--active-recon`，字典爆破加 `--brute`（可追加 `--full-dict`），爆破受 `config.json.max_requests_per_second` 限速。

6. 广度建模门禁
   `python .claude\skills\pentest-windftsy\scripts\check_breadth.py --project <id>`

7. 漏洞挖掘门禁
   `python .claude\skills\pentest-windftsy\scripts\check_vuln_mining.py --project <id>`

8. 威胁收敛门禁
   `python .claude\skills\pentest-windftsy\scripts\check_threat_convergence.py --project <id>`

9. 漏洞登记
   `python .claude\skills\pentest-windftsy\scripts\register_report.py --project <id> ...`

10. 报告生成
   草稿：`python .claude\skills\pentest-windftsy\scripts\build_report.py --project <id> --draft`
   正式：`python .claude\skills\pentest-windftsy\scripts\build_report.py --project <id> --final`

`--final` 是正式报告唯一放行入口。它必须校验三道门禁、SRC policy、SRC submit 的 impact_verified。不要用 `scripts/check_coverage.py` 或 `verify_poc.sh` 替代新版 final 门禁。

## 工作边界

- 只在用户授权范围、用户提供代码、本地靶场、CTF、内部系统、客户授权评估、防御研究和 AI/LLM 安全评估上下文内工作。
- 真实公网或第三方目标授权不明确时，先确认 scope、账号、频率和禁止操作。
- 默认优先低风险验证、源码分析、只读证据、最小请求量和测试账号。
- 不做自动提交报告，不做高并发扫描，不做破坏性操作，不批量读取真实用户数据。
- 发现凭据、AK/SK、token 时直接记录最小证据并停止深入利用。

## 证据原则

- 没有落盘就视为没发生。
- 所有结论必须能追溯到文件、请求、响应、日志、门禁输出或报告记录。
- 代理、Playwright、curl、Python 探测都必须尽量走同一个代理口径。
- 范围、排除、频率和工作守则以 `config.json` 为单一事实源。

## SRC 模式

SRC 模式必须设置有效 `policy_profile`。厂商规则来自 `references/src-policies/*.json`，只做提交前过滤建议，最终仍以用户当时提供或确认的厂商公告为准。

新增详细规则源：`references/src-cn-bounty-manual.md`。当 `config.json.mode=src` 时，主流程和子代理必须把它作为国内 SRC 赏金场景的评分、筛选和报告参考，重点使用以下内容：

- `IMPACT FIRST`：优先验证真实业务影响；无实际危害证明的内容不进入正式提交候选。
- 资产分级：关键业务、核心业务、一般业务、边缘业务会影响最终风险系数。
- 国内五档评级：严重、高危、中危、低危、无影响；评级必须结合资产重要性和实际影响。
- 高价值攻击面：认证/账号、SSRF、数据接口、支付/资金、文件操作、权限控制、云/容器、反序列化/模板、前端高流量 XSS。
- Do NOT 红线：不做高并发扫描、内网横向、批量读取真实数据、未报备 shell/容器逃逸/改密/删改数据、社工钓鱼、DoS/DDoS、公开披露等。
- Do NOT Report：Self-XSS、无敏感操作 CSRF、无链 CORS/Open Redirect、不可利用内网 IP 泄露、无实际利用第三方 CVE、版本号泄露、邮箱轰炸等默认不作为正式提交。
- 降级因素：需要用户交互、利用条件苛刻、影响范围小、同源多漏洞、只能理论利用、无法稳定复现、非真实业务数据等必须主动降级或转为 `hold/not_reportable`。
- 敏感数据分级和数量阈值：按手册区分极度敏感、敏感信息、业务敏感数据、非敏感信息，并记录最小证明证据。

`src_disposition` 只允许：

- `submit`
- `chain_only`
- `hold`
- `not_reportable`

最终报告只纳入符合策略的 `submit`。`chain_only`、`hold`、`not_reportable` 不进入正式漏洞详情。

若 `src-cn-bounty-manual.md`、厂商 `src-policies/*.json`、用户当次工作守则存在冲突，按更严格者执行；厂商公告和用户明确授权边界优先于通用手册。

## 可选参考

- 根目录 `knowledge/`：旧知识库、payload、字典、漏洞库，按需读取。
- `.claude/skills/s-*`：专项漏洞 Skill，按漏洞类型读取。
- `scripts/cvss31-calculator.js` 已吸收到 Skill 内，可在 enterprise/国外平台报告中按需使用。

不要把旧知识库内容大段复制进提示词。需要长期复用的内容，应迁入 `pentest-windftsy/references/` 或脚本配置。
