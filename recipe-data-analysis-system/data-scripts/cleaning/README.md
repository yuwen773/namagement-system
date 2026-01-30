# 数据清洗脚本

本目录包含数据清洗和标准化脚本。

## 清洗任务

1. **去重处理** - 移除重复的菜谱记录
2. **缺失值处理** - 补全或删除缺失字段的记录
3. **格式统一** - 统一数据格式（难度、时长、单位等）
4. **数据验证** - 验证数据的完整性和合理性
5. **食材提取** - 从食材描述中提取标准化食材列表

## 脚本说明

### clean_recipes.py
**适用场景**: 小数据集（一次性加载到内存）

处理流程：
1. 读取爬取的原始数据
2. 检测并移除重复记录
3. 补全缺失字段
4. 统一数据格式
5. 验证数据完整性
6. 输出清洗后的数据

使用方法：
```bash
cd data-scripts/cleaning
python clean_recipes.py input.json output.json
```

---

### clean_large_dataset.py
**适用场景**: 大数据集（流式处理 1.8GB+ JSON 文件）

核心功能：
- **流式读取**：使用 `ijson` 库逐条解析，避免内存溢出
- **智能去重**：基于 `recipe_id` 和菜谱名称 MD5 哈希
- **数据验证**：确保数据库必需字段完整
- **自动补全**：缺失字段使用合理默认值
- **进度显示**：实时显示清洗进度和有效率
- **可配置**：支持自定义目标数量和批次大小

数据库必需字段验证：
| 字段 | 要求 | 默认值 |
|:-----|:-----|:-------|
| name | 必填 | 无（缺失则跳过） |
| ingredients | 至少 1 条 | 无（缺失则跳过） |
| steps | 至少 1 步 | 无（缺失则跳过） |
| cuisine_type | 可选 | "家常菜" |
| scene_type | 可选 | "晚餐" |
| difficulty | 可选 | "medium" |
| cooking_time | 可选 | 30 |
| image_url | 可选 | "" |

使用方法：
```bash
cd data-scripts/cleaning

# 安装依赖（推荐）
pip install ijson

# 清洗 20,000 条数据（默认）
python clean_large_dataset.py ../dataset/recipe_corpus_full.json ../output/cleaned_20k_recipes.json

# 自定义目标数量
python clean_large_dataset.py ../dataset/recipe_corpus_full.json ../output/cleaned_10k_recipes.json --target 10000

# 查看帮助
python clean_large_dataset.py --help
```

输出文件：
- `cleaned_20k_recipes.json` - 清洗后的数据（含 metadata）
- `cleaning_report.json` - 详细清洗报告

---

## 清洗规则

- 菜谱名称：去除多余空格和特殊字符
- 难度等级：统一为"简单"/"中等"/"困难"
- 烹饪时长：统一为分钟数
- 食材用量：标准化单位（克、毫升、个等）
- 图片URL：验证可访问性
