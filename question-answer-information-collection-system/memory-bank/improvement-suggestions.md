### 爬虫模块分析与优化建议

你好！看了你新提供的实施计划（IMPLEMENTATION_PLAN.md），整体框架很务实，遵循“后端优先、前端后行、数据最后”的顺序，适合Django + Vue的开发。用户认证、数据API、统计分析和前端页面的设计都比较完整，尤其是API响应格式标准化（{code, data, message}）、权限控制和性能测试的部分，体现了生产级考虑。数据目标（10,000+条）也合理，验收清单覆盖全面。

但是，如你所指，爬虫部分（第三阶段：步骤7-11）确实有优化空间。这个模块的目标是采集“360问答”平台的数据（假设是360搜索旗下的问答社区，如wenda.so.com或类似），但设计偏简单（requests + BeautifulSoup），忽略了现代问答平台的反爬机制（e.g., IP封禁、JS渲染、行为检测）。如果不优化，采集效率低、失败率高，尤其全量模式下（15,000条），可能导致封禁或数据不全。2026年，这些平台反爬更智能（AI监控），简单脚本难持久。

下面我重点分析爬虫部分的潜在问题，并给出针对性优化建议。其他阶段（如用户模块的密码明文存储——强烈建议改用hash；前端的ECharts集成好，但加loading状态）整体OK，我只简要提及非爬虫问题。建议基于Python爬虫生态（Scrapy/Playwright主流），无缝集成你的Django后端。如果你需要更新后的完整计划文档或代码片段，我可以提供。

#### 1. **现有爬虫设计的潜在问题**
基于步骤7-11（模型、清洗、脚本、管理命令、API），总结核心问题：

- **反爬机制不足**：
  - 用requests发送HTTP请求，仅加Headers和1-2s延迟，容易被检测（User-Agent单一、无代理）。360问答页面可能有JS动态加载（e.g., 回答列表懒加载），BeautifulSoup无法处理JS，导致解析失败。
  - 重试仅3次，无代理旋转或指纹伪装。问答平台常有行为分析（e.g., 高频访问触发验证码），全量采集（多页历史数据）风险高——IP易封，需手动换IP。
  - 无登录支持：部分问答需登录查看完整回答，但文档未提。

- **效率与性能问题**：
  - 同步请求（get_page()），全量模式下采集15,000条（假设每页20条，750页）可能需数小时，甚至因超时崩溃。步骤10的--limit好，但无分布式/并行。
  - 数据清洗在utils.py中，但未集成到爬虫管道，容易重复处理。入库用ORM，但大数据时（10,000+）批量插入未优化，可能数据库负载高。
  - 异步标为“可选”（Django Q/Celery），但API同步调用（POST /api/crawler/start/）会阻塞后端响应。

- **合规与安全风险**：
  - 360问答条款禁止大规模爬取（类似知乎/百度知道），用于“网络问答平台”可能触碰商业数据采集灰区。文档无免责或限频机制。
  - 日志记录进度好，但若包含URL/数据，需加密。模型中source_url暴露来源，潜在追踪风险。
  - 无监控/恢复：中途失败（如网络断），无自动续传。

- **集成与维护问题**：
  - 脚本在spiders/wenda_spider.py，独立于Django，测试难。BeautifulSoup慢（用lxml更好），但2026年推荐parsel/selectolax（快5-10倍）。
  - 管理命令好，但API状态查询（CrawlerStatus模型）实现复杂，无实时进度（e.g., “running 50%”）。
  - 测试仅小规模（20条），全量未提模拟反爬测试。

- **数据质量与扩展性**：
  - 去重基于title/source_url好，但问答ID更可靠（需提取）。tags用JSON，但ManyToManyField更好（ORM支持查询）。
  - 无扩展：如采集多平台（不止360），或AI增强解析（e.g., LLM提取实体）。

总体风险：演示模式（20条）OK，但全量失败率>30%，影响数据准备（步骤22-24）。性能测试中，爬虫相关API可能超时。

#### 2. **优化建议**
将爬虫升级为“模块化智能采集系统”，用**Scrapy + Playwright**（处理JS），集成Celery异步。优先JSON API（如果360暴露），fallback浏览器模拟。目标：成功率>90%，全量分批跑（e.g., 每天限2000条）。保持Django集成，便于管理命令/API调用。

##### **2.1 技术栈调整**
- **核心框架**：**Scrapy**（调度/管道/去重） + **Playwright**（JS渲染，通过scrapy-playwright插件）。替换requests + BeautifulSoup——Scrapy更robust，Playwright比Selenium快/隐蔽。
  - 安装：`pip install scrapy scrapy-playwright celery django-celery-results playwright`；然后`playwright install`。
  - 为什么？Scrapy易集成Django（作为Celery任务），自动处理分页/重试。Playwright伪装浏览器，指纹低。
