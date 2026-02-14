# 景点评论批量生成设计方案

**日期**: 2025-02-13
**目标**: 为每个景点增加 10-15 条评论数据

---

## 1. 需求概述

当前系统的景点没有对应的评论数据，需要批量生成评论以：
- 展示景点评分和用户反馈
- 测试评论功能完整性
- 丰富前端展示效果

---

## 2. 数据库表结构

### 2.1 评论表 (comments_comment)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | FK -> UserProfile | 关联用户 |
| attraction_id | FK -> Attraction | 关联景点 |
| content | TextField | 评论内容 |
| rating | IntegerField | 评分 (1-5) |
| status | CharField | 状态: PENDING/APPROVED/REJECTED |
| is_deleted | BooleanField | 逻辑删除 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

### 2.2 景点表 (attractions_attraction)

关键字段：id, name, category, region

### 2.3 用户表 (accounts_userprofile)

关键字段：id, username, real_name

---

## 3. 实现方案

### 3.1 创建 Django Management Command

**文件位置**: `backend/comments/management/commands/import_comments.py`

### 3.2 评论内容模板

```python
COMMENT_TEMPLATES = {
    "自然风光": [
        "风景太美了，空气清新，值得一去！",
        "自然风光绝佳，拍照超级出片",
        "环境很好，就是人有点多",
        "值得推荐，风景如画",
        ...
    ],
    "人文古迹": [
        "历史文化底蕴深厚，长知识了",
        "建筑风格独特，很震撼",
        "讲解很详细，了解了很多历史",
        ...
    ],
    "主题乐园": [
        "游乐设施很丰富，玩得很开心",
        "适合亲子游，孩子特别喜欢",
        "氛围感满满，体验超棒",
        ...
    ],
}
```

### 3.3 评分分布

| 评分 | 比例 |
|------|------|
| 5分 | 50% |
| 4分 | 30% |
| 3分 | 15% |
| 2分 | 3% |
| 1分 | 2% |

### 3.4 状态分布

| 状态 | 比例 |
|------|------|
| APPROVED | 85% |
| PENDING | 15% |

---

## 4. 命令参数设计

```bash
# 为所有景点生成评论（每个景点10条）
python manage.py import_comments

# 为所有景点生成评论（每个景点15条）
python manage.py import_comments --count 15

# 为指定景点生成评论
python manage.py import_comments --attraction-id 1

# 重新生成（先清空再生成）
python manage.py import_comments --clear
```

---

## 5. 实现步骤

1. 创建命令文件结构和基础框架
2. 实现用户和景点数据获取
3. 实现评论模板和内容生成
4. 实现评分和状态随机分配逻辑
5. 实现批量插入数据库
6. 添加命令行参数支持

---

## 6. 验收标准

- [ ] 命令可正常执行，无报错
- [ ] 每个景点生成 10-15 条评论（可配置）
- [ ] 评论内容真实可读，与景点类别相关
- [ ] 评分分布符合预期（好评为主）
- [ ] 状态分布符合预期（大部分 APPROVED）
- [ ] 可通过参数控制生成数量和范围
