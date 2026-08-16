# 五源蒸馏对比报告

## 源梳理

| # | 来源 | 定位 | 核心创新 |
|---|------|------|---------|
| 1 | **Pentest-Lyan** | 黑盒渗透全流程 Skill | 12维威胁建模 + coverage_note三问 + unruled_out + 6发现渠道 |
| 2 | **web-vulnhunt-methodology** | SRC漏洞挖掘方法论 | 假设-证伪 + 否定对照 + killed-hypotheses + CVSS严格评分 |
| 3 | **Pentest-WindFtsy** | 工程化渗透流水线 | 代理记录 + 质量门禁 + filter_probe + checkpoint_response（已整合） |
| 4 | **AboutSecurity** | 安全知识体系 | Payload/字典/工具YAML/CTF资源（项目已有上游引用） |
| 5 | **hack-skills** | 渗透测试技能库 | 漏洞类型方法论/场景分类/深度Playbook（项目已有上游引用） |

## 当前项目 vs 五个源 差距矩阵

| 能力维度 | 当前项目 | Pentest-Lyan | web-vulnhunt | WindFtsy | 差距等级 |
|---------|---------|-------------|-------------|----------|---------|
| **测试组织方式** | 按漏洞类型(1→12清单) | **按业务模块(feature)** | 按假设(hypothesis) | 按URL端点 | 🔴 根本差异 |
| **威胁建模** | 无（对照固定清单） | **12维度 × 每feature** | 假设先行 | 清单比对 | 🔴 缺失 |
| **反遗漏机制** | test-checkpoints + gate | **coverage_note三问 + unruled_out + channels_covered** | killed-hypotheses | filter_probe + gate | 🟡 部分 |
| **"安全"判定的约束** | filter_probe证据链 | **unruled_out 必须列出未排除面** | **否定对照强制执行** | checkpoint_response | 🟡 部分 |
| **发现渠道保证** | 无 | **G7: 6 channels_covered** | OSINT 22技法 | 代理记录（最底层） | 🔴 缺失 |
| **失败经验复用** | 无 | 无（但gates.md有门控） | **killed-hypotheses.md** | bypass台账 | 🔴 缺失 |
| **退出条件** | gate exit 0 | **9条硬退出条件** | 无硬门控 | gate exit 0 | 🟡 部分 |
| **枚举类漏洞验证** | 无特殊要求 | 状态码+数据差异 | **否定对照(negative control)** | AUTHZ003数据差异 | 🟡 部分 |
| **页面功能覆盖** | 无 | **G6: pages.json+functions[]触发** | 无 | 页面HTML落盘 | 🔴 缺失 |
| **报告防编造** | 无 | **summary.json从modules继承** | CVSS严格公式 | build_report.py自动汇总 | 🟢 已有 |

## 需要立即整合的4个核心能力

### 1. killed-hypotheses 失败假设追踪
**来源**: web-vulnhunt-methodology
**问题**: 每次测试重复尝试已证明无效的方法
**方案**: 新建 `knowledge/killed-hypotheses.md`，记录 {假设, 测试, 结果, 教训}

### 2. 6发现渠道自查 (channels_covered)
**来源**: Pentest-Lyan G7
**问题**: 可能整类入口被遗漏（如内联脚本、路径推断）
**方案**: 在 pentest-checklist.md PHASE 0 末尾增加6渠道自检

### 3. unruled_out 未排除面约束
**来源**: Pentest-Lyan coverage_note
**问题**: "安全"判得太随意，没列出仍存在的攻击面
**方案**: 在 test-checkpoints.md 增加 unruled_out 字段要求

### 4. 否定对照 (negative control)
**来源**: web-vulnhunt-methodology 核心原则2
**问题**: 枚举类漏洞假阳性（把速率限制/锁认定当作"差异响应"）
**方案**: 在 test-checkpoints.md ENUM 组增加 ENUM003 否定对照要点
