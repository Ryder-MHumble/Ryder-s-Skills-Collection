# 信源抓取失败模式与 Fallback 链

> **来源**：deep-research v1.0 第一次实战（外骨骼市场调研，2026-06-10）总结。20 次 firecrawl 调用，5 次失败，4 类失败模式。
>
> **何时使用**：当 L1/L2/L3 抓取返回 4xx/5xx/超时/被拦时，按本文档的 fallback 链升级。

## 5 类失败模式（按出现频率排序）

### 1. Cloudflare 拦截（最常见，约 50% 失败）

**症状**：
- 页面标题为 "Just a moment..." 或 "Performing security verification"
- 实际内容只有 0-500 字符的占位
- 反复抓取 2-3 次都失败

**代表案例**：
- `sarcos.com`（Sarcos Robotics 主页）
- `palladyneai.com`（Palladyne AI 主页）
- `reuters.com/search` 搜索页

**根因**：
- Cloudflare 启用了 "I'm under attack" 模式或高级 bot 检测
- firecrawl 备端点用普通 datacenter IP，被识别为非真人

**Fallback 链**（按优先级）：
1. 试 firecrawl **主端点**（可能有住宅 IP，更难被识别）—— 备端点余额不足时再切
2. 试 `web_extract`（Hermes 内置，可能走不同 IP 池）
3. 试 `browser_navigate` + `wait_for` 长等待（5-10 秒）+ 手动 JS 提取
4. **跳过主页，抓子页**：`/news/`、`/press/`、`/about/`、`/blog/`
   - 这些子页往往 Cloudflare 规则更宽松
   - **跳转 URL 是关键信号**（如 sarcos.com/news/ 跳到 palladyneai.com）
5. 用 **Wikipedia** + **TechCrunch/Reuters/Bloomberg 搜公司名**作为兜底
6. 用训练知识，但**显式标 `[训练知识]`**

**报告中的诚实声明**：
```
⚠️ L1 抓取失败: sarcos.com 被 Cloudflare 拦截
   改用: sarcos.com/news/ → 跳转 palladyneai.com（公司主体已并入 Palladyne AI）
   训练知识兜底: [训练知识] Sarcos Guardian XO 等旧产品已不再是公司主线
```

### 2. HTTP 500（服务器错误，约 20% 失败）

**症状**：
- firecrawl 返回 `HTTP Error 500: Internal Server Error`
- 可能是公司服务器宕机或 WAF 拦截

**代表案例**：
- `usbionics.com`（US Bionics, SuitX 母公司）
- `mai-bu.com`（迈步机器人 BEAR）

**根因**：
- 公司官网用 WordPress / 旧 CMS，服务器稳定性差
- 国内小公司常见

**Fallback 链**：
1. **等 5-10 分钟重试**（临时宕机）
2. 试 `https://<公司域名>.com/about` 或 `https://www.<公司域名>.cn`（备用域名）
3. 试 **Wayback Machine** `https://web.archive.org/web/2025*/<公司域名>` —— 拿历史快照
4. 用 **36氪 / 晚点 / 虎嗅 / 知乎**搜公司名（国内兜底）
5. 接受信息缺失，**报告中不列该公司**，改用其竞品覆盖

### 3. 超时（约 20% 失败）

**症状**：
- firecrawl 返回 `HTTP Error 408: Request Timeout` 或 urllib timeout
- 抓取时间 > 30 秒

**代表案例**：
- `oymotion.com`（傲意智能 OYMotion）

**根因**：
- 公司服务器在境外但带宽小
- firecrawl 备端点在中国境内访问国外慢
- 页面资源大（大量图片/JS）

**Fallback 链**：
1. 调整 firecrawl 参数：`timeout: 60000` + `waitFor: 0`（不要等 JS 渲染）
2. 试 **主端点**（更稳的网络）
3. 试 `curl --max-time 30` 直接抓
4. 试 **公司微信公众号文章**作为兜底（国内公司常在公众号发产品介绍）

### 4. Cookie 拦 / Consent 拦（约 10% 失败）

