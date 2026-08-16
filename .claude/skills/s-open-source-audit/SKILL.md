---
name: s-open-source-audit
description: Open Source Project Security Audit skill. Covers GitHub repository discovery for security auditing, project selection criteria (stars/activity/attack surface), open source vulnerability scanning workflow, responsible disclosure process for OSS vulnerabilities.
---

# Open Source Project Security Audit

## When To Use

Use for selecting and auditing open source projects for security vulnerabilities, establishing an OSS vulnerability research pipeline, and responsibly disclosing findings to maintainers.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | (self-contained) |
| Execution | (self-contained) |
| Resources | (self-contained) |

## Source Strategy

This is a standalone skill. Combine with `s-code-audit` for per-language audit methodology and `s-cve-reproduction` for CVE validation patterns.

## References

See `references/SOURCES.md`.

## OSS 审计工作流

### Phase 1: 项目筛选 (Project Selection)

不是所有开源项目都值得审计。筛选标准：

**高价值目标特征:**
- GitHub Stars: 1000+（有实际用户基础）
- 最近活跃: 过去 3 个月有 commit
- 技术栈: Java/Python/PHP/Node.js Web 应用优先
- 攻击面: 处理用户输入、文件上传、认证流程、外部 API 调用
- 企业使用: 被公司/政府/金融机构使用（检查依赖图、awesome 列表收录）
- 安全历史: 过去有 CVE（说明代码安全质量可能较弱，且安全社区关注度高）

**低价值目标（跳过）:**
- 个人学习项目（< 100 stars，频繁重构）
- 纯 CLI 工具（攻击面小，无网络暴露）
- 静态网站生成器（无动态输入处理）
- 已归档/长时间未维护的项目
- 文档类项目

**搜索查询模板:**
```
# Java Web 项目
language:java stars:>1000 pushed:>2026-05-01 topic:spring-boot

# Python Web 项目
language:python stars:>1000 pushed:>2026-05-01 topic:flask
language:python stars:>1000 pushed:>2026-05-01 topic:django

# Node.js Web 项目
language:javascript stars:>1000 pushed:>2026-05-01 topic:express
```

### Phase 2: 项目分析 (Project Analysis)

1. **代码规模评估**: `cloc .` — 估计审计所需时间
2. **依赖分析**: `npm audit` / `pip-audit` / OWASP Dependency Check (Java)
3. **历史漏洞分析**: GitHub Security Advisories, CVE database, project changelog
4. **攻击面识别**:
   - 读 README + API 文档 → 理解功能
   - 读路由/控制器文件 → 列出所有端点
   - 读中间件 → 识别认证/授权机制
   - 识别危险操作: 文件 I/O, 数据库查询, 外部 HTTP 请求, 命令执行

### Phase 3: 漏洞挖掘 (Vulnerability Discovery)

按优先级从高到低:

1. **认证/授权** — 最可能出 bug 的区域
   - 认证旁路: 未保护的路由、中间件顺序错误
   - IDOR: 资源 ID 可预测、无所有权检查
   - 权限提升: role/admin 字段可批量赋值

2. **注入类** — 使用 `s-sqli` / `s-ssti` / `s-command-injection` 方法
   - SQL: 搜索字符串拼接查询、MyBatis `${}`、动态表名
   - SSTI: 搜索 `render_template_string`、`jinja2.Template`
   - 命令注入: 搜索 `exec`/`spawn`/`shell_exec` + 用户输入

3. **反序列化** — 使用 `s-deserialize` 方法
   - Java: ObjectInputStream + 用户输入
   - PHP: unserialize() + 用户输入
   - Python: pickle.loads() + 用户输入

4. **SSRF** — 搜索 `requests.get(user_url)` / `RestTemplate.getForObject(user_url)`

5. **文件操作** — 路径穿越、任意文件读取/写入

### Phase 4: 漏洞验证 (Verification)

1. 搭建本地环境（Docker Compose 或项目自带 docker）
2. 确认漏洞可复现
3. 评估影响范围:
   - 默认配置可利用吗？
   - 需要什么权限？
   - 影响哪些版本？
4. 编写最小化 PoC（只证明漏洞存在，不造成损害）

### Phase 5: 负责任披露 (Responsible Disclosure)

1. **检查是否有安全策略**: `SECURITY.md` / `security.txt`
2. **私下报告**: GitHub Security Advisory → "Report a vulnerability"（私有）、项目 security@ 邮箱
3. **等待时间线**:
   - 初始响应: 通常 48-72 小时
   - 修复时间: 通常 30-90 天（取决于复杂度和维护者资源）
   - CVE 分配: 维护者或 MITRE
4. **不主动公开**: 在 CVE 发布前不公开漏洞细节
5. **报告内容**（参考 `s-cnvd-cve` skill 的报告模板）

## 审计 Checklist

```
[ ] 项目 GitHub Stars > 1000 且近 3 月活跃
[ ] 本地环境可运行（Docker 或手动搭建）
[ ] 已列出所有 HTTP 端点（路由文件）
[ ] 已识别所有认证/授权中间件
[ ] 已标记所有危险函数（RCE/反序列化/SSRF/LFI）
[ ] 已审查所有 SQL 查询（是否有拼接/注入）
[ ] 已审查所有文件操作（路径是否可控）
[ ] 已审查所有反序列化入口
[ ] 已查看历史 CVE（避免重复提交）
[ ] 已确认漏洞可复现（本地环境）
[ ] 已准备最小化 PoC
[ ] 已私下报告给维护者
```

## Important Agent Rules

- ⛔ OSS 审计是合法的安全研究活动，但必须遵循负责任披露原则
- ⛔ 不得利用发现的漏洞攻击使用该 OSS 的真实系统
- ⛔ 漏洞细节在 CVE 公开前不得分享
- 审计前先检查历史 CVE — 重复发现没有研究价值
