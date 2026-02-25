# 待导入数据说明文档

**生成时间**: 2026-02-25

---

## 一、未导入的数据

| 数据源文件 | 行数 | 已导入 | 缺失 | 状态 |
|-----------|------|--------|------|------|
| gas_consumption.csv | 27,164 | 21,720 | **5,444** | ❌ 部分导入 |
| water_consumption.csv | 245,040 | 244,029 | 1,011 | ⚠️ 基本完整 |
| building_meta.csv | 64 | 3 | **61** | ❌ 仅导入3栋 |
| campus_meta.csv | 5 | 5 | 0 | ✅ 完整 |
| calender.csv | 2,312 | - | **2,312** | ❌ 无对应表 |
| events.csv | 106 | - | **106** | ❌ 无对应表 |
| nmi_meta.csv | 14 | - | **14** | ❌ 无对应表 |

---

## 二、缺失的数据库表

以下数据源文件缺少对应的数据库表：

| 数据源文件 | 需要创建的表 | 说明 |
|-----------|-------------|------|
| calender.csv | `em_calendars` | 日历数据（假期/学期/考试） |
| events.csv | `em_events` | 设备事件记录 |
| nmi_meta.csv | `em_nmi_metas` | NMI 元数据（或合并到设备表） |

---

## 三、导入问题说明

### gas_consumption.csv
- **问题**: CSV 使用 `campus_id` 字段，数据库需要 `device_id`
- **数据分布**:
  - campus_id=1 (Bundoora): 23,111 行
  - campus_id=3 (Bendigo): 4,053 行
- **解决方案**: 需要配置 campus_id → device_id 映射

### building_meta.csv
- **问题**: 仅导入 3 栋建筑，CSV 有 64 条
- **解决方案**: 补充导入剩余 61 栋建筑

---

## 四、数据库当前状态

```
能源数据: 265,749 条
  - WATER: 244,029 条
  - GAS:   21,720 条
  - ELECTRICITY: 0 条

建筑层级:
  - 校区: 5 个
  - 建筑: 3 栋 (应导入 64 栋)
  - 楼层: 5 层
  - 房间: 5 间

设备: 19 台
  - WATER: 16 台
  - ELECTRICITY: 1 台
  - GAS: 2 台
```
