# 目标网站分析报告

> 更新日期: 2026-01-30
> 阶段: 阶段三 - 数据准备与导入 - 步骤 3.1

---

## 1. 目标网站选择

### 已分析的网站

| 网站 | URL | 状态 | 备注 |
|:-----|:----|:----:|:-----|
| 下厨房 | https://www.xiachufang.com | ✅ 可访问 | 主要目标 |
| 美食杰 | https://www.meishij.net | ❌ 404 | 需要备选方案 |

**决策**：以下厨房为主要爬取目标，如有需要可添加备选网站（如豆果美食、香哈菜谱等）。

---

## 2. 下厨房网站结构分析

### 2.1 网站基本信息

| 项目 | 内容 |
|:-----|:-----|
| 网站名称 | 下厨房 (xiachufang.com) |
| 主域名 | https://www.xiachufang.com |
| 移动端 | https://m.xiachufang.com |
| 内容类型 | 菜谱分享平台 |
| 内容规模 | 3,500,000+ 菜谱，79,000,000+ 作品 |

### 2.2 URL 结构分析

#### 首页
- URL: `https://www.xiachufang.com/`
- 包含: 热门菜谱、新秀菜谱、时令食材等

#### 分类页
- URL: `https://www.xiachufang.com/category/`
- 分类维度:
  - 菜式（家常菜、快手菜、下饭菜等）
  - 烘焙甜品饮料（蛋糕、面包、饼干等）
  - 肉类（猪肉、鸡肉、牛肉等）
  - 蔬菜水果
  - 汤粥主食
  - 口味特色（辣、糖醋、蒜香等）
  - 水产
  - 蛋奶豆制品
  - 米面干果腌咸

#### 菜谱详情页
- URL 格式: `https://www.xiachufang.com/recipe/{recipe_id}/`
- 示例: `https://www.xiachufang.com/recipe/100000/` (无油版红烧肉)

#### 菜谱列表页（按分类）
- URL 格式: `https://www.xiachufang.com/category/{category_id}/`
- 可通过分类页获取具体分类链接

### 2.3 菜谱详情页 HTML 结构

#### 关键数据字段

| 字段 | CSS选择器/位置 | 说明 |
|:-----|:---------------|:-----|
| 菜谱名称 | `h1.page-title` | 菜谱标题 |
| 成品图片 | `.recipe-cover img` | 主图 URL |
| 用料列表 | `.recipe-ingredients` | 食材及用量 |
| 制作步骤 | `.recipe-steps` | 详细步骤和图片 |
| 小贴士 | `.recipe-tip` | 额外提示 |
| 做过人数 | `.stats-done` | 社交数据 |
| 收藏人数 | `.stats-collected` | 社交数据 |

#### HTML 结构示例

```html
<div class="recipe-page">
  <h1 class="page-title">无油版红烧肉</h1>
  <div class="recipe-cover">
    <img src="https://i2.chuimg.com/recipe_pic/0/f6/4d/100000.1?..." />
  </div>
  <div class="recipe-ingredients">
    <!-- 食材列表 -->
  </div>
  <div class="recipe-steps">
    <!-- 制作步骤 -->
  </div>
  <div class="recipe-tip">
    <!-- 小贴士 -->
  </div>
</div>
```

### 2.4 分页机制

| 项目 | 内容 |
|:-----|:-----|
| 分页方式 | URL 参数或页码链接 |
| 需要进一步分析 | 具体分页参数 |

### 2.5 图片 URL 规律

| 项目 | 内容 |
|:-----|:-----|
| 图片域名 | `https://i2.chuimg.com/` |
| 路径格式 | `/recipe_pic/{path}/{filename}.{ext}?imageView2/...` |
| 可用的图片处理参数 | `imageView2/2/w/{width}/interlace/1/q/75` |

---

## 3. 反爬策略分析

### 3.1 User-Agent 检测

| 项目 | 状态 |
|:-----|:----:|
| 检测 User-Agent | ✅ 是 |
| 需要伪装 | ✅ 是 |