- **异步执行**：强制用**Celery + Redis**（broker）。API触发任务，返回task_id；状态查询用Celery结果。
  - 配置：settings.py加`CELERY_BROKER_URL = 'redis://localhost:6379/0'`。
- **反爬增强**：
  - **代理池**：集成Scrapy-Rotating-Proxies（免费代理）或付费（如Bright Data）。每请求随机IP。
  - **指纹伪装**：加playwright-stealth（pip install），隐藏自动化痕迹。
  - **延迟/行为模拟**：随机睡3-8s；Playwright加鼠标滚动/等待。
  - **验证码**：集成2Captcha API（付费），或手动（但不荐）。
  - **UA/Headers旋转**：Scrapy中间件随机列表（mobile/desktop）。
  - **API优先**：用DevTools抓360问答的JSON接口（e.g., /api/questions.json），用httpx异步发。效率高10倍，无需浏览器。

##### **2.2 模块重设计**
更新第三阶段为以下（替换原步骤7-11）：

**步骤7：设计问答数据模型**（原好，优化tags为ManyToManyField(Tag模型)，加unique_together=(title, source_url)防重）。

**步骤8：实现数据清洗工具**（原好，集成到Scrapy Pipeline）。

**步骤9：实现360问答爬虫脚本**（重写为Scrapy Spider）：
- 创建crawler/spiders/wenda_spider.py：
  ```python
  import scrapy
  from scrapy_playwright.page import PageMethod
  from crawler.items import QuestionItem  # 定义Item

  class WendaSpider(scrapy.Spider):
      name = 'wenda_360'
      start_urls = ['https://wenda.so.com/search?q=关键词']  # 调整为你的起点

      def start_requests(self):
          for url in self.start_urls:
              yield scrapy.Request(url, meta={'playwright': True, 'playwright_page_methods': [PageMethod('wait_for_selector', '.question-list')]})  # 调整selector

      def parse(self, response):
          for item in response.css('.question-item'):  # 调整为360的selector
              yield QuestionItem({
                  'title': item.css('.title a::text').get().strip(),
                  'description': item.css('.desc::text').get(),
                  'answer_content': item.css('.answer::text').get(),
                  # ... 其他字段，提取answer_time等
                  'source_url': item.css('.title a::attr(href)').get()
              })
          # 分页：next_page = response.css('.next-page::attr(href)').get()
          if next_page and (self.mode == 'full' or self.collected < self.limit):
              yield scrapy.Request(next_page, meta={'playwright': True})

  # items.py定义QuestionItem(scrapy.Item)
  ```
- Pipeline（crawler/pipelines.py）：集成DataCleaner，批量存MySQL（用django.db批量插入）。

**步骤10：创建爬虫管理命令**（优化用Celery触发）：
- handle()：用celery_app.send_task('crawler.tasks.run_spider', args=[mode, limit])。

**步骤11：创建爬虫状态API**（用Celery结果）：
- POST /api/crawler/start/：返回task_id。
- GET /api/crawler/status/<task_id>/：用AsyncResult查state/progress/logs。
- tasks.py示例：
  ```python
  from celery import shared_task
  from scrapy.crawler import CrawlerProcess

  @shared_task(bind=True)
  def run_spider(self, mode='demo', limit=20):
      process = CrawlerProcess(settings={  # 配置代理/UA
          'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': True},
          'ITEM_PIPELINES': {'crawler.pipelines.QuestionPipeline': 300},
      })
      process.crawl('wenda_360', mode=mode, limit=limit)
      process.start()
      self.update_state(state='PROGRESS', meta={'current': 10, 'total': limit})  # 进度更新
      return {'status': 'completed', 'collected': limit}
  ```

##### **2.3 测试与数据准备优化**
- **测试**：加pytest测试Spider（mock响应）。模拟反爬：加延迟/代理测试。
- **数据准备**（步骤22-24）：优先用公开数据集（e.g., Kaggle问答CSV）导入，fallback爬取。分批+续传：用Redis存进度。
- **性能**：全量用分布式Scrapy-Cluster（多机）。目标：10,000条<2小时。
- **合规**：加robots.txt检查；限频（每天<5000条）；文档加免责。

##### **2.4 非爬虫部分简要建议**
- 用户模块：密码改hash（用set_password()）；role用choices。
- API：加drf-spectacular生成Swagger文档。
- 前端：ECharts加resize监听；数据中心用virtual-scroller优化大表。
- 部署：加Docker-compose（后端+Redis+Celery）。

#### 3. **下一步行动**
- **优先**：实现演示Spider，测试20条。如果OK，扩展全量。
- **时间**：原第三阶段2-3天，优化后4-5天（加反爬/Celery）。
- 如果“360问答”具体URL/selector有变，告诉我，我帮调试。想查360问答最新反爬？可以用工具，但先假设标准。

这个优化能让爬虫更可靠。如果你有具体问题（如“试了requests被封”），贴细节，我再细化！