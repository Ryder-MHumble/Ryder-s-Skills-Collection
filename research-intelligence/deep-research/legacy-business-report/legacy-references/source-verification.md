# Source验证技术手册

## 环境现状（2026年5月实测）

| 搜索引擎 | 中文查询 | 英文查询 | 状态 |
|---------|---------|---------|------|
| Google | IP被封 | IP被封 | ❌ |
| Bing | 完全不可用（中文查询返回完全不相关结果，如搜「上海创智学院院长」返回豆包广告） | 质量差 | ❌ |
| DuckDuckGo | 被限流 | 被限流 | ❌ |
| **Yahoo搜索** | ❌ 底层=Bing，同样偏移 | ✅ **有效**，尤其英文+中文品牌名混合查询 | ✅英文/⚠️中文 |

## 可用替代策略

### 1. SEC EDGAR API（美国上市公司财务数据）

```bash
curl -s "https://data.sec.gov/api/xbrl/companyfacts/CIK{XXXXXXXX}.json" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  --max-time 30
```

CIK格式：`CIK` + 10位补零数字。如Ekso Bionics = `CIK0001549084`。

返回JSON包含多年XBRL事实数据（营收、净亏损等），可直接解析。

另可使用XBRL实例文件ZIP：
```bash
curl -sL "https://efts.sec.gov/LATEST/ots_xbrl_instances/{filing-id}-xbrl.zip" \
  -H 'User-Agent: ...' --max-time 30 -o tmp.zip
unzip -p tmp.zip | head -500
```

⚠️ **2026年5月实测**：XBRL zip直接URL从服务器返回403（EDGAR反爬加强）。改用EDGAR搜索API验证文件存在：
```bash
curl -sL "https://efts.sec.gov/LATEST/search-index?q=%22Company+Name%22" \
  -H 'User-Agent: jingyi@research.com' --max-time 15
```
或用CGI搜索页：`https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=10-K`

### 2. 36氪搜索（中国创业公司融资信息）

1. `browser_navigate` 到 `https://www.36kr.com/search/articles/{keyword}`
2. 在搜索结果页用 `browser_snapshot` 提取文章链接（格式 `/p/{数字ID}`）
3. `browser_navigate` 到具体文章验证内容

⚠️ **36氪验证码陷阱**：36氪文章页经常触发滑块验证码（TTGCaptcha），browser无法通过。如果被拦截：
- 搜索结果页的**标题和摘要**已经可以确认数据点存在
- 可以记录文章URL和标题作为source标注
- 不要反复重试（验证码不会消失）
- curl也会被拦截返回验证码HTML

验证案例：极壳B+轮5000万美元融资，36氪2026-05-18发文确认，URL `https://36kr.com/p/3814502648045319`（有验证码但标题可确认）

### 3. 中文科技媒体（已验证可达，无验证码）

| 媒体 | URL格式 | 可达性 | 验证案例 |
|------|---------|--------|----------|
| 爱范儿 | `ifanr.com/{id}` | ✅ 无验证码 | https://www.ifanr.com/1620966（Hypershell Pro X评测） |
| 极客公园 | `geekpark.net/news/{id}` | ✅ 无验证码 | https://www.geekpark.net/news/351019（Hypershell深度体验） |
| 腾讯新闻 | `news.qq.com/rain/a/{id}` | ✅ 无验证码 | https://news.qq.com/rain/a/20251201A08U7I00（极壳创始人对话） |

**爱范儿和极客公园**是消费科技/硬件评测的优质B级来源，文章含实测数据、用户原话、续航测试等。

**腾讯新闻**常转载懒熊体育等专业媒体，内容含融资细节、创始人访谈、行业判断。

⚠️ 爱范儿curl可能超时（15秒不够），优先用browser导航。

### 4. 直接URL访问（已知具体URL）

```bash
curl -sI -L "$URL" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  --max-time 12 -o /dev/null -w '%{http_code}'
```

200/301/302 = 可达，404/403/000 = 不可达。

### 5. 公司官网产品页

直接curl或browser导航到官网，提取产品参数/定价。属C级来源。

Squarespace托管的网站（如skipwithjoy.com）curl可获取HTML但内容为JS渲染，需要browser才能看到产品信息。

**中国公司官网访问策略**（2026-05实测）：
- 很多中国公司官网是SPA单页应用，curl只能拿到空壳HTML，**必须用browser导航**
- 优先用browser访问，curl仅用于快速检测HTTP状态码
- 示例：fftai.com（傅利叶）用browser可看到完整产品线，curl无法渲染

⚠️ **公司官网不可达 = 信息盲区**：部分中国公司官网长期无法访问，实测案例：
- 程天科技 ctibot.com：超时/空响应
- 迈步机器人 maburobot.com：DNS无法解析
- 在当前搜索环境下（Bing中文不可用、Google被封、社交平台不可用），官网不可达的公司几乎无替代信息源
- 此时只能标注为「信息未独立验证」并向用户请求材料

### 6. TechCrunch等英文科技媒体

直接browser导航到已知URL。搜索功能不稳定，最好已知具体URL再访问。

