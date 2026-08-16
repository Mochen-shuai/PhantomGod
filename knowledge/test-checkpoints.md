# 编号化测试要点规范（Test Checkpoints）

> **蒸馏自 Pentest-WindFtsy v1.0.0 的 test-checkpoints.md 与 vuln-checklist.md。**
> 每个编号要点必须在漏洞矩阵或报告中**逐条应答**，`tested_not_found`/`doubtful`/`filtered` 时不允省略。

---

## 核心机制：filter_probe（防护探测，必须先于 payload）

**所有 generic 类漏洞测试的第一步**：在正常参数值**中间**插入单一特殊字符/关键字，观察防护行为。

| 防护类型 | 现象 | 后续策略 |
|---------|------|---------|
| **放行** | 原样返回，无报错 | 该字符可直接用于构造 payload |
| **过滤** | 替换为空 | 双写绕过、等价替代 |
| **替换** | 替换为其他字符 | 分析替换规则，利用替换结果 |
| **拦截** | 触发报错/403/WAF | 编码绕过、协议混淆 |
| **转义** | 添加 `\` 或转义序列 | 利用转义打破闭合 |

**格式**：`{符号/关键字: [防护情况, 说明]}` — 结构化对象，不作自然语言描述。
**禁止**：把整条 payload 当作 key（如 `' OR 1=1--`），必须拆成 `'`、`OR`、`=`、`--` 等单一元素。

---

## 一、SQL 注入（SQL）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **SQL001** | **防护规则探测**：至少测试空白符(` `,`\t`,`\n`)、注释(`#`,`-- `,`/**/`)、关键字(`AND`,`OR`,`SELECT`,`UNION`)、符号(`'`,`"`,`(`,`)`,`%`,`;`)各3个以上，记入 filter_probe | filter_probe 为空 |
| **SQL002** | **先判闭合再构造**：识别参数拼接上下文 — 字符串型 `'...'` / 双引号 `"..."` / LIKE `%...%` / 数字型无引号 / `ORDER BY` / `IN (...)`，用不同闭合方式测试 | 未说明上下文判断依据 |
| **SQL003** | **针对过滤定制 payload**：探明空格被过滤 → 用 `/**/`、`%09`、`%0a`、括号；关键字黑名单 → 大小写、内联注释`/*!*/`、双写、等价运算符`&&`/`||`；至少3种绕过方式 | 只用一种绕过方式 |
| **SQL004** | **充分尝试各注入类型**：联合查询→报错注入→布尔盲注→时间盲注逐一尝试。**无回显时必须做盲注**，不因单一类型无果即判安全 | 未做盲注即判 `tested_not_found` |

---

## 二、XSS 跨站脚本（XSS）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **XSS001** | **黑名单绕过遍历**：遇标签/属性/事件被过滤时，遍历非黑名单标签(`svg`,`video`,`audio`,`marquee`,`details`,`a`等)、事件(`onerror`,`onload`,`ontoggle`,`onanimationstart`,`onfocus`等)、协议与编码。**不因个别标签被拦即判安全** | 只试了 `<img>` 和 `<script>` |
| **XSS002** | **闭环验证输出上下文**：确认输入落到哪个页面的哪个元素、是 `innerHTML` 还是 `textContent`。**存储型必须到实际渲染页验证执行**，跨 URL 也要验 | 只验证了输入端点，未跟踪到输出端点 |

---

## 三、命令注入（CMDI）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **CMDI001** | **探测分隔与拼接位**：在正常值中段注入 `;` `\|` `\|\|` `&&` `$()` `` ` `` `%0a`，观察是否打破命令语义 | 只测了 `;id` 一个 payload |
| **CMDI002** | **无回显做带外/时延**：`ping -c 3 127.0.0.1` / `sleep 5` / `timeout 5` 制造时延，或 DNS/HTTP 带外。确无带外通道且无时延差异才记 `doubtful` | 无回显直接判 `tested_not_found` |
| **CMDI003** | **遇过滤至少3种绕过**：命令替换、`${IFS}`/`<`/`%09`替代空格、引号拼接、Base64编码、变量拆分 | 绕过尝试少于3种 |

---

## 四、SSRF 服务端请求伪造（SSRF）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **SSRF001** | **内网/云元数据探测**：`127.0.0.1`、`10.0.0.1`、`192.168.1.1`、`169.254.169.254`，对比时延/状态码/响应内容差异 | 只测了云元数据一个地址 |
| **SSRF002** | **协议与地址混淆≥3种**：`file://`/`gopher://`/`dict://`、IP进制/十进制/`@`混淆、短域名、302重定向 | 只用了一种协议 |
| **SSRF003** | **危害闭环**：读到内网/元数据内容或触发内网请求证据；无带外与回显时以时延/报错差异佐证 | 无回显直接判 `tested_not_found` |

