# dataSource 数据集导入评估报告

生成时间：2026-02-25  
项目目录：`D:\work\code\personal\namagement-system\intangible-cultural-heritage-system`

## 1. 数据源清单与规模

### 1.1 结构化数据（可入库记录）
- `dataSource/archive (2)/elements.csv`：562
- `dataSource/archive (3)/ich001.csv`：849
- `dataSource/archive (3)/Cultural_Heritage_Video_Dataset.csv`：2000
- `dataSource/archive (5)/IICH_dataset.csv`：500
- `dataSource/第四版.jsonl`：2682
- `dataSource/IhChina_2006-2021`（Shapefile/DBF）：3610

结构化总计：**10203 条**

### 1.2 图谱与素材
- `dataSource/archive (2)/graph_en.json`
  - nodes：2424
  - edges：19945
- 图片素材：
  - `archive (3)/Images` + `archive (4)/Cultural dataset` 合计：152 张

## 2. 质量评估结论

### 2.1 高质量（推荐主导入）
- `ich001.csv`：字段完整、主键稳定、全球国家覆盖广，适合作为全球主档案。
- `elements.csv`：结构规范、重复低，可作为 UNESCO 概念标签增强源。
- `IhChina_2006-2021`：字段完整度高（核心字段缺失接近 0），适合作为中国专题地理层。

### 2.2 中质量（场景增强）
- `graph_en.json`：适合做关系图谱增强（概念关联、知识网络）。
- `Cultural_Heritage_Video_Dataset.csv`：适合传播分析，不建议作为非遗主表。
- `第四版.jsonl`：问答数据可用于检索/问答功能，主表价值有限。

### 2.3 低质量（限制使用）
- `IICH_dataset.csv`：重复率高（仅建议用于测试或演示，不纳入核心统计）。

## 3. 是否达到 1w 条硬性要求
- 结论：**已达到**  
- 依据：结构化记录总量 **10203**（已超过 10000）

## 4. 导入策略（落地建议）

### 4.1 优先级
1. P0：`ich001.csv` + `elements.csv` + `IhChina_2006-2021`
2. P1：`graph_en.json` + `Cultural_Heritage_Video_Dataset.csv` + `第四版.jsonl`
3. P2：`IICH_dataset.csv`（仅测试）

### 4.2 统一处理流程
1. 文件扫描与任务登记（hash、大小、mtime）
2. 分格式解析（CSV/JSONL/JSON/SHP+DBF）
3. 原始层入库（raw）
4. 清洗标准化（国家、分类、文本、坐标）
5. 去重合并（core）
6. 统计聚合（mart）
7. 生成导入日志与错误报告

### 4.3 地图范围适配
- 主地图：**全球国家级**
- 中国专题：保留 `IhChina_2006-2021` 省市点位层作为子专题

## 5. 风险与注意事项
- `IhChina_2006-2021` 为 Shapefile，导入需 GIS 解析链路（建议 GDAL/GeoPandas 或 DBF 解析工具）。
- 多源国家字段存在命名差异，需统一到 ISO-3166 代码。
- 问答/视频类数据和主档案语义不同，需分表管理，避免污染核心指标。
- `IICH_dataset.csv` 高重复，默认不进入核心报表。

## 6. 最终建议
- 按 P0 源先完成“核心数据闭环”，先稳定全球+中国两层可视化。
- P1 源逐步接入增强分析能力（关系图谱/传播分析/问答）。
- 保持“全量首次导入 + hash 增量更新”模式，确保可追溯与可回滚。