**建议**：使用真实浏览器 User-Agent 轮换

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    # 更多...
]
```

### 3.2 IP 限制

| 项目 | 状态 |
|:-----|:----:|
| IP 限制 | ⚠️ 可能存在 |
| 需要代理 | 后续根据实际情况决定 |

**建议**：
1. 初始阶段不使用代理，设置合理的请求间隔
2. 如遇到 IP 封禁，考虑添加代理池
3. 控制请求频率（建议 2-5 秒间隔）

### 3.3 登录要求

| 项目 | 状态 |
|:-----|:----:|
| 需要登录 | ❌ 否 |
| 基础数据可获取 | ✅ 是 |

**说明**：菜谱详情页无需登录即可访问，部分用户数据可能需要登录。

### 3.4 请求频率限制

| 项目 | 建议 |
|:-----|:-----|
| 请求间隔 | 2-5 秒 |
| 并发请求数 | 1 个（单线程） |
| 每日请求上限 | 初始建议 1000-2000 次 |

### 3.5 其他反爬措施

| 项目 | 状态 | 说明 |
|:-----|:----:|:-----|
| Cookie | 可选 | 首次访问会设置 Cookie |
| Headers | 必须 | 需设置完整的请求头 |
| TLS 指纹 | 未检测 | 无明显 TLS 指纹验证 |

---

## 4. 可爬取的数据字段

### 4.1 必须字段（核心数据）

| 字段 | 来源 | 映射到数据库 |
|:-----|:-----|:-------------|
| 菜谱名称 | `h1.page-title` | `recipes.name` |
| 成品图片 URL | `.recipe-cover img` | `recipes.image_url` |
| 用料列表 | `.recipe-ingredients` | `recipe_ingredients` |
| 制作步骤 | `.recipe-steps` | `recipes.steps` |

### 4.2 可选字段（增强数据）

| 字段 | 来源 | 映射到数据库 |
|:-----|:-----|:-------------|
| 难度等级 | 分析估算 | `recipes.difficulty` |
| 烹饪时长 | 分析步骤估算 | `recipes.cooking_time` |
| 口味标签 | 分析步骤/用料 | `recipes.flavor_tags` |
| 菜系分类 | 分析/默认"家常菜" | `recipes.cuisine_type` |
| 场景分类 | 分析/默认"晚餐" | `recipes.scene_type` |

### 4.3 需要补充的数据

| 字段 | 获取方式 | 说明 |
|:-----|:---------|:-----|
| 点击量 | 随机生成 | 100-50000 之间 |
| 收藏量 | 随机生成 | 点击量的 5%-20% |
| 菜系分类 | 分析或默认 | 根据菜谱名称分析 |
| 难度等级 | 分析或默认 | 根据步骤复杂度分析 |

---

## 5. 爬虫环境准备

### 5.1 需要安装的依赖

```bash
pip install requests beautifulsoup4 lxml pandas
```

| 包名 | 版本 | 用途 |
|:-----|:----:|:-----|
| requests | latest | HTTP 请求 |
| beautifulsoup4 | latest | HTML 解析 |
| lxml | latest | 解析器（速度快） |
| pandas | latest | 数据处理 |

### 5.2 Python 虚拟环境

由于项目已有 `backend_venv`，可在该虚拟环境中安装爬虫依赖：

```bash
# Windows
backend_venv\Scripts\activate

# Linux/Mac
source backend_venv/bin/activate

# 安装依赖
pip install requests beautifulsoup4 lxml pandas
```

### 5.3 工具函数准备

需要创建的工具模块：

| 模块 | 功能 |
|:-----|:-----|
| `request_utils.py` | HTTP 请求封装（UA 轮换、重试） |
| `parser_utils.py` | HTML 解析工具 |
| `data_validator.py` | 数据验证 |

---

## 6. 爬虫策略

### 6.1 数据获取流程

```
1. 获取分类列表 → category/
   ↓
2. 遍历分类，获取菜谱列表 → category/{id}/
   ↓
3. 解析列表页，提取菜谱详情页链接
   ↓
4. 请求菜谱详情页 → recipe/{id}/
   ↓
5. 解析详情页，提取数据
   ↓
6. 保存为 JSON 格式
   ↓
7. 下载图片（可选）
```

### 6.2 初始爬取策略

| 阶段 | 目标 | 数量 |
|:-----|:-----|:----:|
| 测试爬取 | 验证解析逻辑 | 10-50 条 |
| 小批量爬取 | 积累数据 | 500-1000 条 |
| 大批量爬取 | 达到目标 | 10000-20000 条 |

### 6.3 数据存储策略

1. **原始数据**：保存为 JSON 文件（按日期或批次）
2. **清洗后数据**：保存为独立的 JSON 文件
3. **图片文件**：下载到 `data-scripts/spiders/images/` 目录

---

## 7. 风险与注意事项

### 7.1 法律风险

| 风险 | 应对措施 |
|:-----|:---------|
| 版权问题 | 仅用于学习，不商用 |
| robots.txt | 检查并遵守 |

### 7.2 技术风险

| 风险 | 应对措施 |
|:-----|:---------|
| IP 封禁 | 控制频率，使用代理 |
| 网站结构变化 | 定期检查更新选择器 |
| 数据质量问题 | 后续清洗验证 |

### 7.3 数据质量风险

| 风险 | 应对措施 |
|:-----|:---------|
| 缺少关键字段 | 数据清洗时补全 |
| 数据格式不统一 | 统一处理逻辑 |
| 重复数据 | 去重处理 |

---

## 8. 下一步工作

### 8.1 立即执行

- [x] 完成网站分析
- [ ] 安装爬虫依赖
- [ ] 创建爬虫脚本模板
- [ ] 编写测试爬虫（爬取 10 条数据）

### 8.2 后续工作

- [ ] 编写数据清洗脚本
- [ ] 编写数据导入脚本
- [ ] 执行完整爬取
- [ ] 数据验证

---

## 9. 附录

### 9.1 CSS 选择器测试

需要在实际爬取时验证和调整选择器。

### 9.2 备选网站列表

| 网站 | URL | 备注 |
|:-----|:----|:-----|
| 豆果美食 | https://www.douguo.com | 备选 1 |
| 香哈菜谱 | https://www.xiangha.com | 备选 2 |
| 心食谱 | https://www.xinshipu.com | 备选 3 |

### 9.3 参考文档

- Requests: https://docs.python-requests.org/
- BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- lxml: https://lxml.de/

---

**分析完成时间**: 2026-01-30
**分析人员**: Claude Code
**状态**: ✅ 已完成分析，等待测试验证