验证案例：German Bionic Series A $20M，TechCrunch 2020-12-16报道，URL可达

### 7. 公司IR财报PDF

直接curl下载PDF，用pymupdf提取文本。属A级来源。

验证案例：Cyberdyne FY2026财报。⚠️ 旧路径 `/company/ir/_library/3q/4q_2026_kessan.pdf` 已404。正确路径：
- IR信息页：`https://www.cyberdyne.jp/company/IR.html`（注意大写IR）
- 决算短信PDF：`https://www.cyberdyne.jp/wp_uploads/2026/05/20260514_kessantanshin_jp.pdf`（339KB，已验证可达）

⚠️ 日本公司网站URL结构经常变动，报告中的PDF链接可能失效，应以IR信息页作为A级source入口。

## 不可靠的source

| 来源 | 问题 | 处理方式 |
|------|------|---------|
| 百度百科 | URL编码不稳定，频繁404；但人物/机构页面本身内容可访问 | 不当source链接，可当事实参考 |
| delegate_task子agent返回的URL | 可能编造，无法验证 | 不信任 |
| delegate_task子agent返回的URL | 可能编造，无法验证 | 不信任 |
| Reddit | 需要验证 | 不直接爬取 |
| YouTube | 无法提取评论 | 不使用 |
| 36氪文章页（curl） | 触发验证码 | 搜索页确认标题即可 |
| 中国工商注册网站（天眼查/企查查等） | 全部反爬封IP | 必须请用户自行查询 |

### 8. 人民网搜索（中国机构/政策研究首选）

**人民网搜索** `https://search.people.cn/s/?keyword={关键词}&st=1` 是中文机构/政策研究最可靠的信息源：

- ✅ 无验证码、无反爬、无需登录
- ✅ 聚合上观新闻、解放日报等上海权威媒体内容
- ✅ 搜索结果精准，不会偏移到无关内容
- ⚠️ 结果页摘要高亮标记会打断关键词，需点进文章确认

**典型用法：** 查找某机构的负责人信息时，搜"机构名+负责人姓名"或"机构名+调研"（如领导调研必然有接待人员信息），比任何搜索引擎都有效。

验证案例：搜索「上海创智学院」→ 首条结果直接确认"党委书记、常务副院长丁晓东"（来源：上观新闻转人民网2025-09-13）

### 9. 第一财经搜索（中国科技/产业信息）

`https://www.yicai.com/search?keys={关键词}` 可搜索文章URL：

- ✅ 搜索结果页可提取文章URL（格式 `/news/{id}.html` 或 `/video/{id}.html`）
- ⚠️ 文章内容页经常截断为付费/会员内容，只能看到摘要
- 可与人民网互补：人民网搜机构/政策，第一财经搜产业/公司

### 10. 百度百科（人物/机构基础信息）

百度百科对具体人物/机构的基础信息页面无需登录即可访问：

- ✅ 人物职务、履历、出生年月等基础事实通常准确
- ⚠️ URL编码不稳定（如`/item/丁晓东/7294629`），不能当可靠source链接
- ⚠️ 内容可能滞后，不适合查最新变动
- 用browser_console提取`document.body.innerText`可获得完整文本（snapshot经常被截断）

### 11. Browser控制台文本提取技巧

当browser_snapshot被截断时，用JS直接提取全文：

```javascript
document.body.innerText.substring(0, 8000)
```

- 对百度百科、人民网文章页等纯文本页面效果极好
- 对JS渲染页面（如爱范儿Squarespace）可能拿到空文本，需回到snapshot
- 比snapshot更完整，不易被sidebar/footer干扰

### 12. Yahoo搜索（Google/Bing不可用时的替代搜索引擎）

**Yahoo搜索** `https://search.yahoo.com/?p={query}` 或 `https://www.yahoo.com/search?p={query}` 在Google/Bing均不可用时是**唯一可用的英文+中文混合搜索引擎**：

- ✅ 英文查询效果好，能返回公司官网、CrunchBase、新闻媒体等结果
- ✅ 支持中文关键词+英文混合查询（如 `"GearFlow" "吉孚洛" 外骨骼 产品 融资`）
- ✅ 图片搜索结果常包含Alamy/Getty图库照片——**图库照片的caption是产品发布事件的有力证据**
- ✅ 视频搜索结果包含YouTube链接——可直接跳转验证
- ⚠️ 中文纯中文查询效果与Bing相同（Yahoo搜索底层是Bing），返回不相关结果
- ⚠️ 搜索首页需要先点击搜索按钮触发，不能直接在首页看到结果

**关键发现**：Yahoo搜索的图片搜索结果中，Alamy/Getty等图库照片的caption包含精确日期和事件描述（如「SHANGHAI, CHINA - MARCH 20, 2025 - An exoskeleton walking robot launched by Haier for elderly」），是**产品发布事件验证的意外高质量来源**。

**使用模式**：
1. `browser_navigate` 到 Yahoo搜索页
2. 输入查询（优先英文+中文品牌名混合）
3. 点击搜索按钮
4. `browser_snapshot` 提取结果
5. 重点关注：图片搜索carousel（含图库caption）、视频搜索结果（含YouTube链接）

