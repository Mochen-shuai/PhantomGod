# Pentest-WindFtsy

> 一套面向 **WEB 应用安全评估 / 威胁建模** 的 Claude Code 技能包：把「全面测绘攻击面 → 建模并验证权限矩阵 → 逐 URL 逐参数挖掘漏洞 → 收敛威胁并专项绕过 → 产出附真实证据、经质量门禁审核的漏洞报告」固化为**数据驱动、可断点续跑、有质量门禁**的标准流程。

技能通过一个**记录型 HTTP/HTTPS 代理**把流经的所有请求按完整 URL 分类落盘，用于接口与参数清点；配套两个子代理分别负责**漏洞挖掘**与**专项绕过**，并由主技能统一调度、对账收敛。

**目前的应用效果**：
- 天积安全靶场综合商城系统测试使用GLM5.2可以稳定达到4000+，可以挖到24-27个漏洞（单次对话）。
- 企业内某新开发项目（未经安全测试，中小规模系统，约200个接口）发现120+中高危漏洞（纯黑盒测试），涉及越权访问（未授权、IDOR、垂直越权等）、SQL注入、XSS、文件上传、敏感信息泄露等，误报率小于10%。
- 企业内某项目（中小规模系统，约200个系统，经过多轮安全扫描、渗透测试和开源工具代码审计），发现24中高危漏洞（提供源码参考），19个有效（其中2个误报是测试环境特殊配置导致的），涉及越权删除、金额篡改、流程篡改、敏感信息泄露等。

总体来说在企业内部安全测试的场景还是比较好用，但是也有很多坑，比如消耗的token和时间比较多（说实话非常多，目测挖SRC会亏本……）、子代理并发架构对人机交互的处理不太好、过滤绕过机制不稳定、cheklist和重点测试清单合理性存疑等等，还需要逐步优化，也欢迎各位师傅提供建议。

在模型适配方面，目前来看水平不低于GLM5.2的模型都能很好的适配，比如grok4.5。低于GLM5.2水平的模型，如目前deepseekV4预览版效果就要差很多，不知道正式版效果如何。

---

## 项目组成

本项目实际内容包括 `.mcp.json` 与 `.claude/` 下的技能和子代理，**下载解压到任意目录即可作为 Claude Code 的工作目录使用**：

```
<你的工作目录>/
├── CLAUDE.md                        # 工作规则、标准流程、SRC 边界（主流程唯一入口）
├── .mcp.json                        # playwright-proxy + cheatengine MCP 配置
├── knowledge/                       # 字典 / payload / 漏洞库（按需参考）
└── .claude/
    ├── agents/                      # 配套子代理
    │   ├── pentest-vuln-miner.md    #   漏洞挖掘子代理（逐 URL 逐参数挖掘，产出漏洞矩阵与报告）
    │   └── pentest-bypass-miner.md  #   专项绕过子代理（对被防护信号穷尽多族绕过）
    ├── hooks/                       # 会话钩子（安全上下文注入、工具前后置处理）
    ├── rules/                       # 通用规则（安全研究背景）
    └── skills/
        ├── pentest-windftsy/        # 主技能（攻击面测绘 → 威胁建模 → 漏洞挖掘 → 收敛 → 报告）
        │   ├── SKILL.md             #   技能主流程与工作规范
        │   ├── references/          #   阶段规范、数据结构、质量门禁、SRC 策略、漏洞链等
        │   ├── scripts/             #   数据处理与质量门禁脚本（Python）
        │   │   └── proxy/           #   记录型 HTTP/HTTPS 代理（基于 mitmproxy）
        │   └── assets/templates/    #   项目配置模板
        └── s-*/                     # 45 个专项漏洞技能，按漏洞类型按需读取
                                     #   （SQLi / XSS / SSRF / 反序列化 / LLM 安全 / web3 / 移动端…）
```

> 运行产生的项目数据默认落在工作目录下的 `pentest-data/{project-id}/`（本仓库不含示例数据）。
>
> 本地另有 `.claude/security-sources/`（AboutSecurity / hack-skills 第三方资源）、`tools/`、`agent-security-skill-hub/`，均为第三方或独立 git 仓库，不随本仓库分发（见 `.gitignore`）。

---

## 环境要求

| 依赖 | 说明 |
|------|------|
| **Claude Code** | 技能与子代理的运行环境 |
| **Python 3.x** | 数据处理、质量门禁脚本与代理（开发环境为 Python 3.14） |
| **mitmproxy** | 记录型代理依赖，见 `proxy/requirements.txt`（`mitmproxy==12.2.3`） |
| **python-docx** | 报告阶段生成 DOCX 交付版依赖，见 `proxy/requirements.txt`（`python-docx==1.1.2`） |
| **Node.js / npx** | 运行 `@playwright/mcp`（由 `.mcp.json` 自动拉起） |
| **操作系统** | 面向 **Windows**（命令示例使用 PowerShell 与反斜杠路径） |

