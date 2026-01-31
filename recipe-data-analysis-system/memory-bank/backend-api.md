# 菜谱数据分析系统 - 后端 API 接口文档

> 版本：v1.0
> 更新日期：2026-01-31
> 基础路径：`http://localhost:8000/api`

---

## 目录

1. [通用说明](#通用说明)
2. [用户认证模块 (accounts)](#用户认证模块-accounts)
3. [菜谱模块 (recipes)](#菜谱模块-recipes)
4. [分类模块 (categories)](#分类模块-categories)
5. [食材模块 (ingredients)](#食材模块-ingredients)
6. [收藏模块 (favorites)](#收藏模块-favorites)
7. [数据分析模块 (analytics)](#数据分析模块-analytics)

---

## 通用说明

### 统一响应格式

所有 API 接口返回统一的 JSON 格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {}
}
```

### 响应代码说明

| Code | HTTP Status | 说明 |
|:-----|:-----------|:-----|
| 200  | 200        | 操作成功 |
| 201  | 201        | 创建成功 |
| 400  | 400        | 请求参数错误 |
| 401  | 401        | 未认证/认证失败 |
| 403  | 403        | 无权限 |
| 404  | 404        | 资源不存在 |
| 500  | 500        | 服务器内部错误 |

### 认证方式

使用 JWT Token 认证，需要在请求头中携带：

```
Authorization: Bearer <access_token>
```

### 分页参数

| 参数      | 类型   | 默认值 | 说明           |
|:---------|:-------|:-------|:---------------|
| page      | int    | 1      | 页码           |
| page_size | int    | 20     | 每页数量（最大100） |

### 分页响应格式

```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "next": null,
        "previous": "http://localhost:8000/api/recipes/?page=1",
        "results": []
    }
}
```

---

## 用户认证模块 (accounts)

### 1. 用户注册

**接口地址：** `POST /api/accounts/register/`

**请求参数：**

| 参数              | 类型   | 必填 | 说明                     |
|:------------------|:-------|:-----|:-------------------------|
| username          | string | 是   | 用户名（3-20个字符）      |
| password          | string | 是   | 密码（至少8位）           |
| password_confirm  | string | 是   | 确认密码                 |
| email             | string | 否   | 邮箱                     |

**请求示例：**
```json
{
    "username": "testuser",
    "password": "password123",
    "password_confirm": "password123",
    "email": "test@example.com"
}
```

**成功响应（201）：**
```json
{
    "code": 201,
    "message": "注册成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "is_active": true,
        "created_at": "2026-01-30T12:00:00Z"
    }
}
```

**错误响应（400）：**
```json
{
    "code": 400,
    "message": "参数验证失败",
    "errors": {
        "username": ["该用户名已被注册"]
    }
}
```

---

### 2. 用户登录

**接口地址：** `POST /api/accounts/login/`

**请求参数：**

| 参数     | 类型   | 必填 | 说明   |
|:---------|:-------|:-----|:-------|
| username | string | 是   | 用户名 |
| password | string | 是   | 密码   |

**请求示例：**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "...",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "is_active": true
        }
    }
}
```

---

### 3. 获取当前用户信息

**接口地址：** `GET /api/accounts/me/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "is_active": true,
        "created_at": "2026-01-30T12:00:00Z"
    }
}
```

---

### 4. 更新用户资料

**接口地址：** `PUT /api/accounts/me/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**请求参数：**

| 参数        | 类型   | 必填 | 说明                       |
|:------------|:-------|:-----|:---------------------------|
| nickname    | string | 否   | 昵称（最大50个字符）        |
| bio         | string | 否   | 个人简介（最大500个字符）   |
| avatar_url  | string | 否   | 头像 URL                   |
| phone       | string | 否   | 手机号（需符合格式且唯一）  |

**请求示例：**
```json
{
    "nickname": "美食家小王",
    "bio": "热爱烹饪，喜欢尝试各种菜谱"
}
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "user_id": 1,
        "username": "testuser",
        "nickname": "美食家小王",
        "phone": null,
        "bio": "热爱烹饪，喜欢尝试各种菜谱",
        "avatar_url": "",
        "created_at": "2026-01-30T12:00:00Z"
    }
}
```

---

### 5. 修改密码

**接口地址：** `PUT /api/accounts/password/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**请求参数：**

| 参数                | 类型   | 必填 | 说明           |
|:--------------------|:-------|:-----|:---------------|
| old_password        | string | 是   | 旧密码         |
| new_password        | string | 是   | 新密码（至少8位） |
| new_password_confirm | string | 是   | 确认新密码     |

**请求示例：**
```json
{
    "old_password": "oldpass123",
    "new_password": "newpass456",
    "new_password_confirm": "newpass456"
}
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "密码修改成功",
    "data": null
}
```

---

### 6. 角色检查

**接口地址：** `GET /api/accounts/role-check/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "角色检查成功",
    "data": {
        "username": "testuser",
        "role": "user",
        "is_admin": false,
        "can_access_admin": false
    }
}
```

---

### 7. 管理员统计

**接口地址：** `GET /api/accounts/admin/stats/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**权限要求：** 仅管理员可访问

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "total_users": 150,
        "active_users": 142,
        "admin_count": 5,
        "user_count": 145,
        "today_new_users": 3
    }
}
```

**错误响应（403）：**
```json
{
    "code": 403,
    "message": "权限不足，仅管理员可访问",
    "data": null
}
```

---

### 8. 健康检查

**接口地址：** `GET /api/accounts/health/`

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "accounts 模块运行正常",
    "data": {
        "status": "healthy",
        "module": "accounts"
    }
}
```

---

## 菜谱模块 (recipes)

### 1. 菜谱列表

**接口地址：** `GET /api/recipes/`

**请求参数：**

| 参数           | 类型   | 必填 | 说明 |
|:---------------|:-------|:-----|:-----|
| page           | int    | 否   | 页码（默认1） |
| page_size      | int    | 否   | 每页数量（默认20，最大100） |
| ordering       | string | 否   | 排序字段（默认-created_at） |
| cuisine_type   | string | 否   | 菜系筛选 |
| difficulty     | string | 否   | 难度筛选（easy/medium/hard） |
| scene_type     | string | 否   | 场景筛选 |
| target_audience | string | 否   | 人群筛选 |

**排序字段可选值：**
- `view_count`, `-view_count` - 按点击量
- `favorite_count`, `-favorite_count` - 按收藏量
- `created_at`, `-created_at` - 按创建时间
- `cooking_time`, `-cooking_time` - 按烹饪时长

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "宫保鸡丁",
                "cuisine_type": "川菜",
                "difficulty": "medium",
                "cooking_time": 30,
                "image_url": "/media/recipes/1_xxx.jpg",
                "view_count": 100,
                "favorite_count": 20
            }
        ]
    }
}
```