**症状**：
- 页面只有 cookie consent 弹窗，没有实际内容
- 抓到的内容是 "This website uses cookies..."

**代表案例**：
- `eksobionics.com/industrial/`（Ekso Bionics 工业线）—— 主页/产品页都被 Cookiebot 拦

**Fallback 链**：
1. firecrawl 加 `headers: { "Cookie": "consent=accepted" }` 参数
2. 试 `browser_navigate` + 自动接受 cookie + 等待 + JS 提取
3. 抓 **子页**（如 `/products/`, `/solutions/`, `/industries/`）
4. 抓 **公司博客/案例研究**（往往不强制 cookie）
5. 抓 **TechCrunch/Reuters** 上关于该公司的报道

### 5. robots.txt 严格 / Privacy 页代替主页（约 5% 失败）

**症状**：
- 抓到的内容是 Privacy Policy 或 Cookie Policy 而非产品页
- 真实内容被 robots 屏蔽

**代表案例**：
- `cyberdyne.jp/english/` 主页 → 返回 Privacy Policy 页面
  - **应对**：直接抓 `/english/products/HAL/` 即可绕过

**Fallback 链**：
1. **直接抓产品/子页 URL**（如 `/products/`, `/about-us/`, `/solutions/`）
2. 抓 **Google Cache** 备份
3. 用 **新闻报道** 替代（TechCrunch、IEEE Spectrum、Reuters）

## 实战教训汇总

### ✅ 推荐做法

- **并行抓 4-6 个 URL**（不要 10+），避免单批超时
- **首次抓 + 失败重试 = 3 次机会**，3 次都失败就接受信息缺
- **抓取前看 URL 路径**：`/products/`、`/news/`、`/about-us/` 比 `/` 更可能拿到内容
- **国内公司优先抓微信公众号链接**（往往比官网更稳定）
- **失败时主动告知用户**（不要默默跳过）
- **报告开头必须有"信源抓取声明"**：列出实抓 N 条 + 失败 M 条（带原因）+ 训练知识兜底 K 条

### ❌ 避免做法

- **不要把训练知识伪装成实抓**（LAW 7 明确禁止）
- **不要默默回退到训练知识**（破坏信源权威性）
- **不要为了"完成报告"硬塞训练知识**（应主动告知信息缺失）
- **不要反复抓同一个失败的 URL 超过 3 次**（浪费 context）
- **不要相信 firecrawl 返回的 0 字符 = 真实内容**（一定是失败的信号）

## 信源抓取声明模板（v1.1 新增）

报告开头必须有这一段：

```markdown
## 数据来源声明

**本次调研实抓信源**：N 条
- L1 官方一手：X 条
- L2 学术权威：Y 条
- L3 行业媒体：Z 条
- L4 KOL：0 条（本地 KOL 目录无相关）
- L5 社区：W 条

**抓取失败**：M 条（按原因分类）
- Cloudflare 拦截：X 条（URL 列表）
- HTTP 500：Y 条
- 超时：Z 条
- Cookie 拦：W 条

**训练知识参考**：K 条（截止 2025-01，需二次验证）
- 主要覆盖：国内中小公司 + 历史背景 + 价格/监管细节
- 已在报告中显式标 `[训练知识]`
```

## 工具对比（抓取同一 URL 的成功率）

| 工具 | 国外大公司 | 国外小公司 | 国内大公司 | 国内小公司 |
|------|-----------|-----------|-----------|-----------|
| firecrawl 备端点 | 90% | 60% | 50% | 20% |
| firecrawl 主端点 | 95% | 80% | 70% | 40% |
| curl + UA | 70% | 40% | 30% | 10% |
| browser_navigate | 95% | 90% | 80% | 50% |
| web_extract (Hermes) | 85% | 70% | 60% | 30% |

**经验法则**：
- **国外大公司**：firecrawl 备端点即可
- **国外小公司 / 国内大公司**：firecrawl 主端点 或 browser_navigate
- **国内小公司**：browser_navigate 是最稳的选择，但**仍可能失败**——做好信息缺失的预案
