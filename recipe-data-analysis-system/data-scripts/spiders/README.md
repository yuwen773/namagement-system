# 爬虫脚本

本目录包含从美食网站爬取菜谱数据的脚本。

## 目标网站

- 下厨房 (xiachufang.com)
- 美食杰 (meishij.net)

## 脚本说明

### recipe_spider.py
主要的菜谱爬虫脚本，功能包括：
- 爬取菜谱列表
- 解析菜谱详情（名称、菜系、难度、食材、步骤、图片）
- 下载菜谱图片
- 保存为 JSON 格式

## 使用方法

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml

# 运行爬虫
python recipe_spider.py
```

## 配置项

- `START_URL`: 起始页面 URL
- `MAX_PAGES`: 最大爬取页数
- `DELAY`: 请求间隔（秒）
- `OUTPUT_FILE`: 输出文件路径

## 注意事项

1. 遵守 robots.txt
2. 设置合理的请求间隔（2-5秒）
3. 处理反爬策略（User-Agent 轮换）
4. 异常处理和重试机制