---

### 2. 菜谱搜索

**接口地址：** `GET /api/recipes/search/`

**请求参数：**

| 参数        | 类型   | 必填 | 说明 |
|:------------|:-------|:-----|:-----|
| keyword     | string | 是   | 搜索关键词 |
| search_type | string | 否   | 搜索类型（默认name） |
| page        | int    | 否   | 页码（默认1） |
| page_size   | int    | 否   | 每页数量（默认20，最大100） |

**搜索类型可选值：**
- `name` - 按菜谱名称搜索（默认）
- `ingredient` - 按食材搜索

**请求示例：**
```
GET /api/recipes/search/?keyword=鸡肉&search_type=name
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "搜索成功",
    "data": {
        "count": 10,
        "keyword": "鸡肉",
        "search_type": "name",
        "results": [...]
    }
}
```

---

### 3. 菜谱详情

**接口地址：** `GET /api/recipes/{recipe_id}/`

**路径参数：**

| 参数       | 类型 | 必填 | 说明   |
|:-----------|:-----|:-----|:-------|
| recipe_id  | int  | 是   | 菜谱ID |

**功能说明：**
- 返回菜谱完整信息（基本信息、食材列表、详细步骤等）
- 自动增加菜谱点击量计数
- 记录用户浏览行为到行为日志表

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "id": 1,
        "name": "宫保鸡丁",
        "cuisine_type": "川菜",
        "difficulty": "medium",
        "cooking_time": 30,
        "image_url": "/media/recipes/1_xxx.jpg",
        "steps": "详细步骤...",
        "flavor_tags": "辣,甜",
        "view_count": 101,
        "favorite_count": 20,
        "ingredients": [
            {
                "id": 1,
                "name": "鸡肉",
                "amount": "300g",
                "category": "meat"
            }
        ],
        "flavor_list": ["辣", "甜"]
    }
}
```

**错误响应（404）：**
```json
{
    "code": 404,
    "message": "菜谱不存在",
    "data": null
}
```

---

### 4. 热门菜谱

**接口地址：** `GET /api/recipes/hot/`

**请求参数：**

| 参数    | 类型   | 必填 | 说明 |
|:--------|:-------|:-----|:-----|
| sort_by | string | 否   | 排序方式（默认view_count） |
| limit   | int    | 否   | 返回数量（默认20，最大50） |

**排序方式可选值：**
- `view_count` - 按点击量排序（默认）
- `favorite_count` - 按收藏量排序

**请求示例：**
```
GET /api/recipes/hot/?sort_by=favorite_count&limit=10
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "sort_by": "view_count",
        "limit": 20,
        "count": 20,
        "results": [...]
    }
}
```

---

### 5. 通用图片上传

**接口地址：** `POST /api/recipes/upload-image/`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**请求参数：**

| 参数   | 类型 | 必填 | 说明         |
|:-------|:-----|:-----|:-------------|
| image  | file | 是   | 图片文件     |

**文件限制：**
- 格式：jpg、jpeg、png、webp
- 大小：最大 5MB

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "上传成功",
    "data": {
        "url": "/media/recipes/temp_1706582400.jpg",
        "filename": "temp_1706582400.jpg"
    }
}
```