---

## 安装与启用

1. **下载解压**：将本仓库下载并解压到任意目录，把该目录作为 Claude Code 的工作目录（项目根）。
2. 安装python3环境，可以手动安装也可以让AI agent安装。
3. **安装 Python 依赖（代理 + 报告渲染）**（默认源会比较卡，考虑换源或开梯子）：

   ```powershell
   python -m pip install -r .claude\skills\pentest-windftsy\scripts\proxy\requirements.txt
   ```

   > 一条命令装齐全流程依赖：`mitmproxy`（记录型代理）+ `python-docx`（报告阶段渲染 DOCX 交付版）。

---

## 代理与 MCP 说明

技能的接口/参数清点依赖一条本地记录型代理，浏览器流量经它抓取并按 URL 落盘：
- **代理服务器**：技能准备阶段会自动启动代理服务器， （`scripts/proxy/start.py`，基于 mitmproxy）：默认监听 `127.0.0.1:24304`，解密 HTTPS 后把所有请求按**完整 URL**分类落盘（清单 / 原始报文 / 参数详情），支持范围/排除过滤与断点续跑。代理首次启动会在 `%USERPROFILE%\.mitmproxy\` 生成 CA 证书 `mitmproxy-ca-cert.pem`（用于解密 HTTPS）。
- **playwright MCP（）**：在该工作目录启动 Claude Code，`.mcp.json` 会自动注册 `playwright-proxy` MCP（首次运行 `npx` 会自动拉取 `@playwright/mcp`），该MCP已默认配置代理服务器地址，启动的浏览器通过 `--proxy-server http://127.0.0.1:24304` 把流量导入上述代理；`--isolated` 表示**浏览器数据不落盘**（无持久化用户目录），`--ignore-https-errors` 用于接受代理的 MITM 证书。

> **端口一致性**：代理端口默认 `24304`，实际以项目 `config.json` 的 `proxy_port` 为准（代理与广度门禁同源读取）。若调整端口，需同步修改 `.mcp.json` 中的 `--proxy-server`。

---

## 基础调用方式（仅供测试功能，不推荐实际使用）

在上述工作目录启动 Claude Code 后，使用 `pentest-windftsy` + 目标URL即可触发技能运行，例如：

> 目标： `http://target.example.com/` 

主技能会按阶段推进：

1. **准备**：初始化项目目录与配置，后台启动记录代理。
2. **攻击面测绘（广度）**：全面访问业务流程与接口，测绘攻击面，验证权限矩阵，经广度门禁。
3. **漏洞挖掘**：调度 `pentest-vuln-miner` 子代理逐 URL 逐参数挖掘，产出参数漏洞矩阵与漏洞报告，经挖掘门禁。
4. **威胁收敛**：对账未消账威胁，对被防护信号调度 `pentest-bypass-miner` 子代理专项绕过，经收敛门禁。
5. **报告产出**：汇总生成附真实请求/响应证据的漏洞报告清单（Markdown / HTML / DOCX）。

所有产物落在工作目录的 `pentest-data/{project-id}/` 下。各阶段的详细规范见 `.claude/skills/pentest-windftsy/references/`。

---
## 推荐的调用方式

在实际使用中建议在任务下发时根据需要明确项目ID、测试账号、安全边界、测试范围等信息，获取更好的测试结果。相关信息直接以自然语言提供即可，skill会自动处理并写入配置文件，对于特别重要的信息可以放在`# 工作守则` 之后，该标签之后的内容会被原样写入配置文件并作为最高优先级的要求，避免AI提炼错误。
参考示例：
- 示例一
  ```markdown
  目标：http://localhost:8080/range/pentest/shop/
  项目id：HeaSecShop
  测试规则：
      1. 这是一个用于测试的环境，允许执行任何数据修改操作
      2. 可以使用靶场的重置功能重置靶场数据，重置功能本身不在漏洞挖掘范围内
      3. 允许访问靶场自带的短信模拟器获取短信验证码（使用方式见range/common/components/sms-simulator/api-doc.php），但不要挖掘短信模拟器本身接口的漏洞（不挖range/common/components/sms-simulator/路径下的漏洞）。

  测试账号：
  管理员	heasecadmin	heasec@123
  用户	maijia1	user@123  手机号15900001111 天积宝支付密码886688
  用户	maijia2	user@123  手机号15900002222 天积宝支付密码998899
  商户	shanghu1	shop@123  手机号13300001111
  商户	shanghu2	shop@123  手机号13300002222

  # 工作守则
  1. 本次测试完全独立开展，不继续之前的测试项目，不读取任何历史测试结果包括记忆信息。
  2. 要求进行纯黑盒测试，禁止使用任何形式读取服务端源码  
  3. 不允许访问range/pentest/shop/vuln.php
  ```