---

## 五、路径穿越/文件包含（PATH）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **PATH001** | **穿越序列与编码探测**：`../`、`..\`、`..%2f`、`..%252f`、`%2e%2e/`、`....//` 等中段注入，记 filter_probe | filter_probe 为空 |
| **PATH002** | **以已知文件坐实**：读到 `/etc/passwd`、`win.ini`、`/proc/self/environ` 或应用配置等越界文件内容或明确差异 | 只有路径穿越尝试，未用已知文件验证 |
| **PATH003** | **遇过滤至少3种绕过**：多重URL编码、点号变形、合法前缀+穿越、空字节/截断、绝对路径 | 绕过尝试少于3种 |

---

## 六、文件上传（UPLOAD）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **UPLOAD001** | **后缀黑名单遍历**：按目标语言遍历所有可解析后缀（PHP: `php/php3/php4/php5/php7/pht/phtml/phar/phps`）+ 大小写/双扩展/`.`截断/`%00`/多MIME/魔术字节 | 只试了 `.php` 一个后缀 |
| **UPLOAD002** | **路径穿越联动**：脚本上传成功但当前目录不解析时，尝试用路径穿越写到可解析目录，或改写解析规则文件如 `.htaccess` | 上传成功后未进一步尝试 |

---

## 七、越权/未授权（AUTHZ）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **AUTHZ001** | **越权前正向确认会话**：测试前先用该会话成功访问"本角色专属且需登录"的页面并拿到本人数据，确认会话有效。**防会话失效/未登录导致的假阴性** | 未确认会话有效性 |
| **AUTHZ002** | **完整跟踪302再判权限**：遇3xx**禁止直接判"已拦截"**。跟踪到最终页面：落到登录页=拦截；落到目标数据=越权成立 | 看到302就直接写"有权限保护" |
| **AUTHZ003** | **以服务端数据差异坐实**：越权成立须以读到/改到他人的真实数据为证。**不能仅根据状态码不同判定** | 只用状态码差异做结论 |

---

## 八、用户枚举（ENUM）

| 编号 | 测试要点 |
|------|---------|
| **ENUM001** | **校验状态码一致性**：存在/不存在用户名的响应**状态码**是否一致（**不能只看 body**） |
| **ENUM002** | **校验响应头/时延一致性**：响应头、响应时间、跳转等是否泄露账号存在性 |
| **ENUM003** | **否定对照（negative control）**：在声称"差异响应可区分存在/不存在"前，**必须**用保证不存在的随机标识符跑一遍相同流程。**防速率限制/锁/IP声誉冒充确定性差异**（蒸馏自 web-vulnhunt-methodology 原则2） |

---

## 九、并发/竞态（RACE）

| 编号 | 测试要点 |
|------|---------|
| **RACE001** | **识别 check-then-act 写操作**：库存/余额/限领/扣减/状态流转等"先查后写"的操作点 |
| **RACE002** | **构造未消费新包高并发发起**：不能重放已消费包；须**新造请求**并发，验超卖/超领/双花 |
| **RACE003** | **以服务端状态差异坐实**：库存/余额/领取记录的前后对比证据，而非仅"响应成功" |

---

## 十、重放（REPLAY）

| 编号 | 测试要点 |
|------|---------|
| **REPLAY001** | **重放+竞态**：直接重放已有包失败时，**必须构造未请求过的新包再高并发重放**，验签名/一次性token是否可重放 |

---

## 十一、验证码/短信绕过（SMS）

| 编号 | 测试要点 |
|------|---------|
| **SMS001** | **置空校验**：验证码/短信码置空时后端是否仍校验 |
| **SMS002** | **缺参绕过**：不提交该参数时是否跳过校验；另测复用、无频率限制、可枚举、响应泄露 |

---

## 十二、优惠/积分/抽奖（PRIZE）

| 编号 | 测试要点 |
|------|---------|
| **PRIZE001** | **重复使用与竞态**：优惠/积分/抽奖/券的重复提交、并发领取、跨账号复用；重放须测竞态双花 |

---