---

### 6. 菜谱图片上传

**接口地址：** `POST /api/recipes/{recipe_id}/upload-image/`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**路径参数：**

| 参数      | 类型 | 必填 | 说明   |
|:----------|:-----|:-----|:-------|
| recipe_id | int  | 是   | 菜谱ID |

**请求参数：**

| 参数   | 类型 | 必填 | 说明     |
|:-------|:-----|:-----|:---------|
| image  | file | 是   | 图片文件 |

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "上传成功",
    "data": {
        "url": "/media/recipes/1_1706582400.jpg",
        "recipe_id": 1
    }
}
```

---

### 7. 健康检查

**接口地址：** `GET /api/recipes/health/`

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "recipes 模块运行正常",
    "data": {
        "status": "healthy",
        "module": "recipes"
    }
}
```

---

## 分类模块 (categories)

### 1. 分类列表

**接口地址：** `GET /api/categories/`

**请求参数：**

| 参数 | 类型   | 必填 | 说明 |
|:-----|:-------|:-----|:-----|
| type | string | 否   | 分类类型筛选 |

**分类类型可选值：**
- `cuisine` - 菜系分类
- `scene` - 场景分类
- `crowd` - 人群分类
- `taste` - 口味分类
- `difficulty` - 难度分类

**请求示例：**
```
GET /api/categories/?type=cuisine
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": [
        {
            "id": 1,
            "name": "川菜",
            "type": "cuisine",
            "sort_order": 1
        },
        {
            "id": 2,
            "name": "粤菜",
            "type": "cuisine",
            "sort_order": 2
        }
    ]
}
```

---

### 2. 按类型获取分类

**接口地址：** `GET /api/categories/{category_type}/`

**路径参数：**

| 参数           | 类型   | 必填 | 说明     |
|:---------------|:-------|:-----|:---------|
| category_type  | string | 是   | 分类类型 |

**分类类型可选值：**
- `cuisine` - 菜系分类
- `scene` - 场景分类
- `crowd` - 人群分类
- `taste` - 口味分类
- `difficulty` - 难度分类

**请求示例：**
```
GET /api/categories/cuisine/
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": [
        {
            "id": 1,
            "name": "川菜",
            "type": "cuisine",
            "sort_order": 1
        }
    ]
}
```

---

## 食材模块 (ingredients)

### 1. 食材列表

**接口地址：** `GET /api/ingredients/`

**请求参数：**

| 参数     | 类型   | 必填 | 说明 |
|:---------|:-------|:-----|:-----|
| category | string | 否   | 食材分类筛选 |
| search   | string | 否   | 搜索食材名称（模糊匹配） |
| page     | int    | 否   | 页码（默认1） |
| page_size| int    | 否   | 每页数量（默认20，最大100） |

**食材分类可选值：**
- `vegetable` - 蔬菜
- `meat` - 肉类
- `seafood` - 海鲜
- `seasoning` - 调料
- `fruit` - 水果
- `grain` - 谷物
- `dairy` - 乳制品
- `other` - 其他

**请求示例：**
```
GET /api/ingredients/?category=meat&search=鸡
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "鸡肉",
                "category": "meat",
                "category_display": "肉类"
            }
        ]
    }
}
```

---

## 收藏模块 (favorites)

### 1. 收藏菜谱

**接口地址：** `POST /api/favorites/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**请求参数：**

| 参数      | 类型 | 必填 | 说明   |
|:----------|:-----|:-----|:-------|
| recipe_id | int  | 是   | 菜谱ID |

**请求示例：**
```json
{
    "recipe_id": 1
}
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "收藏成功",
    "data": {
        "id": 1,
        "recipe": {...},
        "created_at": "2026-01-30T12:00:00Z"
    }
}
```

**错误响应（400）：**
```json
{
    "code": 400,
    "message": "已经收藏过该菜谱",
    "data": null
}
```

---

### 2. 收藏列表

**接口地址：** `GET /api/favorites/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**请求参数：**

