# CSV数据导入快速开始指南

## 快速开始

### 命令行导入（推荐）

```bash
cd backend
python manage.py import_csv
```

### Python脚本

```bash
cd backend
python run_import.py
```

## CSV文件格式

将CSV文件放在 `backend/data/` 目录下：

```csv
商品ID,商品标题,价格,价格单位,价格描述,卖家昵称,店铺名称,店铺标签,销量,地区,标签,商品属性,图片链接,商品链接
```

**示例**：
```csv
750776311357,万代PG独角兽高达,3599,¥,券后价,小鑫数码,永乐玩具,7年老店,65人付款,广东 深圳,官方立减12%,出售状态:现货|品牌:Bandai,http://img.jpg,http://detail.url
```

## 常用命令

```bash
# 基本导入
python manage.py import_csv

# 指定目录
python manage.py import_csv --dir /path/to/csv

# 试运行（不实际导入）
python manage.py import_csv --dry-run
```

## 数据清洗规则

- ✅ **自动检测表头**：缺失表头的CSV会自动添加
- ✅ **智能填充**：自动填充缺失的标题、店铺、链接
- ✅ **字段截断**：自动截断过长的URL（1000字符）、标题（500字符）
- ✅ **允许重复**：相同商品ID可有多条记录

## 导入结果示例

```
找到 10 个CSV文件
批次号: IMPORT_20260208_214317
成功导入: 10738
跳过记录: 429
错误记录: 0
```

## 验证导入

```bash
python manage.py shell

>>> from products.models import Product
>>> Product.objects.count()  # 总数
10738
>>> Product.objects.filter(batch_no='IMPORT_20260208_214317').count()  # 特定批次
10738
```

---

**快速导入**：
```bash
cd backend && python manage.py import_csv
```
