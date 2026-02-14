# 景点图片批量添加设计方案

## 需求背景

数据库现有 3700 个景点，均无图片。项目已有 `images_config.py` 配置文件，包含 12 个热门景点的 Unsplash 图片 URL。

## 目标

为所有景点添加封面图和轮播图。

## 方案选择

**采用方案：按类别分配默认图**

- 优先精确匹配景点名称（现有12个配置）
- 未匹配时按景点 `category` 字段分配类别默认图

## 数据设计

### 类别图片配置

| 类别 | 封面图 URL | 轮播图 |
|------|-----------|--------|
| 自然风光 | https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80 | 4张山景/自然 |
| 人文古迹 | https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80 | 4张古建筑 |
| 主题乐园 | https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=800&q=80 | 4张游乐园 |
| 海滩/海滨 | https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80 | 4张海滩 |
| 其他 | https://images.unsplash.com/photo-1473116763241-2e4a44daa1fa?w=800&q=80 | 4张通用风景 |

### 精确匹配景点（12个）

使用 `images_config.py` 中已有配置：
- 故宫、长城、西湖、黄山、九寨沟、鼓浪屿
- 上海迪士尼乐园、张家界国家森林公园、兵马俑
- 桂林山水、丽江古城、三亚湾

## 实现方案

### 实现方式

创建 Django management command：`python manage.py update_attraction_images`

功能：
1. 加载 `images_config.py` 中的精确匹配配置
2. 加载类别默认图片配置
3. 遍历所有未删除景点：
   - 名称精确匹配 → 使用配置图片
   - 未匹配 → 使用类别默认图
4. 批量更新 `cover_image` 和 `images` 字段

### 字段处理

- `cover_image`: 存入完整 Unsplash URL 字符串
- `images`: 存入 JSON 数组 `["url1", "url2", "url3", "url4"]`

### 预期效果

- 12 个精确匹配景点：使用专属图片
- 其余景点：按类别分配统一图片

## 测试验证

1. 运行命令后抽样检查 5-10 个景点
2. 验证 API 返回的图片 URL 是否正确
3. 前端页面展示是否正常

## 实施步骤

1. 创建类别图片配置
2. 编写 `update_attraction_images` management command
3. 执行命令
4. 验证结果
