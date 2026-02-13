# 查询性能优化方案

## 概述

本文档记录了电影票房预测与可视化系统在数据量达到500万+记录时的查询性能优化方案。

## 背景

系统生成了以下数据规模：
- 电影：约9,800部
- 影院：200家
- 票房记录：约580万条

原始查询在管理端Dashboard和票房列表页面出现30秒超时问题。

---

## 问题1：Dashboard概览统计超时

### 问题描述

`GET /visualization/stats/overview/` 接口超时（30秒）

### 根因分析

1. **票房累计计算**：对580万条记录做`SUM(daily_box_office)`聚合
2. **最近记录查询**：在580万条记录上做`order_by('-record_date')` + `select_related`

### 解决方案

#### 1.1 累计票房优化

**原代码**（约30秒超时）：
```python
# 从票房表聚合
total_box_office = BoxOfficeRecord.objects.aggregate(
    total=Coalesce(Sum('daily_box_office'), Value(Decimal('0')))
)['total']
```

**优化后**（毫秒级）：
```python
# 从电影表获取（数据在生成时已计算好）
total_box_office = Movie.objects.aggregate(
    total=Coalesce(Sum('box_office_total'), Value(Decimal('0')))
)['total'] * 10000  # 万元转元
```

#### 1.2 最近记录优化

**原代码**（超时）：
```python
recent_records = BoxOfficeRecord.objects.select_related(
    'movie', 'cinema'
).order_by('-record_date')[:5]
```

**优化后**（0.15秒）：
```python
# 先获取ID列表，再关联详情
recent_ids = list(BoxOfficeRecord.objects.values_list('id', flat=True).order_by('-record_date')[:5])
recent_records = BoxOfficeRecord.objects.filter(id__in=recent_ids).select_related('movie', 'cinema')
```

---

## 问题2：票房列表超时

### 问题描述

`GET /boxoffice/` 列表接口超时（30秒+）

### 根因分析

1. **分页方式**：使用OFFSET分页，对大数据集效率低
2. **COUNT查询**：每次请求都执行`COUNT(*)`，对580万条记录约3秒
3. **关联查询**：Django ORM的`select_related`在大量数据上性能差

### 解决方案

#### 2.1 游标分页替代OFFSET

```python
# 第一页：从最新开始
if page == 1:
    cursor.execute('''
        SELECT b.id, b.record_date, ...
        FROM boxoffice_records b
        LEFT JOIN movies m ON b.movie_id = m.id
        LEFT JOIN cinemas c ON b.cinema_id = c.id
        ORDER BY b.id DESC
        LIMIT %s
    ''', [page_size])

# 后续页：使用last_id游标
else:
    last_id = request.query_params.get('last_id')
    cursor.execute('''
        SELECT b.id, b.record_date, ...
        FROM boxoffice_records b
        LEFT JOIN movies m ON b.movie_id = m.id
        LEFT JOIN cinemas c ON b.cinema_id = c.id
        WHERE b.id < %s
        ORDER BY b.id DESC
        LIMIT %s
    ''', [last_id, page_size])
```

#### 2.2 表统计信息替代COUNT

```python
# 原：COUNT(*) - 约3秒
cursor.execute('SELECT COUNT(*) FROM boxoffice_records')

# 新：information_schema - 毫秒级
cursor.execute('''
    SELECT TABLE_ROWS FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'boxoffice_records'
''')
```

#### 2.3 原始SQL替代Django ORM

```python
# 原：Django ORM - 超时
queryset = BoxOfficeRecord.objects.select_related('movie', 'cinema').all()

# 新：原始SQL - 毫秒级
cursor.execute('''
    SELECT b.id, b.record_date, b.daily_box_office, b.screening_count, b.audience_count,
           b.created_at,
           m.id as movie_id, m.title as movie_title,
           c.id as cinema_id, c.name as cinema_name
    FROM boxoffice_records b
    LEFT JOIN movies m ON b.movie_id = m.id
    LEFT JOIN cinemas c ON b.cinema_id = c.id
    ORDER BY b.id DESC
    LIMIT 10
''')
```

---

## 性能对比

### Dashboard概览统计

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 响应时间 | 30秒+超时 | **0.15秒** |

### 票房列表

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 第一页响应时间 | 30秒+超时 | **0.02秒** |
| 后续页响应时间 | 30秒+超时 | **0.00秒** |

---

## 技术要点总结

### 1. 数据结构设计

- **预计算**：在数据生成时计算好累计值，避免运行时聚合
- **索引**：为常用查询字段添加索引
- **分区**：大数据表可考虑按时间分区

### 2. 查询优化

- **游标分页**：使用ID或时间戳游标，替代OFFSET
- **原始SQL**：复杂查询可使用原始SQL，避免ORM开销
- **近似值**：对大数据集使用近似统计（如information_schema）替代精确COUNT

### 3. 缓存策略

- **Redis缓存**：对不常变化的数据使用Redis缓存
- **查询缓存**：利用数据库查询缓存

### 4. 监控告警

- **慢查询日志**：开启MySQL慢查询日志
- **APM工具**：使用SkyWalking、Pinpoint等APM工具监控

---

## 相关文件

- `backend/visualization/views.py` - Dashboard API优化
- `backend/boxoffice/views.py` - 票房列表API优化
- `backend/scripts/data_generator.py` - 数据生成工具

---

## 参考资料

- [MySQL ORDER BY 优化](https://dev.mysql.com/doc/refman/8.0/en/order-by-optimization.html)
- [MySQL LIMIT 优化](https://dev.mysql.com/doc/refman/8.0/en/limit-optimization.html)
- [Django ORM 性能优化](https://docs.djangoproject.com/en/4.2/topics/db/optimization/)