## 十三、反序列化（DESER）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **DESER001** | **序列化格式识别**：确认目标使用哪种序列化格式 — PHP `O:`/`a:`、Java `ac ed` magic bytes / Base64 `rO0`、Python pickle `gASV`、.NET `AAEAAAD/////`、YAML `!!` 标签 | 未识别格式就丢 payload |
| **DESER002** | **盲反序列化检测**：修改序列化字节中非关键字段 → 对比报错类型差异。不同报错=反序列化已发生；相同报错=可能在反序列化前被拦截 | 未做字节修改对比 |
| **DESER003** | **优先DNS/时延验证RCE**：反序列化RCE验证优先用`java.net.URL` DNS回调、`curl` DNS查询、`sleep` 时延 — 不写文件/不反弹shell | 直接尝试写文件或反弹shell |

---

## 十四、原型链污染（PROTO）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **PROTO001** | **污染验证**：注入`{"__proto__":{"polluted":"yes"}}`后，验证`({}).polluted === "yes"`。不可仅凭 parse 错误判安全 | 未执行污染验证 |
| **PROTO002** | **绕过方法≥3种**：`constructor.prototype`、`__pro__`+`__to__` 拼接、嵌套键`["__proto__"]`、宽字符/Unicode编码 | 只试了 `__proto__` |
| **PROTO003** | **Gadget 发现**：确认污染后搜索 Node.js 服务端可利用 gadget（child_process.spawn opts、NODE_OPTIONS、--require）或客户端 XSS gadget（innerHTML、srcdoc、onerror） | 确认污染但未尝试 gadget 利用 |

---

## 十五、HTTP 请求走私（SMUG）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **SMUG001** | **CL.TE / TE.CL / TE.TE 全测**：使用 Turbo Intruder single-packet attack 逐一确认每种类型，不因一种无果即判安全 | 只测了一种类型 |
| **SMUG002** | **时序盲检测**：不依赖响应体内容 — 使用 timing technique（smuggled incomplete chunk + normal request 时间差 > 阈值） | 仅用响应内容判定 |
| **SMUG003** | **HTTP/2 downgrade**：识别 CDN/proxy → origin 的 H2→HTTP/1.1 降级链，测试 `:authority` 头覆盖和 smuggled prefix | 未测 H2C 降级 |

---

## 十六、Web 缓存中毒（CP）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **CP001** | **Cache Key Oracle**：识别缓存键组成（X-Cache-Key / Pragma: x-get-cache-key），unkeyed headers 即为攻击面 | 未确认缓存键 |
| **CP002** | **缓存 HIT 验证**：注入 header → 等缓存 → 不带 header 重新请求 → 确认 `X-Cache: HIT` 且响应含注入内容。不可仅凭单次响应差异 | 未验证缓存 HIT |
| **CP003** | **至少3类 unkeyed input**：X-Forwarded-Host、X-Forwarded-Scheme、X-Original-URL、Accept、Cookie 子字段、Fat GET body | 只测了1个 header |

---

## 十七、GraphQL 安全（GQL）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **GQL001** | **Introspection 备用发现**：introspection 被禁用时，继续检测字段建议错误消息（`Cannot query field 'X' on type 'Y'. Did you mean...`），`__type(name:)` 查询，和非生产环境 introspection | 禁用 introspection 后直接放弃 |
| **GQL002** | **Alias + Batch 绕过**：用别名合并多个查询（`a:user(id:1) b:user(id:2)...`）绕过速率限制；用 Apollo batch `[{query:...},{query:...}]` 绕过认证 | 只测了单个查询 |
| **GQL003** | **Resolver 级注入**：对每个 field argument 测试 SQLi/NoSQLi/SSRF（resolver 可能拼接参数到数据库查询），不只测 GraphQL 语法层 | 只测了 query 层面的语法错误 |

---

## 十八、WebSocket 安全（WS）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **WS001** | **CSWSH（Origin 检查）**：从不同 Origin（evil.com / null / 无 Origin）发起 WebSocket 握手，确认是否拒绝 | 未测试 Origin 绕过 |
| **WS002** | **每条消息鉴权**：WebSocket 握手后，发送修改目标用户ID/资源ID的消息，确认服务端对每条消息有独立权限检查 | 只验证了握手认证 |
| **WS003** | **消息注入**：测试 WebSocket 消息体中的 SQLi/XSS/SSTI — 每条消息是一个独立的注入面 | 未对消息 payload 做注入测试 |

---