验证案例：搜索 `Haier exoskeleton wearable robot` → 图片结果Alamy caption确认海尔2025年3月20日上海发布外骨骼步行机器人；搜索 `"GearFlow" exoskeleton wearable outdoor` → 首条结果为Gearflow Robotics YouTube频道+抖音链接+企查查/亿欧公司信息

### 13. YouTube频道页（公司/产品验证）

YouTube频道页 `https://www.youtube.com/@{ChannelName}` 是验证新兴消费品牌的有效来源：

- ✅ 频道描述（About弹窗）常包含公司自我介绍、总部地址、成立时间
- ✅ 视频标题直接暴露产品名称/型号（如「Let's meet the all-new Gearflow Exoskeleton C2」）
- ✅ 社媒链接列表暴露品牌在抖音/小红书/Instagram等平台的存在
- ✅ 订阅数+观看数+建号时间可判断品牌成熟度
- ⚠️ YouTube本身被列为「不可靠source」，但频道About信息属于C级来源，可用于验证公司存在和产品线

**使用技巧**：点击频道描述的 `...more` 按钮展开完整About信息，包含社媒链接矩阵。这是发现中国品牌社媒存在的快捷方式（因为小红书/抖音本身不可直接访问）。

验证案例：@GearflowRobotics → About信息确认「consumer exoskeleton brand rooted in Zhuhai, China」，视频标题确认产品名C2，社媒链接确认抖音3个账号+小红书+Instagram+TikTok

## 完全不可用的中文信息源

| 来源 | 问题 | 备注 |
|------|------|------|
| 天眼查 tianyancha.com | 反爬封IP | 所有企业注册信息查询均不可用 |
| 企查查 qcc.com | 405封IP | 同上 |
| 爱企查 aiqicha.baidu.com | 空白页/反爬 | 同上 |
| 启信宝 qixin.com | 不显示搜索结果 | 同上 |
| 国家企业信用信息公示系统 gsxt.gov.cn | IP标记为攻击 | 同上 |
| 百度搜索（mobile） | 每次触发图形验证码 | 不可用 |
| 京东搜索 search.jd.com | 触发风控验证页 | 不可用 |
| 小红书 xiaohongshu.com | IP risk detection，强制登录 | 不可用 |
| 搜狗搜索 sogou.com | 返回验证码/乱码内容 | 不可用 |
| 上观新闻 shobserver.com | Access Denied | 需用人民网搜索间接获取其内容 |
| 解放日报 jfdaily.com | Access Denied | 同上 |
| 微博搜索 s.weibo.com | 需登录 | 不可用 |
| 知乎搜索 zhihu.com | 反爬空白页 | 不可用 |
| 澎湃新闻搜索 thepaper.cn | 返回0结果 | 不可用 |

**关键影响：** 中国企业工商信息（股东、法人、持股）在此环境下**完全无法查询**。如需此类信息，必须请用户自行在天眼查/企查查上查询后提供。

## 新兴消费品类搜索盲区

当目标品类是1-2年内才出现的新兴消费品类（如2024-2025年消费级外骨骼、轻时尚助力设备等），存在系统性搜索盲区：

**根本原因**：产品信息主要存在于小红书种草、抖音测评、微信公众号等社交平台，而这些平台在此环境全部不可用（验证码/反爬/封IP）。主流搜索引擎和科技媒体尚未收录。

**典型表现**：
- 用户提及的品牌在Bing/Google/百度搜不到任何结果
- 品牌可能只有微信小程序或抖音店铺，没有传统官网
- 公司官网可能是SPA单页应用，browser能看到导航但curl拿不到内容

**推荐策略**：
1. **先向用户确认**：品牌中文名、官网链接、电商平台链接、公众号名称——任何锚点都行
2. 用户提供锚点后，做**定向验证**（访问已知URL、搜索已知媒体）而非泛搜索
3. 搜索引擎零结果 ≠ 品牌不存在，此时必须回问用户
4. 不要在无目标的web搜索上浪费超过10分钟
5. 如果品牌确实只有社交平台信息，在报告中诚实标注「信息来源为社交平台，未独立验证」

## delegate_task子agent使用注意

- **不要给子agent分配browser工具集的web搜索任务**：大概率超时（600秒限制不够用于浏览器操作+页面加载+内容提取）
- 子agent适合做**纯curl可完成**的验证任务（如SEC EDGAR API调用、已知URL的HTTP状态检查）
- 子agent返回的URL**必须自己二次验证**，不要直接引用
- 子agent已完成但输出被截断时，检查是否有中间文件保存到磁盘

## 批量验证脚本模板

```bash
urls=(
  "https://example.com/page1"
  "https://example.com/page2"
)
for url in "${urls[@]}"; do
    code=$(curl -sI -L "$url" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' --max-time 12 -o /dev/null -w '%{http_code}' 2>/dev/null)
    if [ "$code" = "200" ]; then icon="✅"; else icon="❌"; fi
    echo "$icon $code $url"
done
```
