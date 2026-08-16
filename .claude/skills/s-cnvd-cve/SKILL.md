---
name: s-cnvd-cve
description: CNVD/CVE Application and Reporting skill. Covers CNVD submission process, CVE request workflow, vulnerability report writing standards, disclosure timeline management, and platform comparison (CNVD vs CVE vs CNNVD).
---

# CNVD / CVE 申报流程

## When To Use

Use for submitting vulnerabilities to CNVD (国家信息安全漏洞共享平台), requesting CVE IDs from MITRE, managing coordinated disclosure timelines, and choosing the right platform for different vulnerability types.

## Source Priority

| Task Type | Primary Source |
|---|---|
| Methodology | (self-contained) |
| Execution | (self-contained) |
| Resources | (self-contained) |

## Source Strategy

This is a standalone skill for the administrative side of vulnerability disclosure. The technical side is covered by `s-cve-reproduction` and the other `s-*` vulnerability skills.

## References

See `references/SOURCES.md`.

---

## Part 1: CNVD 申报

### 什么是 CNVD
国家信息安全漏洞共享平台 (China National Vulnerability Database)，由 CNCERT/CC 运营。收录国内厂商和产品的安全漏洞。

### 申报流程

1. **注册账号**: https://www.cnvd.org.cn/ → 注册并完成实名认证
2. **提交漏洞**: "漏洞提交" → 填写表单
3. **审核流程**:
   - 初审: CNVD 工作人员验证漏洞存在性（1-5 个工作日）
   - 归档: 确认后分配 CNVD-ID（格式：CNVD-YYYY-NNNNN）
   - 通知厂商: CNVD 通知受影响厂商修复
   - 公开: 厂商修复后或 30 天后公开

### CNVD 提交表单要素

| 字段 | 说明 |
|------|------|
| 漏洞名称 | `[厂商] [产品] [漏洞类型] 漏洞` |
| 漏洞类型 | 从 CNVD 分类中选择（SQL注入/XSS/文件上传/RCE...） |
| 危害等级 | 高/中/低（参考 CNVD 评级标准） |
| 影响版本 | 精确版本号 + 版本范围 |
| 漏洞描述 | 简要描述漏洞原理和危害 |
| 漏洞证明 | 复现步骤 + 截图 + PoC 代码 |
| 修复建议 | 代码级修复方案 |
| 参考链接 | 厂商公告/CVE 链接/原始报告 |

### CNVD 评级标准

| 等级 | 标准 |
|------|------|
| **高危** | 直接获取系统权限、核心敏感信息泄露、核心业务拒绝服务 |
| **中危** | 普通信息泄露、需交互的 XSS、需特定条件的漏洞 |
| **低危** | 轻微信息泄露、local DoS、条件苛刻的漏洞 |

### CNVD vs CNNVD 区别

| | CNVD | CNNVD |
|---|------|-------|
| 运营方 | CNCERT/CC | 中国信息安全测评中心 |
| 收录范围 | 偏重国内厂商 | 偏重国际 CVE 翻译 |
| 影响力 | 国家漏洞库主渠道 | 侧重安全研究和预警 |
| 提交入口 | cnvd.org.cn | cnnvd.org.cn |

---

## Part 2: CVE 申报

### 什么是 CVE
Common Vulnerabilities and Exposures，由 MITRE 维护的全球漏洞标识符标准。

### CVE 申请流程

**方法一：通过 GitHub Security Advisory（推荐，最快）**
1. 在 GitHub 仓库 → Security → "Report a vulnerability"
2. 或 → Advisories → "New draft security advisory"
3. 填写漏洞描述 → 提交
4. GitHub 审核 → 自动请求 CVE ID
5. CVE ID 通常在 24-72 小时内分配

**方法二：通过 CVE Numbering Authority (CNA)**
1. 确定漏洞属于哪个 CNA 的范围（如 Microsoft、Google、Apache 等有自己的 CNA）
2. 联系相应 CNA 或 MITRE 直接提交
3. 提交到 https://cveform.mitre.org/

**方法三：通过 HackerOne / Bugcrowd**
1. 如果目标有 HackerOne/Bugcrowd 项目，通过平台提交
2. 平台会协助 CVE 申请

### CVE 提交要素

| 字段 | 说明 |
|------|------|
| Vulnerability Type | CWE ID（如 CWE-89 SQL Injection） |
| Root Cause | 简要描述根因 |
| Affected Versions | 精确版本范围 |
| Attack Vector | 网络/本地/物理 |
| Attack Complexity | 低/高 |
| Privileges Required | 无/低/高 |
| User Interaction | 无/需要 |
| Impact (CIA) | Confidentiality/Integrity/Availability 各评分 |

### CVE 时间线管理

```
Day 0:    发现漏洞 + 确认
Day 1-7:  联系厂商/维护者（私下）
Day 7-14: 厂商确认 + 制定修复计划
Day 30:   预期补丁完成
Day 30-90: CVE 公开发布
Day 90+:  超过 90 天未修复 → 可考虑公开（遵循披露政策）
```

---

## Part 3: 平台选择决策树

```
发现漏洞
├─ 开源项目？
│   ├─ 是 → GitHub Security Advisory → CVE
│   └─ 否 → 继续
├─ 国内厂商产品？
│   ├─ 是 → CNVD 提交（优先）
│   └─ 否 → 继续
├─ 国际厂商产品？
│   ├─ 有 H1/Bugcrowd 项目？ → 平台提交
│   ├─ 有自己 CNA？ → 联系厂商 CNA
│   └─ 无 CNA → MITRE 直接提交
├─ 云服务/AI 产品？
│   └─ CNVD + CVE 同时提交（双披露）
└─ 移动 APP？
    └─ CNVD（Android/iOS 底层用 CVE）
```

---

## Part 4: 报告模板（通用高质量报告）

```markdown
## 漏洞概述
- 厂商:
- 产品/版本:
- 漏洞类型: (CWE-xxx)
- 危害等级: 高/中/低
- CVE ID: (如有)

## 漏洞根因
(一两句话描述根因)

## 复现环境
- OS/版本:
- 软件版本:
- 配置:

## 复现步骤
1.
2.
3.

## 危害证明
(截图 + PoC + 影响说明)
最大危害: (RCE/任意文件读取/账号接管/...)

## 修复建议
(代码级具体修复方案)

## 附录
- 参考链接:
- 披露时间线:
```

## Important Agent Rules

- ⛔ CNVD/CVE 提交前确保漏洞信息准确 — 错误报告浪费审核资源
- ⛔ 不得重复提交已知 CVE — 提交前查重
- ⛔ 遵守各平台披露政策 — 不得在厂商修复前公开
- 国内 SRC 漏洞一般不需要额外提交 CNVD（厂商自己处理），第三方组件漏洞才走 CNVD/CVE
