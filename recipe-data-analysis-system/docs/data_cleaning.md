# 数据清洗工作记录

> 更新日期: 2026-01-30

## 任务背景

**数据集**: `recipe_corpus_full.json` (1.8GB, 1,520,327 条菜谱记录)

**目标**: 清洗并提取 20,000 条完整数据用于 MySQL 数据库入库

**数据来源**: 下厨房 (xiachufang.com) - 清华大学/Baidu/BIGAI 联合发布的中文菜谱语料库

## 数据集分析

### 文件格式
- **格式**: JSON Lines (每行一个 JSON 对象)
- **编码**: UTF-8
- **记录数**: 1,520,327 条
- **平均长度**: 224 字符/条

### 字段结构
| 字段名 | 类型 | 说明 | 映射目标 |
|:-------|:-----|:-----|:---------|
| `name` | string | 菜谱名称 | `recipes.name` |
| `dish` | string | 菜品类型 | `recipes.cuisine_type` |
| `description` | string | 描述 | (可选) |
| `recipeIngredient` | array | 食材列表 | `recipe_ingredients` |
| `recipeInstructions` | array | 制作步骤 | `recipes.steps` |
| `author` | string | 作者ID | (不需要) |
| `keywords` | array | 关键词 | (不需要) |

## 解决方案

### 脚本实现

**文件**: `data-scripts/cleaning/clean_large_dataset.py`

**核心功能**:
1. **格式自动检测** - 自动识别 JSON Lines / JSON Array 格式
2. **流式读取** - 逐行解析，避免内存溢出
3. **字段名映射** - 支持 `recipeIngredient` → `ingredients`, `recipeInstructions` → `steps`
4. **数据验证** - 确保数据库必需字段完整
5. **智能去重** - 基于 MD5 哈希去重
6. **进度显示** - 实时显示处理进度和有效率
7. **可配置** - 支持自定义目标数量

### 数据库必需字段验证

| 字段 | 验证规则 | 默认值 |
|:-----|:---------|:-------|
| `name` | 必填，非空 | 无（跳过） |
| `ingredients` | 必填，至少 1 条 | 无（跳过） |
| `steps` | 必填，至少 1 步 | 无（跳过） |
| `cuisine_type` | 可选 | "家常菜" |
| `scene_type` | 可选 | "晚餐" |
| `difficulty` | 可选 | "medium" |
| `cooking_time` | 可选 | 30 (分钟) |
| `image_url` | 可选 | "" |

## 使用方法

### 安装依赖
```bash
pip install ijson
```

### 运行清洗脚本
```bash
cd data-scripts/cleaning

# 清洗 20,000 条数据（默认）
python clean_large_dataset.py ../dataset/recipe_corpus_full.json ../output/cleaned_20k_recipes.json

# 自定义目标数量
python clean_large_dataset.py ../dataset/recipe_corpus_full.json ../output/cleaned_10k_recipes.json --target 10000
```

### 输出文件
- `cleaned_20k_recipes.json` - 清洗后的数据（含 metadata）
- `cleaning_report.json` - 详细清洗报告

## 技术要点

### 1. 流式处理大文件
```python
# 逐行读取，避免一次性加载到内存
with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        recipe = json.loads(line.strip())
        # 处理单条记录
```

### 2. 字段名兼容
```python
def _extract_ingredients_from_recipe(self, recipe):
    # 支持多种字段名
    ingredients = recipe.get('ingredients') \
        or recipe.get('recipeIngredient') \
        or recipe.get('recipe_ingredients') \
        or []
    return self._normalize_ingredients(ingredients)
```

### 3. 数据验证
```python
def _validate_recipe(self, recipe):
    # 必填字段检查
    if not recipe.get('name'):
        return False, "缺少菜谱名称"

    ingredients = self._extract_ingredients_from_recipe(recipe)
    if not ingredients or len(ingredients) == 0:
        return False, "缺少食材信息"

    steps = self._extract_steps_from_recipe(recipe)
    if not steps or len(steps) == 0:
        return False, "缺少制作步骤"

    return True, None
```

## 数据质量指标

根据初步测试：
- **原始数据**: 1,550,151 条
- **重复数据**: ~485,706 条 (~31%)
- **无效数据**: ~1,064,445 条 (缺少必需字段)
- **预期有效数据**: ~20,000 条

## 后续步骤

1. ✅ **运行清洗脚本** - 已提取 20,000 条完整数据
2. ✅ **数据导入** - 已使用 `importing/import_recipes.py` 导入 MySQL
3. ✅ **数据验证** - 已验证入库数据的完整性

> 详见: [数据导入工作记录](./data_import.md)

## 相关文件

| 文件 | 说明 |
|:-----|:-----|
| `data-scripts/cleaning/clean_large_dataset.py` | 主清洗脚本 |
| `data-scripts/cleaning/clean_recipes.py` | 小数据集清洗脚本 |
| `data-scripts/cleaning/README.md` | 使用文档 |
| `data-scripts/importing/import_recipes.py` | 数据导入脚本 |
| `memory-bank/implementation-plan.md` | 实施计划步骤 3.3 |

## 参考资源

- [下厨房菜谱语料库](https://counterfactual-recipe-generation.github.io/dataset_en.html)
- [ijson 文档](https://pypi.org/project/ijson/) - 流式 JSON 解析库
- 数据库表结构: `memory-bank/architecture.md`
