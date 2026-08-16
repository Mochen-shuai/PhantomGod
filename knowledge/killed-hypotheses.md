# Killed Hypotheses — 失败假设追踪

> 蒸馏自 web-vulnhunt-methodology 的 killed-hypotheses.md。
> 重复死路是漏洞研究最昂贵的失效模式。每完成一个目标，在此记录**无效的方法**。

## 使用规则

- 每条记录：**假设 → 精确测试 → 结果 → 一句教训**
- 并非"这个漏洞不存在"，而是"这个方法在这个目标上不work"
- 下次测试同类目标前，先读此文件

---

## 模板

```markdown
## H{编号} — {简短描述}

**假设.** {具体假设内容}

**测试.** {精确的测试方法、payload、端点}

**结果.** {实际观察到的现象}

**教训.** {一句话：为什么失败、什么条件下可能成立、替代方向}
```

---

## H1 — SQLi 时间盲注 SLEEP 被 WAF 拦截

**假设.** `search.php?keyword=test' AND SLEEP(5)--` 可触发时间盲注

**测试.** 5种SLEEP变体（SLEEP/BENCHMARK/pg_sleep/WAITFOR DELAY/DBMS_LOCK.SLEEP）

**结果.** 所有含SLEEP关键字的请求返回403+WAF拦截页，不含SLEEP的请求正常

**教训.** WAF对延时函数关键字是全量拦截，需绕过关键字而非闭合——尝试 `SLE/**/EP`、`/*!50000SLEEP*/`、`benchmark()`小写。注入可能仍存在，但先要过WAF层。

---

## H2 — upload.php 表单参数猜测

**假设.** upload.php 接受 `file` 参数

**测试.** 用 `file=@/dev/null;filename=test.png` 发送POST

**结果.** 空响应，无任何输出

**教训.** 参数名不是 `file`，实际是 `product_no`+`category`+`file` 三参数组合(来自merchant.js的doUploadImage函数)。**curl失败时优先回读JS找实际调用方式**，而非猜测参数名。

---

## H3 — 图片验证码绕过(置空参数)

**假设.** 注册接口 `captcha` 参数置空可绕过验证码校验

**测试.** `{"captcha":""}` 和 `{"captcha":null}` 和 完全不带 `captcha` 字段

**结果.** 三种方式均返回 `"请输入图片验证码"`

**教训.** 后端确实强制校验了captcha字段的存在性。下一步可尝试：暴力破解(4位数字10000种，但需解决session绑定)、OCR识别、验证码复用(同一session多次注册)。

---

## H4 — 商户设置折扣为0实现免费

**假设.** `discount-set.php` 设置 `discount_percent=0` 可实现零元购

**测试.** `{"discount_percent":0.0, "discount_start":..., "discount_end":...}`

**结果.** `"折扣率必须在0-1之间"` — 0被拒绝

**教训.** 校验是 `>0` 而非 `>=0`。但 `0.01` 未被拒绝（0.01折=0.1折），理论上可把价格降到极低但非零。需验证：0.01是否被接受？→ 已被接受(99% off)。**最小值应该是 >0 但值太小仍有危害。**

---

## H5 — 跨商户删除商品

**假设.** 商户shanghu1可删除商户shanghu2的商品

**测试.** `product-delete.php {"product_no":"SP20260101004"}` (属于shanghu2)

**结果.** `"商品不存在或无权删除"` — 被正确拦截

**教训.** 跨商户保护在此端点生效。但要注意：`product-image-delete.php` 不需要 product_no 就能删图片（只需 product_no+image），且 product_no 参数校验不严格。**同模块不同端点保护不一致是常见模式。**

---

## H6 — 支付签名重放

**假设.** 支付URL中的 `sign` 参数可被重放（拿已支付订单的sign支付新订单）

**测试.** 将 DD202608011600001 的 sign 替换到 DD202608011626001 的支付请求中

**结果.** `"签名验证失败"` — 签名包含 order_no，不可跨订单复用

**教训.** 签名机制正确实现了参数绑定(order_no+amount+timestamp)。下一步：测试签名算法是否可预测(HMAC key是否硬编码在JS中)、timestamp是否可回退。

---

## H7 — 并发退款双花

**假设.** 对同一订单并发发送3个退款请求可实现多次退款

**测试.** 3个并发 `refund.php {"order_no":"DD202608011606001","refund_amount":0.01}`

**结果.** 第一个成功，后续两个返回 `"当前订单状态不允许退款"` — 状态机保护生效

**教训.** 退款操作有乐观锁/状态机保护。但并发创建订单场景(create-batch-order)5个请求全部成功——**并发漏洞通常不在"消费"端而在"创建"端**。

---

*最后更新: 2026-08-01*