- 示例二
  ```markdown
  目标：https://www.heasec.com/
  安全等级：高
  测试规则：
      1. 这是一个经过授权的SRC项目，请重点关注SRC常见收录的漏洞类型，避免挖掘CORS、CSRF、请求头缺失等SRC不收录的漏洞。
      2. 如果遇到短信验证码验证或其他人机无法绕过交互机制，应暂停测试，提示用户进行人工干预。
  测试账号：heasec/heasec@123

  # 工作守则
  请严格遵守SRC公告要求：
  【粘贴具体的SRC规范要求】
  ```

**说明**：
- **项目ID**：默认会基于目标URL提取，同个项目多次测试可以手工指定项目ID避免冲突。如果项目意外中断也可以使用技能指定项目ID继续测试，技能会基于当前落盘的文件状态实现断点续测。
- **测试目标**：默认取最严格的路径，如`http://localhost:8080/range/pentest/shop/`只会测试`/range/pentest/shop/`路径下的漏洞，要调整的话可以具体说明，可以扩大或排除指定路径。
- **安全等级**：默认的安全边界，内置高中低三级，如果不提供默认为`高`。
  - `high`：影响范围限于测试账号；不删除已有数据；禁止影响资金或其它不可回退操作。（真实生产环境）
  - `medium`：影响范围限于测试账号（含测试中注册的账号），可对其增删改/办理业务；其它账号仅读。（生产中的测试账号）
  - `low`：可对测试环境数据任意增删改查。（测试环境）
- **灰盒测试**：对于企业内部进行安全测试的场景，如果能获取源代码的情况下可以将源代码放到工作目录作为参考效果会有很大提升，参考提示词加一条`项目源码在src/heasec/目录下，可以按需读取，但以黑盒测试结果为准`

---

## 可调整的参数

任务下发时的**自然语言参数**（项目 ID、测试账号、安全边界、测试范围、`# 工作守则` 等）见上文「推荐的调用方式」，由 skill 自动处理并写入配置文件。下面是更底层的**配置字段与命令行参数**，一般无需手动干预，特殊需求时可自行调整。

### `config.json` 关键字段（项目级配置，落在 `pentest-data/{project-id}/config.json`）

准备阶段由 skill 依自然语言下发自动写入，也可手工编辑后续阶段读取的这份「单一事实源」。

| 字段 | 说明 |
|------|------|
| `scope` | 允许**安全测试**的范围（注意区别于「允许访问」）；未指定则默认取目标路径下全部。语法（纯域名 / 路径前缀 / 正则）见 `scripts/proxy/README.md` |
| `exclude` | 范围内需**排除**的 URL（允许访问但不测试、或高风险端点如注销）；语法同 `scope`，优先级高于 `scope` |
| `scope_regex` / `exclude_regex` | 是否把 `scope`/`exclude` 各条按**正则**解释（对完整 URL 做 search），默认 `false`（字面匹配） |
| `test_accounts` | 测试账号数组（`role` / `username` / `password` / `login_url`），供建立会话池与权限矩阵验证 |
| `security_level` | 安全等级 `high` / `medium` / `low`（默认 `high`），控制可执行操作的破坏性边界（详见上文「安全等级」） |
| `work_guidelines` | 工作守则，`# 工作守则` 标记后的内容**原样写入**，**全程最高优先级**，各阶段与子代理严格遵守 |
| `goals` / `constraints` | 目标成果 / 约束条件（自然语言，供各阶段参考） |
| `proxy_port` | 记录型代理监听端口（默认 `24304`）；与广度门禁同源读取，改动需同步 `.mcp.json` 的 `--proxy-server` |

### `init_project.py` 参数（准备阶段初始化项目）

`python .claude\skills\pentest-windftsy\scripts\init_project.py --target <url> [选项]`

| 参数 | 默认 | 说明 |
|------|------|------|
| `--target` | 必填 | 目标根地址，如 `http://www.heasec.com:8080/`；据此推导 project-id |
| `--project` | 由 target 推导 | 手动指定 project-id（多次测试同目标、或断点续测时用） |
| `--security-level` | `high` | 安全等级 `high` / `medium` / `low` |
| `--proxy-port` | `24304` | 代理端口，写入 `config.proxy_port` |
| `--data-root` | `pentest-data` | 数据根目录 |