## 十九、Clickjacking / XS-Leaks（CLICK）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **CLICK001** | **XFO + CSP 双检查**：同时检查 `X-Frame-Options` 和 `CSP: frame-ancestors` — 两者可能不一致，CSP 可覆盖 XFO | 只查了 XFO |
| **CLICK002** | **sandbox frame busting 绕过**：`<iframe sandbox="allow-forms allow-scripts">` 测试是否可绕过 frame busting JS | 未用 sandbox iframe |
| **CLICK003** | **敏感操作页面**：不只测试首页 — 检查账号删除、密码修改、转账确认、OAuth 授权等关键页面是否可嵌入 | 只测试了首页 |

---

## 二十、JNDI / Java 框架（JNDI）

| 编号 | 测试要点 | 不满足不可判 `tested_not_found` |
|------|---------|-------------------------------|
| **JNDI001** | **DNS/OOB 先行**：在所有用户输入点（headers/params/body）注入 `${jndi:dns://callback}`，用 DNS callback 确认 JNDI lookup 是否触发 | 未做 DNS 探测直接尝试 RCE |
| **JNDI002** | **JDK 版本判定**：JDK ≥ 8u191 时 `trustURLCodebase` 默认 false — 须改用 `javaSerializedData` + 本地 gadget，不可依赖远程 class 加载 | 未区分 JDK 版本 |
| **JNDI003** | **Log4j 混淆绕过**：`${${lower:j}ndi}` `${${::-j}${::-n}${::-d}${::-i}}` 等嵌套语法绕过 WAF 关键字检测 | 只用了一个直连 payload |

---

## 使用规范

### 何时必填 checkpoint_response

当漏洞类型匹配上表前缀，且 `status ∈ {tested_not_found, doubtful, filtered}` 时**必填**：

```json
{
  "param": "order_no",
  "vuln_type": "SQL注入",
  "status": "tested_not_found",
  "filter_probe": {
    "'": ["放行", "原样返回，未触发报错"],
    " ": ["放行", "未过滤"],
    "OR": ["放行", "关键字未拦截"],
    "SLEEP": ["拦截", "触发WAF 403"]
  },
  "checkpoint_response": {
    "SQL001": "符合。测试了空白符(空格/TAB/换行)、注释(#/--/\\/**\\/)、关键字(AND/OR/SELECT/UNION)、符号(' / \" / ( / ))，记入filter_probe",
    "SQL002": "符合。参数值在响应中回显为单引号字符串上下文，用 ' 闭合测试",
    "SQL003": "符合。SLEEP关键字被WAF拦截后，尝试了大小写(sLeEp)、内联注释(/*!50000SLEEP*/)、等价函数(BENCHMARK)，均被拦截",
    "SQL004": "符合。联合查询无显式回显→报错注入无数据库报错→布尔盲注无真/假差异→时间盲注因SLEEP被拦截无法执行，判定为强WAF防护"
  },
  "tests": ["' → 语法报错", "' OR '1'='1 → WAF拦截", "ORDER BY 1 → 正常响应"],
  "basis": "参数值回显表明进入SQL上下文，但强WAF过滤所有可利用关键字和函数，且无绕过窗口"
}
```

### unruled_out 未排除面（蒸馏自 Pentest-Lyan）

每条 `status=tested_not_found` / `not_vulnerable` 的判定**必须**附带 `unruled_out` 字段，列出**尚未排除的攻击面**：

```json
{
  "unruled_out": [
    "二次注入：该参数值是否会被后续SQL查询不安全使用，未验证",
    "WAF绕过：当前测试仅针对关键字黑名单，未测试编码绕过（URL编码/Unicode/双写）",
    "盲注：无回显场景的时间盲注因SLEEP被WAF拦截而无法完成，WAF绕过前不能排除"
  ]
}
```

**规则**：
- 不确定能否排除 → 不能标 `tested_not_found`，应标 `doubtful`
- `unruled_out` 为空数组 → 必须证明穷尽了该漏洞类型的所有攻击路径
- **禁止**用"已全面测试""未发现异常"等模糊词替代具体面

### 防护判定降级规则

| 场景 | 正确判定 | 错误判定 |
|------|---------|---------|
| 输入被过滤但仍可绕过 | `filtered` | `tested_not_found` |
| 输入被拦截但有编码/混淆空间 | `filtered` | `tested_not_found` |
| 输入完全不影响SQL语义 | `tested_not_found` (需证参数化查询) | 仅因无报错即判 |
| 客观条件无法测试 | `doubtful` (说明受阻原因) | `tested_not_found` |
| 有 unruled_out 未排除面 | `doubtful` (不可判安全) | `tested_not_found` |