| 参数     | 类型   | 必填 | 说明 |
|:---------|:-------|:-----|:-----|
| page     | int    | 否   | 页码（默认1） |
| page_size| int    | 否   | 每页数量（默认20，最大100） |
| ordering | string | 否   | 排序字段（默认-created_at） |

**排序字段可选值：**
- `created_at` - 按收藏时间升序
- `-created_at` - 按收藏时间降序（默认）

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "recipe": {...},
                "created_at": "2026-01-30T12:00:00Z"
            }
        ]
    }
}
```

---

### 3. 取消收藏

**接口地址：** `DELETE /api/favorites/{recipe_id}/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**

| 参数      | 类型 | 必填 | 说明   |
|:----------|:-----|:-----|:-------|
| recipe_id | int  | 是   | 菜谱ID |

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "取消收藏成功",
    "data": null
}
```

**错误响应（400）：**
```json
{
    "code": 400,
    "message": "未收藏该菜谱",
    "data": null
}
```

---

### 4. 检查收藏状态

**接口地址：** `GET /api/favorites/check/{recipe_id}/`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**

| 参数      | 类型 | 必填 | 说明   |
|:----------|:-----|:-----|:-------|
| recipe_id | int  | 是   | 菜谱ID |

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "is_favorited": true,
        "recipe_id": 1
    }
}
```

---

## 数据分析模块 (analytics)

### 1. 菜系分布分析

**接口地址：** `GET /api/analytics/cuisines/`

**功能说明：**
- 统计各菜系的菜谱数量
- 计算占比百分比（保留两位小数）
- 按数量降序排列

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取菜系分布数据成功",
    "data": [
        {
            "name": "川菜",
            "count": 3500,
            "percentage": 17.5
        },
        {
            "name": "粤菜",
            "count": 2800,
            "percentage": 14.0
        }
    ]
}
```

---

### 2. 难度等级统计

**接口地址：** `GET /api/analytics/difficulty/`

**功能说明：**
- 统计各难度等级的菜谱数量和占比
- 计算各难度等级的平均烹饪时长
- 按数量降序排列

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取难度统计数据成功",
    "data": [
        {
            "name": "简单",
            "value": "easy",
            "count": 5000,
            "percentage": 25.0,
            "avg_cooking_time": 20
        },
        {
            "name": "中等",
            "value": "medium",
            "count": 8000,
            "percentage": 40.0,
            "avg_cooking_time": 35
        },
        {
            "name": "困难",
            "value": "hard",
            "count": 7000,
            "percentage": 35.0,
            "avg_cooking_time": 60
        }
    ]
}
```

---

### 3. 口味偏好分析

**接口地址：** `GET /api/analytics/flavors/`

**功能说明：**
- 统计各口味标签的菜谱数量
- 计算占比百分比
- 按数量降序排列

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取口味偏好数据成功",
    "data": [
        {
            "name": "辣",
            "count": 8000,
            "percentage": 40.0
        },
        {
            "name": "鲜",
            "count": 6000,
            "percentage": 30.0
        },
        {
            "name": "甜",
            "count": 4000,
            "percentage": 20.0
        }
    ]
}
```

---

### 4. 食材使用频率统计

**接口地址：** `GET /api/analytics/ingredients/`

**功能说明：**
- 统计各食材被使用的菜谱数量
- 返回 Top 20 或指定数量食材
- 按使用次数降序排列

**请求参数：**

| 参数  | 类型 | 必填 | 说明 |
|:------|:-----|:-----|:-----|
| limit | int  | 否   | 返回数量（1-100，默认20） |

**请求示例：**
```
GET /api/analytics/ingredients/?limit=30
```

**成功响应（200）：**
```json
{
    "code": 200,
    "message": "获取食材使用频率数据成功（Top 20）",
    "data": [
        {
            "id": 1,
            "name": "鸡蛋",
            "count": 5000,
            "category": "other"
        },
        {
            "id": 2,
            "name": "葱",
            "count": 4500,
            "category": "vegetable"
        }
    ]
}
```

---

## 错误码说明

| 错误码 | 说明                     |
|:-------|:-------------------------|
| 400    | 请求参数错误             |
| 401    | 未认证或认证失败         |
| 403    | 权限不足                 |
| 404    | 资源不存在               |
| 500    | 服务器内部错误           |

---

## 更新日志

| 版本 | 日期       | 说明 |
|:-----|:-----------|:-----|
| v1.0 | 2026-01-31 | 初始版本，包含已实现的 7 个模块 28 个接口 |