### 记录型代理 `proxy/start.py` 参数（全程抓包）

推荐用 `--config` 直接读项目 `config.json`（scope/exclude/proxy_port 与门禁同源，避免漂移）。常用参数：

| 参数 | 默认 | 说明 |
|------|------|------|
| `--config` | 无 | 从 `config.json` 读 `scope`/`exclude`/`proxy_port`（与 `--scope`/`--exclude` 互斥，**推荐**） |
| `--port` | `24304` | 监听端口 |
| `--log-dir` | `<项目>/proxy-logs` | 日志目录 |
| `--target-hosts` | 空（全部） | 逗号分隔的目标主机过滤（子串匹配），滤掉浏览器后台噪声 |
| `--scope` / `--exclude` | 空 | 临时抓包时的范围 / 排除规则（不走 config 时用） |
| `--body-cap` | `1048576` | 原始请求 body 落盘截断字节数（0=不限） |
| `--param-value-cap` | `100` | 参数样本值最大字符数 |
| `--resp-preview-cap` | `200` | 响应体预览落盘字节数（0=关闭） |

> 完整参数与范围/排除语法见 [`scripts/proxy/README.md`](.claude/skills/pentest-windftsy/scripts/proxy/README.md)。报告阶段结束后可用 `proxy/stop.py --config pentest-data\{id}\config.json` 停止代理、释放端口。

---

## 输出产物

运行产物统一落在工作目录的 `pentest-data/{project-id}/` 下（可加入 `.gitignore` 避免凭据外泄）：

```
pentest-data/
├── index.json                                  项目清单（根级）
└── {project-id}/
    ├── config.json  state.json  sessions.json
    ├── pages.jsonl  js.jsonl  business-chains.jsonl  threats.jsonl
    ├── url-inventory.json  mining-scope.json  url-static-params.json  retest-list.json  bypass-list.json  vuln-reports.json
    ├── pages-html/{PAGExxxx}.html   js-files/   permission-matrix/{URLxxxxx}.json
    ├── reports/{vuln_id}.md   vuln-matrix/{URLxxxxx}.json   url-context/{URLxxxxx}.json
    ├── report/{id}-report-{YYYYMMDD}.{md,html,docx}   汇总评估报告（报告阶段产出）
    ├── proxy-logs/  (url_index.jsonl / requests/ / params/ …)
    └── tmp/                                         过程临时脚本 / payload / 中间产物
```

主要产物：

| 分组 | 产物 | 内容 |
|------|------|------|
| 配置 / 状态 | `config.json` / `state.json` / `sessions.json` | 项目配置 / 各阶段与质量门禁退出态 / 各角色会话池（含 unauthenticated 基线） |
| 攻击面清单 | `pages.jsonl` / `js.jsonl` / `business-chains.jsonl` | 页面（含渲染后 HTML、可交互元素、约束）/ JS（含密钥、隐藏接口）/ 业务链走通情况 |
| 攻击面清单 | `threats.jsonl` / `url-inventory.json` / `permission-matrix/` | 威胁清单（含消账态）/ URL 与参数总清单 / 多角色权限矩阵（越权判定） |
| 挖掘产出 | `vuln-matrix/{URLID}.json` / `mining-scope.json` | 逐 URL 逐参数漏洞矩阵（含防护探测、测试要点应答）/ 必挖清单基线 |
| 挖掘产出 | `reports/{vuln_id}.md` / `vuln-reports.json` / `bypass-list.json` | 逐份漏洞报告（附真实请求/响应证据）/ 报告登记与验收态 / 被防护绕过台账 |
| 代理日志 | `proxy-logs/` | `url_index.jsonl`（URL 清单）+ `requests/`（原始报文）+ `params/`（参数详情），接口与参数清点数据源 |
| 最终报告 | `report/{id}-report-{YYYYMMDD}.{md,html,docx}` | 完整评估报告，三种格式内容一致（Markdown 源 / HTML 存档查看 / DOCX 正式交付） |

**评估报告章节**：封面（目标 / 范围 / 安全等级 / 漏洞统计）→ 测试概述 → 测试账号与角色 → 攻击面测绘概览 → 漏洞统计概览 → 漏洞详情（仅审核通过项，按危害降序嵌入正文）→ 威胁收敛结论 → 被防护与残余缺口 → 修复建议汇总 → 质量门禁退出态附录。

---

## 免责声明

本项目仅用于**已获合法授权**的安全测试、安全研究与教育用途。使用者须自行确保对目标系统拥有明确授权，并遵守适用的法律法规。因未授权或不当使用造成的任何后果，由使用者自行承担。

---

## 许可证

本项目以 [GNU General Public License v3.0](LICENSE) 开源。
