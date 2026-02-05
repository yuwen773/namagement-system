# API Documentation (Simplified)
> Base URL: `/api/`
> Format: JSON

### API 根视图 - 返回所有可用的 API 端点
`GET /api/`

---

### 用户视图集
`GET /api/users/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "phone": "string",
      "nickname": "string",
      "avatar": "http://example.com",
      "email": "user@example.com",
      "points": 0,
      "status": "active",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 用户视图集
`POST /api/users/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户登录
`POST /api/auth/login/`

---

### 用户注册
`POST /api/auth/register/`

---

### 密码重置
`POST /api/auth/password/reset/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "username": "string",
  "new_password": "string",
  "code": "string"
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "密码重置成功",
  "data": null
}
```

---

### 获取当前用户信息
`GET /api/users/me/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "phone": "string",
      "nickname": "string",
      "avatar": "http://example.com",
      "email": "user@example.com",
      "points": 0,
      "status": "active",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 更新当前用户资料
`PUT /api/users/profile/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`GET /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`PATCH /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`DELETE /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 管理员用户管理接口

#### 获取用户列表（管理员）
`GET /api/users/users/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| search | query | string | 否 | 搜索关键词（手机号、昵称） |
| status | query | string | 否 | 用户状态筛选 |
| ordering | query | string | 否 | 用于排序结果的字段 |
| page | query | integer | 否 | 分页结果集中的页码 |
| page_size | query | integer | 否 | 每页返回的结果数量 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "count": 100,
    "page": 1,
    "page_size": 20,
    "results": [
      {
        "id": 1,
        "phone": "13800138000",
        "nickname": "用户昵称",
        "avatar": "http://example.com/avatar.jpg",
        "email": "user@example.com",
        "points": 100,
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

#### 获取用户详细信息（管理员）
`GET /api/users/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | 用户ID |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "phone": "13800138000",
    "nickname": "用户昵称",
    "avatar": "http://example.com/avatar.jpg",
    "email": "user@example.com",
    "points": 100,
    "status": "active",
    "addresses": [
      {
        "id": 1,
        "receiver_name": "张三",
        "phone": "13800138000",
        "province": "北京市",
        "city": "北京市",
        "district": "朝阳区",
        "address": "某某街道123号",
        "is_default": true
      }
    ],
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

#### 禁用/启用用户账号（管理员）
`PATCH /api/users/users/{id}/status/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | 用户ID |
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "is_active": false
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "用户状态更新成功",
  "data": {
    "id": 1,
    "is_active": false
  }
}
```

---

### 获取案例列表
`GET /api/content/cases/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| status | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "title": "string",
      "summary": "string",
      "cover_image": "string",
      "author": "string",
      "status": "draft",
      "status_display": "string",
      "view_count": 0,
      "published_at": "2019-08-24T14:15:22Z",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建案例
`POST /api/content/cases/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ModificationCaseCreate](#schemamodificationcasecreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取案例详情
`GET /api/content/cases/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "status_display": "string",
  "view_count": 0,
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新案例
`PUT /api/content/cases/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ModificationCaseCreate](#schemamodificationcasecreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/content/cases/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ModificationCaseUpdate](#schemamodificationcaseupdate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "title": "string",
  "summary": "string",
  "content": "string",
  "cover_image": "string",
  "author": "string",
  "status": "draft",
  "sort_order": -2147483648,
  "published_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除案例
`DELETE /api/content/cases/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取问题列表
`GET /api/content/faqs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| category | query | string | 否 | none |
| is_active | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "question": "string",
      "answer": "string",
      "category": "order",
      "category_display": "string",
      "sort_order": -2147483648,
      "is_active": true,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建问题
`POST /api/content/faqs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [FAQ](#schemafaq) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "question": "string",
  "answer": "string",
  "category": "order",
  "category_display": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取问题详情
`GET /api/content/faqs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "question": "string",
  "answer": "string",
  "category": "order",
  "category_display": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新问题
`PUT /api/content/faqs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [FAQ](#schemafaq) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "question": "string",
  "answer": "string",
  "category": "order",
  "category_display": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/content/faqs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [FAQ](#schemafaq) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "question": "string",
  "answer": "string",
  "category": "order",
  "category_display": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除问题
`DELETE /api/content/faqs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取优惠券列表
`GET /api/marketing/coupons/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "discount_type": "full_reduction",
      "min_amount": "string",
      "discount_amount": "string",
      "discount_rate": "string",
      "valid_from": "2019-08-24T14:15:22Z",
      "valid_until": "2019-08-24T14:15:22Z",
      "total_quantity": -2147483648,
      "issued_quantity": -2147483648,
      "is_active": true
    }
  ]
}
```

---

### 创建优惠券
`POST /api/marketing/coupons/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [Coupon](#schemacoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "issued_quantity": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 查询参数：
`GET /api/marketing/coupons/my-coupons/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "discount_type": "full_reduction",
      "min_amount": "string",
      "discount_amount": "string",
      "discount_rate": "string",
      "valid_from": "2019-08-24T14:15:22Z",
      "valid_until": "2019-08-24T14:15:22Z",
      "total_quantity": -2147483648,
      "per_user_limit": -2147483648,
      "issued_quantity": 0,
      "is_active": true,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 获取优惠券详情
`GET /api/marketing/coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "issued_quantity": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新优惠券
`PUT /api/marketing/coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Coupon](#schemacoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "issued_quantity": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/marketing/coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Coupon](#schemacoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "issued_quantity": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除优惠券
`DELETE /api/marketing/coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 业务逻辑：
`POST /api/marketing/coupons/{id}/claim/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Coupon](#schemacoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "discount_type": "full_reduction",
  "min_amount": "string",
  "discount_amount": "string",
  "discount_rate": "string",
  "valid_from": "2019-08-24T14:15:22Z",
  "valid_until": "2019-08-24T14:15:22Z",
  "total_quantity": -2147483648,
  "per_user_limit": -2147483648,
  "issued_quantity": 0,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取用户优惠券列表
`GET /api/marketing/user-coupons/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "coupon": {
        "id": 0,
        "name": "string",
        "description": "string",
        "discount_type": "full_reduction",
        "min_amount": "string",
        "discount_amount": "string",
        "discount_rate": "string",
        "valid_from": "2019-08-24T14:15:22Z",
        "valid_until": "2019-08-24T14:15:22Z",
        "total_quantity": -2147483648,
        "per_user_limit": -2147483648,
        "issued_quantity": 0,
        "is_active": true,
        "created_at": "2019-08-24T14:15:22Z",
        "updated_at": "2019-08-24T14:15:22Z"
      },
      "coupon_id": 0,
      "status": "unused",
      "used_order": 0,
      "obtained_at": "2019-08-24T14:15:22Z",
      "used_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 用户优惠券管理 ViewSet
`POST /api/marketing/user-coupons/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [UserCoupon](#schemausercoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "coupon": {
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "is_active": true
  },
  "coupon_id": 0
}
```

**Response Example:**
```json
{
  "id": 0,
  "coupon": {
    "id": 0,
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "issued_quantity": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "coupon_id": 0,
  "status": "unused",
  "used_order": 0,
  "obtained_at": "2019-08-24T14:15:22Z",
  "used_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取用户优惠券详情
`GET /api/marketing/user-coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "coupon": {
    "id": 0,
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "issued_quantity": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "coupon_id": 0,
  "status": "unused",
  "used_order": 0,
  "obtained_at": "2019-08-24T14:15:22Z",
  "used_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户优惠券管理 ViewSet
`PUT /api/marketing/user-coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [UserCoupon](#schemausercoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "coupon": {
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "is_active": true
  },
  "coupon_id": 0
}
```

**Response Example:**
```json
{
  "id": 0,
  "coupon": {
    "id": 0,
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "issued_quantity": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "coupon_id": 0,
  "status": "unused",
  "used_order": 0,
  "obtained_at": "2019-08-24T14:15:22Z",
  "used_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户优惠券管理 ViewSet
`PATCH /api/marketing/user-coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [UserCoupon](#schemausercoupon) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "coupon": {
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "is_active": true
  },
  "coupon_id": 0
}
```

**Response Example:**
```json
{
  "id": 0,
  "coupon": {
    "id": 0,
    "name": "string",
    "description": "string",
    "discount_type": "full_reduction",
    "min_amount": "string",
    "discount_amount": "string",
    "discount_rate": "string",
    "valid_from": "2019-08-24T14:15:22Z",
    "valid_until": "2019-08-24T14:15:22Z",
    "total_quantity": -2147483648,
    "per_user_limit": -2147483648,
    "issued_quantity": 0,
    "is_active": true,
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "coupon_id": 0,
  "status": "unused",
  "used_order": 0,
  "obtained_at": "2019-08-24T14:15:22Z",
  "used_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户优惠券管理 ViewSet
`DELETE /api/marketing/user-coupons/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 营销管理补充接口（管理员）

#### 获取营销统计数据
`GET /api/marketing/stats/`

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total_coupons": 100,
    "active_coupons": 50,
    "total_issued": 1000,
    "total_used": 300,
    "usage_rate": 30.0
  }
}
```

---

#### 创建促销活动
`POST /api/marketing/promotions/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "title": "双11大促",
  "description": "全场满减活动",
  "type": "full_reduction",
  "discount_value": 100,
  "min_amount": 500,
  "start_time": "2024-11-01T00:00:00Z",
  "end_time": "2024-11-11T23:59:59Z",
  "is_active": true
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1,
    "title": "双11大促",
    "description": "全场满减活动",
    "type": "full_reduction",
    "discount_value": 100,
    "min_amount": 500,
    "start_time": "2024-11-01T00:00:00Z",
    "end_time": "2024-11-11T23:59:59Z",
    "is_active": true,
    "created_at": "2024-10-01T00:00:00Z"
  }
}
```

---

#### 获取促销活动列表
`GET /api/marketing/promotions/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| is_active | query | boolean | 否 | 是否启用 |
| type | query | string | 否 | 活动类型 |
| ordering | query | string | 否 | 用于排序结果的字段 |
| page | query | integer | 否 | 分页结果集中的页码 |
| page_size | query | integer | 否 | 每页返回的结果数量 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "count": 10,
    "page": 1,
    "page_size": 20,
    "results": [
      {
        "id": 1,
        "title": "双11大促",
        "description": "全场满减活动",
        "type": "full_reduction",
        "discount_value": 100,
        "min_amount": 500,
        "start_time": "2024-11-01T00:00:00Z",
        "end_time": "2024-11-11T23:59:59Z",
        "is_active": true
      }
    ]
  }
}
```

---

#### 创建 Banner 轮播图
`POST /api/marketing/banners/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "title": "首页Banner",
  "image_url": "http://example.com/banner.jpg",
  "link_url": "/products/123",
  "sort_order": 1,
  "is_active": true
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1,
    "title": "首页Banner",
    "image_url": "http://example.com/banner.jpg",
    "link_url": "/products/123",
    "sort_order": 1,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

#### 获取 Banner 列表（后台管理）
`GET /api/marketing/banners/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| is_active | query | boolean | 否 | 是否启用 |
| ordering | query | string | 否 | 用于排序结果的字段 |
| page | query | integer | 否 | 分页结果集中的页码 |
| page_size | query | integer | 否 | 每页返回的结果数量 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "count": 5,
    "page": 1,
    "page_size": 20,
    "results": [
      {
        "id": 1,
        "title": "首页Banner",
        "image_url": "http://example.com/banner.jpg",
        "link_url": "/products/123",
        "sort_order": 1,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

### 返回购物车信息及所有商品列表
`GET /api/orders/cart/`

---

### 删除购物车中的所有商品
`DELETE /api/orders/cart/clear/`

---

### 返回购物车中商品的总数量
`GET /api/orders/cart/count/`

---

### 请求参数：
`POST /api/orders/cart/items/`

---

### URL参数：
`DELETE /api/orders/cart/items/{item_id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| item_id | path | string | 是 | none |

---

### 列表查询
`GET /api/orders/orders/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "order_no": "string",
      "user": 0,
      "user_phone": "string",
      "user_nickname": "string",
      "total_amount": "string",
      "discount_amount": "string",
      "pay_amount": "string",
      "status": "pending_payment",
      "status_display": "string",
      "items_count": 0,
      "express_company": "string",
      "tracking_number": "string",
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建订单
`POST /api/orders/orders/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [OrderCreate](#schemaordercreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon_id": 0,
  "items": [
    {
      "product": 0,
      "quantity": 4294967295
    }
  ],
  "remark": "string"
}
```

**Response Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon_id": 0,
  "items": [
    {
      "product": 0,
      "quantity": 4294967295
    }
  ],
  "remark": "string"
}
```

---

### 查询参数：
`GET /api/orders/orders/my-orders/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "order_no": "string",
      "user": 0,
      "user_phone": "string",
      "user_nickname": "string",
      "recipient_name": "string",
      "recipient_phone": "string",
      "recipient_province": "string",
      "recipient_city": "string",
      "recipient_district": "string",
      "recipient_address": "string",
      "full_address": "string",
      "total_amount": "string",
      "discount_amount": "string",
      "shipping_fee": "string",
      "pay_amount": "string",
      "coupon": 0,
      "coupon_name": "string",
      "status": "pending_payment",
      "status_display": "string",
      "express_company": "string",
      "tracking_number": "string",
      "remark": "string",
      "items": [
        {
          "id": 0,
          "product": 0,
          "product_name": "string",
          "product_image": "http://example.com",
          "product_price": "string",
          "quantity": 4294967295,
          "subtotal": "string",
          "created_at": "2019-08-24T14:15:22Z"
        }
      ],
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z",
      "paid_at": "2019-08-24T14:15:22Z",
      "shipped_at": "2019-08-24T14:15:22Z",
      "completed_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 详情查询
`GET /api/orders/orders/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "order_no": "string",
  "user": 0,
  "user_phone": "string",
  "user_nickname": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "full_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon": 0,
  "coupon_name": "string",
  "status": "pending_payment",
  "status_display": "string",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "items": [
    {
      "id": 0,
      "product": 0,
      "product_name": "string",
      "product_image": "http://example.com",
      "product_price": "string",
      "quantity": 4294967295,
      "subtotal": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新订单
`PUT /api/orders/orders/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderUpdate](#schemaorderupdate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

**Response Example:**
```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

---

### 提供订单的 CRUD 操作：
`PATCH /api/orders/orders/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderUpdate](#schemaorderupdate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

**Response Example:**
```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

---

### 删除订单
`DELETE /api/orders/orders/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 只有待付款和待发货的订单可以取消
`POST /api/orders/orders/{id}/cancel/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderDetail](#schemaorderdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "shipping_fee": "string",
  "coupon": 0,
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order_no": "string",
  "user": 0,
  "user_phone": "string",
  "user_nickname": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "full_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon": 0,
  "coupon_name": "string",
  "status": "pending_payment",
  "status_display": "string",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "items": [
    {
      "id": 0,
      "product": 0,
      "product_name": "string",
      "product_image": "http://example.com",
      "product_price": "string",
      "quantity": 4294967295,
      "subtotal": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

---

### 只有已发货的订单可以确认收货
`POST /api/orders/orders/{id}/confirm/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderDetail](#schemaorderdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "shipping_fee": "string",
  "coupon": 0,
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order_no": "string",
  "user": 0,
  "user_phone": "string",
  "user_nickname": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "full_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon": 0,
  "coupon_name": "string",
  "status": "pending_payment",
  "status_display": "string",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "items": [
    {
      "id": 0,
      "product": 0,
      "product_name": "string",
      "product_image": "http://example.com",
      "product_price": "string",
      "quantity": 4294967295,
      "subtotal": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

---

### 从订单直接申请退换货，自动关联订单信息
`POST /api/orders/orders/{id}/return/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderDetail](#schemaorderdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "shipping_fee": "string",
  "coupon": 0,
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order_no": "string",
  "user": 0,
  "user_phone": "string",
  "user_nickname": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "full_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon": 0,
  "coupon_name": "string",
  "status": "pending_payment",
  "status_display": "string",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "items": [
    {
      "id": 0,
      "product": 0,
      "product_name": "string",
      "product_image": "http://example.com",
      "product_price": "string",
      "quantity": 4294967295,
      "subtotal": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

---

### 请求参数：
`POST /api/orders/orders/{id}/ship/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OrderDetail](#schemaorderdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "shipping_fee": "string",
  "coupon": 0,
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order_no": "string",
  "user": 0,
  "user_phone": "string",
  "user_nickname": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "recipient_province": "string",
  "recipient_city": "string",
  "recipient_district": "string",
  "recipient_address": "string",
  "full_address": "string",
  "total_amount": "string",
  "discount_amount": "string",
  "shipping_fee": "string",
  "pay_amount": "string",
  "coupon": 0,
  "coupon_name": "string",
  "status": "pending_payment",
  "status_display": "string",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string",
  "items": [
    {
      "id": 0,
      "product": 0,
      "product_name": "string",
      "product_image": "http://example.com",
      "product_price": "string",
      "quantity": 4294967295,
      "subtotal": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "paid_at": "2019-08-24T14:15:22Z",
  "shipped_at": "2019-08-24T14:15:22Z",
  "completed_at": "2019-08-24T14:15:22Z"
}
```

---

### 列表查询
`GET /api/orders/returns/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "order": 0,
      "order_no": "string",
      "user_phone": "string",
      "request_type": "return",
      "request_type_display": "string",
      "reason": "string",
      "status": "pending",
      "status_display": "string",
      "created_at": "2019-08-24T14:15:22Z",
      "processed_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建退换货申请
`POST /api/orders/returns/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ReturnRequestCreate](#schemareturnrequestcreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "order": 0,
  "request_type": "return",
  "reason": "string",
  "evidence_images": {}
}
```

**Response Example:**
```json
{
  "order": 0,
  "request_type": "return",
  "reason": "string",
  "evidence_images": {}
}
```

---

### 详情查询
`GET /api/orders/returns/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "order": 0,
  "order_info": {
    "id": 0,
    "order_no": "string",
    "user": 0,
    "user_phone": "string",
    "user_nickname": "string",
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "status_display": "string",
    "items_count": 0,
    "express_company": "string",
    "tracking_number": "string",
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "request_type": "return",
  "request_type_display": "string",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "status_display": "string",
  "admin_note": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "processed_at": "2019-08-24T14:15:22Z"
}
```

---

### 提供退换货申请的 CRUD 操作：
`PUT /api/orders/returns/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ReturnRequestDetail](#schemareturnrequestdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "order": 0,
  "order_info": {
    "user": 0,
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "express_company": "string",
    "tracking_number": "string"
  },
  "request_type": "return",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "admin_note": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order": 0,
  "order_info": {
    "id": 0,
    "order_no": "string",
    "user": 0,
    "user_phone": "string",
    "user_nickname": "string",
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "status_display": "string",
    "items_count": 0,
    "express_company": "string",
    "tracking_number": "string",
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "request_type": "return",
  "request_type_display": "string",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "status_display": "string",
  "admin_note": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "processed_at": "2019-08-24T14:15:22Z"
}
```

---

### 提供退换货申请的 CRUD 操作：
`PATCH /api/orders/returns/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ReturnRequestDetail](#schemareturnrequestdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "order": 0,
  "order_info": {
    "user": 0,
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "express_company": "string",
    "tracking_number": "string"
  },
  "request_type": "return",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "admin_note": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order": 0,
  "order_info": {
    "id": 0,
    "order_no": "string",
    "user": 0,
    "user_phone": "string",
    "user_nickname": "string",
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "status_display": "string",
    "items_count": 0,
    "express_company": "string",
    "tracking_number": "string",
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "request_type": "return",
  "request_type_display": "string",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "status_display": "string",
  "admin_note": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "processed_at": "2019-08-24T14:15:22Z"
}
```

---

### 提供退换货申请的 CRUD 操作：
`DELETE /api/orders/returns/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 请求参数：
`POST /api/orders/returns/{id}/process/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ReturnRequestDetail](#schemareturnrequestdetail) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "order": 0,
  "order_info": {
    "user": 0,
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "express_company": "string",
    "tracking_number": "string"
  },
  "request_type": "return",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "admin_note": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "order": 0,
  "order_info": {
    "id": 0,
    "order_no": "string",
    "user": 0,
    "user_phone": "string",
    "user_nickname": "string",
    "total_amount": "string",
    "discount_amount": "string",
    "pay_amount": "string",
    "status": "pending_payment",
    "status_display": "string",
    "items_count": 0,
    "express_company": "string",
    "tracking_number": "string",
    "created_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z"
  },
  "request_type": "return",
  "request_type_display": "string",
  "reason": "string",
  "evidence_images": {},
  "status": "pending",
  "status_display": "string",
  "admin_note": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "processed_at": "2019-08-24T14:15:22Z"
}
```

---

### 订单补充接口

#### 模拟支付订单
`POST /api/orders/orders/{id}/pay/`

**Description:** 开发测试用，支付后订单状态变更为 `pending_shipment`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | 订单ID |

**Response Example:**
```json
{
  "code": 200,
  "message": "支付成功",
  "data": {
    "id": 1,
    "order_no": "20240101123456",
    "status": "pending_shipment",
    "status_display": "待发货"
  }
}
```

---

#### 获取交易统计数据
`GET /api/orders/stats/`

**Description:** 获取交易统计数据，用于后台仪表盘展示

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "sales_trend": [
      {"date": "2024-01-01", "amount": 10000},
      {"date": "2024-01-02", "amount": 15000}
    ],
    "order_status_distribution": {
      "pending_payment": 10,
      "pending_shipment": 20,
      "shipped": 30,
      "completed": 100,
      "cancelled": 5
    },
    "top_selling_products": [
      {
        "product_id": 1,
        "product_name": "汽车刹车片",
        "sales_count": 100,
        "sales_amount": 50000
      }
    ]
  }
}
```

---

#### 获取管理员订单列表
`GET /api/orders/admin/orders/`

**Description:** 管理员订单列表（支持多维度筛选）

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| status | query | string | 否 | 订单状态筛选 |
| user_phone | query | string | 否 | 用户手机号筛选 |
| order_no | query | string | 否 | 订单号筛选 |
| start_date | query | string | 否 | 开始日期 |
| end_date | query | string | 否 | 结束日期 |
| ordering | query | string | 否 | 用于排序结果的字段 |
| page | query | integer | 否 | 分页结果集中的页码 |
| page_size | query | integer | 否 | 每页返回的结果数量 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "count": 100,
    "page": 1,
    "page_size": 20,
    "results": [
      {
        "id": 1,
        "order_no": "20240101123456",
        "user": 5,
        "user_phone": "13800138000",
        "user_nickname": "张三",
        "total_amount": "299.00",
        "discount_amount": "0.00",
        "pay_amount": "299.00",
        "status": "pending_shipment",
        "status_display": "待发货",
        "items_count": 2,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

#### 获取管理员订单详情
`GET /api/orders/admin/orders/{id}/`

**Description:** 管理员查看订单完整详情

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | 订单ID |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "order_no": "20240101123456",
    "user": 5,
    "user_phone": "13800138000",
    "user_nickname": "张三",
    "recipient_name": "李四",
    "recipient_phone": "13900139000",
    "recipient_address": "北京市朝阳区某某街道123号",
    "total_amount": "299.00",
    "discount_amount": "0.00",
    "pay_amount": "299.00",
    "status": "pending_shipment",
    "status_display": "待发货",
    "items": [
      {
        "id": 1,
        "product_name": "汽车刹车片",
        "product_spec": "前轮",
        "price": "149.50",
        "quantity": 2,
        "subtotal": "299.00"
      }
    ],
    "express_company": "",
    "tracking_number": "",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

#### 售后申请审核
`POST /api/orders/returns/{id}/audit/`

**Description:** 管理员审核售后申请

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | 售后申请ID |
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "status": "approved",
  "admin_note": "同意退货，请寄回商品"
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 1,
    "status": "approved",
    "status_display": "已同意",
    "admin_note": "同意退货，请寄回商品"
  }
}
```

---

### 商品属性管理 ViewSet
`GET /api/products/attributes/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| product | query | string | 否 | none |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "attr_name": "string",
      "attr_value": "string",
      "sort_order": -2147483648,
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 商品属性管理 ViewSet
`POST /api/products/attributes/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ProductAttribute](#schemaproductattribute) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品属性管理 ViewSet
`GET /api/products/attributes/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品属性管理 ViewSet
`PUT /api/products/attributes/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductAttribute](#schemaproductattribute) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品属性管理 ViewSet
`PATCH /api/products/attributes/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductAttribute](#schemaproductattribute) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品属性管理 ViewSet
`DELETE /api/products/attributes/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取分类列表
`GET /api/products/categories/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "parent": 0,
      "parent_name": "string",
      "sort_order": -2147483648,
      "is_active": true,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z",
      "children_count": "string"
    }
  ]
}
```

---

### 创建分类
`POST /api/products/categories/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [Category](#schemacategory) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "parent": 0,
  "parent_name": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "children_count": "string"
}
```

---

### 获取完整分类树
`GET /api/products/categories/tree/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "parent": 0,
      "parent_name": "string",
      "sort_order": -2147483648,
      "is_active": true,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z",
      "children_count": "string"
    }
  ]
}
```

---

### 获取分类详情
`GET /api/products/categories/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "parent": 0,
  "parent_name": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "children_count": "string"
}
```

---

### 更新分类
`PUT /api/products/categories/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Category](#schemacategory) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "parent": 0,
  "parent_name": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "children_count": "string"
}
```

---

### 部分更新
`PATCH /api/products/categories/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Category](#schemacategory) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "parent": 0,
  "parent_name": "string",
  "sort_order": -2147483648,
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "children_count": "string"
}
```

---

### 删除分类
`DELETE /api/products/categories/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 商品图片管理 ViewSet
`GET /api/products/images/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| product | query | string | 否 | none |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "image_url": "string",
      "sort_order": -2147483648,
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 商品图片管理 ViewSet
`POST /api/products/images/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ProductImage](#schemaproductimage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品图片管理 ViewSet
`GET /api/products/images/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品图片管理 ViewSet
`PUT /api/products/images/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductImage](#schemaproductimage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品图片管理 ViewSet
`PATCH /api/products/images/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductImage](#schemaproductimage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

**Response Example:**
```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 商品图片管理 ViewSet
`DELETE /api/products/images/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取商品列表
`GET /api/products/products/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| category | query | string | 否 | none |
| category__in | query | string | 否 | none |
| price__gte | query | string | 否 | none |
| price__lte | query | string | 否 | none |
| status | query | string | 否 | none |
| is_featured | query | string | 否 | none |
| is_new | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "price": "string",
      "original_price": "string",
      "category": 0,
      "category_name": "string",
      "main_image": "string",
      "status": "draft",
      "sales_count": 0,
      "view_count": 0,
      "is_featured": true,
      "is_new": true,
      "stock_quantity": -2147483648,
      "image_count": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建商品
`POST /api/products/products/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取推荐商品
`GET /api/products/products/featured/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| category | query | string | 否 | none |
| category__in | query | string | 否 | none |
| price__gte | query | string | 否 | none |
| price__lte | query | string | 否 | none |
| status | query | string | 否 | none |
| is_featured | query | string | 否 | none |
| is_new | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "price": "string",
      "original_price": "string",
      "category": 0,
      "category_name": "string",
      "main_image": "string",
      "status": "draft",
      "sales_count": 0,
      "view_count": 0,
      "is_featured": true,
      "is_new": true,
      "stock_quantity": -2147483648,
      "image_count": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 获取新品上市
`GET /api/products/products/new-arrivals/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| category | query | string | 否 | none |
| category__in | query | string | 否 | none |
| price__gte | query | string | 否 | none |
| price__lte | query | string | 否 | none |
| status | query | string | 否 | none |
| is_featured | query | string | 否 | none |
| is_new | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "price": "string",
      "original_price": "string",
      "category": 0,
      "category_name": "string",
      "main_image": "string",
      "status": "draft",
      "sales_count": 0,
      "view_count": 0,
      "is_featured": true,
      "is_new": true,
      "stock_quantity": -2147483648,
      "image_count": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 获取商品详情
`GET /api/products/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "stock_quantity": -2147483648,
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "images": [
    {
      "id": 0,
      "image_url": "string",
      "sort_order": -2147483648,
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "attributes": [
    {
      "id": 0,
      "attr_name": "string",
      "attr_value": "string",
      "sort_order": -2147483648,
      "created_at": "2019-08-24T14:15:22Z"
    }
  ],
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新商品
`PUT /api/products/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/products/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除商品
`DELETE /api/products/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 下架商品
`POST /api/products/products/{id}/archive/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 发布商品
`POST /api/products/products/{id}/publish/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取或提交商品评价
`GET /api/products/products/{id}/reviews/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取或提交商品评价
`POST /api/products/products/{id}/reviews/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [ProductList](#schemaproductlist) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "main_image": "string",
  "status": "draft",
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "price": "string",
  "original_price": "string",
  "category": 0,
  "category_name": "string",
  "main_image": "string",
  "status": "draft",
  "sales_count": 0,
  "view_count": 0,
  "is_featured": true,
  "is_new": true,
  "stock_quantity": -2147483648,
  "image_count": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取评价列表
`GET /api/products/reviews/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| product | query | string | 否 | none |
| rating | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "rating": 1,
      "comment": "string",
      "images": {},
      "user_id_display": "string",
      "is_anonymous": true,
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 请求参数：
`POST /api/products/reviews/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [ReviewCreate](#schemareviewcreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

**Response Example:**
```json
{
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

---

### 获取评价详情
`GET /api/products/reviews/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "product": 0,
  "product_name": "string",
  "user_id": -2147483648,
  "user_id_display": "string",
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 提供以下接口：
`PUT /api/products/reviews/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Review](#schemareview) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "product": 0,
  "user_id": -2147483648,
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "product": 0,
  "product_name": "string",
  "user_id": -2147483648,
  "user_id_display": "string",
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 提供以下接口：
`PATCH /api/products/reviews/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Review](#schemareview) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "product": 0,
  "user_id": -2147483648,
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "product": 0,
  "product_name": "string",
  "user_id": -2147483648,
  "user_id_display": "string",
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除评价（管理员）
`DELETE /api/products/reviews/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取我的评价列表
`GET /api/products/reviews/me/`

**Description:** 获取当前登录用户发表的所有评价记录

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| rating | query | integer | 否 | 评分筛选（1-5） |
| ordering | query | string | 否 | 用于排序结果的字段 |
| page | query | integer | 否 | 分页结果集中的页码 |
| page_size | query | integer | 否 | 每页返回的结果数量 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "count": 10,
    "page": 1,
    "page_size": 20,
    "results": [
      {
        "id": 1,
        "product": 123,
        "product_name": "汽车刹车片",
        "user_id": 5,
        "user_id_display": 5,
        "order_item_id": 456,
        "rating": 5,
        "comment": "产品质量很好，安装方便",
        "images": ["http://example.com/image1.jpg"],
        "is_anonymous": false,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

### 获取推荐商品列表
`GET /api/recommendations/products/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| rule | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "rule": 0,
      "rule_name": "string",
      "product": {
        "id": 0,
        "name": "string",
        "price": "string",
        "original_price": "string",
        "category": 0,
        "category_name": "string",
        "main_image": "string",
        "status": "draft",
        "sales_count": 0,
        "view_count": 0,
        "is_featured": true,
        "is_new": true,
        "stock_quantity": -2147483648,
        "image_count": "string",
        "created_at": "2019-08-24T14:15:22Z"
      },
      "sort_order": -2147483648,
      "remark": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 添加推荐商品
`POST /api/recommendations/products/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [RecommendedProductCreate](#schemarecommendedproductcreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

**Response Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

---

### 获取推荐商品详情
`GET /api/recommendations/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "rule": 0,
  "rule_name": "string",
  "product": {
    "id": 0,
    "name": "string",
    "price": "string",
    "original_price": "string",
    "category": 0,
    "category_name": "string",
    "main_image": "string",
    "status": "draft",
    "sales_count": 0,
    "view_count": 0,
    "is_featured": true,
    "is_new": true,
    "stock_quantity": -2147483648,
    "image_count": "string",
    "created_at": "2019-08-24T14:15:22Z"
  },
  "sort_order": -2147483648,
  "remark": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新推荐商品
`PUT /api/recommendations/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [RecommendedProductCreate](#schemarecommendedproductcreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

**Response Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

---

### 部分更新（管理员）
`PATCH /api/recommendations/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [RecommendedProductCreate](#schemarecommendedproductcreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

**Response Example:**
```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

---

### 删除推荐商品
`DELETE /api/recommendations/products/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取推荐规则列表
`GET /api/recommendations/rules/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| rule_type | query | string | 否 | none |
| is_active | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "rule_type": "hot",
      "rule_type_display": "string",
      "description": "string",
      "config": {},
      "priority": -2147483648,
      "limit": -2147483648,
      "is_active": true,
      "product_count": "string",
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 创建推荐规则
`POST /api/recommendations/rules/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [RecommendationRule](#schemarecommendationrule) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "rule_type": "hot",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "rule_type": "hot",
  "rule_type_display": "string",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true,
  "product_count": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取启用的推荐规则
`GET /api/recommendations/rules/active/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| rule_type | query | string | 否 | none |
| is_active | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "rule_type": "hot",
      "rule_type_display": "string",
      "description": "string",
      "config": {},
      "priority": -2147483648,
      "limit": -2147483648,
      "is_active": true,
      "product_count": "string",
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 获取规则详情
`GET /api/recommendations/rules/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "rule_type": "hot",
  "rule_type_display": "string",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true,
  "recommended_products": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新推荐规则
`PUT /api/recommendations/rules/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [RecommendationRule](#schemarecommendationrule) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "rule_type": "hot",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "rule_type": "hot",
  "rule_type_display": "string",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true,
  "product_count": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/recommendations/rules/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [RecommendationRule](#schemarecommendationrule) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "name": "string",
  "rule_type": "hot",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "name": "string",
  "rule_type": "hot",
  "rule_type_display": "string",
  "description": "string",
  "config": {},
  "priority": -2147483648,
  "limit": -2147483648,
  "is_active": true,
  "product_count": "string",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除推荐规则
`DELETE /api/recommendations/rules/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取配置列表
`GET /api/system/configs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| category | query | string | 否 | none |
| is_editable | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "key": "string",
      "value": "string",
      "description": "string",
      "category": "basic",
      "is_editable": true
    }
  ]
}
```

---

### 创建配置
`POST /api/system/configs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [SystemConfig](#schemasystemconfig) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取配置详情
`GET /api/system/configs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新配置
`PUT /api/system/configs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [SystemConfig](#schemasystemconfig) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 部分更新（管理员）
`PATCH /api/system/configs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [SystemConfig](#schemasystemconfig) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除配置
`DELETE /api/system/configs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取日志列表
`GET /api/system/logs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| action_type | query | string | 否 | none |
| object_type | query | string | 否 | none |
| status | query | string | 否 | none |
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "operator": 0,
      "operator_name": "string",
      "action_type": "create",
      "action_type_display": "string",
      "object_type": "string",
      "detail": "string",
      "status": "success",
      "status_display": "string",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 操作日志 ViewSet（仅管理员可访问）
`POST /api/system/logs/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [OperationLog](#schemaoperationlog) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "operator": 0,
  "action_type": "create",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "error_message": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "operator": 0,
  "operator_name": "string",
  "action_type": "create",
  "action_type_display": "string",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "status_display": "string",
  "error_message": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 获取日志详情
`GET /api/system/logs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "operator": 0,
  "operator_name": "string",
  "action_type": "create",
  "action_type_display": "string",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "status_display": "string",
  "error_message": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 操作日志 ViewSet（仅管理员可访问）
`PUT /api/system/logs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OperationLog](#schemaoperationlog) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "operator": 0,
  "action_type": "create",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "error_message": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "operator": 0,
  "operator_name": "string",
  "action_type": "create",
  "action_type_display": "string",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "status_display": "string",
  "error_message": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 操作日志 ViewSet（仅管理员可访问）
`PATCH /api/system/logs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [OperationLog](#schemaoperationlog) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "operator": 0,
  "action_type": "create",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "error_message": "string"
}
```

**Response Example:**
```json
{
  "id": 0,
  "operator": 0,
  "operator_name": "string",
  "action_type": "create",
  "action_type_display": "string",
  "object_type": "string",
  "object_id": "string",
  "detail": "string",
  "ip_address": "string",
  "status": "success",
  "status_display": "string",
  "error_message": "string",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 操作日志 ViewSet（仅管理员可访问）
`DELETE /api/system/logs/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 获取消息列表
`GET /api/system/messages/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "title": "string",
      "message_type": "announcement",
      "message_type_display": "string",
      "status": "draft",
      "status_display": "string",
      "sent_at": "2019-08-24T14:15:22Z",
      "read_at": "2019-08-24T14:15:22Z",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 发送消息
`POST /api/system/messages/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [MessageCreate](#schemamessagecreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement"
}
```

**Response Example:**
```json
{
  "id": 0,
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement"
}
```

---

### 查询参数：
`GET /api/system/messages/my-messages/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| search | query | string | 否 | 搜索关键词。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "recipient": 0,
      "recipient_name": "string",
      "title": "string",
      "content": "string",
      "message_type": "announcement",
      "message_type_display": "string",
      "status": "draft",
      "status_display": "string",
      "sent_at": "2019-08-24T14:15:22Z",
      "read_at": "2019-08-24T14:15:22Z",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 获取消息详情
`GET /api/system/messages/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "recipient": 0,
  "recipient_name": "string",
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "message_type_display": "string",
  "status": "draft",
  "status_display": "string",
  "sent_at": "2019-08-24T14:15:22Z",
  "read_at": "2019-08-24T14:15:22Z",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 更新消息
`PUT /api/system/messages/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Message](#schemamessage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

**Response Example:**
```json
{
  "id": 0,
  "recipient": 0,
  "recipient_name": "string",
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "message_type_display": "string",
  "status": "draft",
  "status_display": "string",
  "sent_at": "2019-08-24T14:15:22Z",
  "read_at": "2019-08-24T14:15:22Z",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 站内消息 ViewSet
`PATCH /api/system/messages/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Message](#schemamessage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

**Response Example:**
```json
{
  "id": 0,
  "recipient": 0,
  "recipient_name": "string",
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "message_type_display": "string",
  "status": "draft",
  "status_display": "string",
  "sent_at": "2019-08-24T14:15:22Z",
  "read_at": "2019-08-24T14:15:22Z",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 删除消息
`DELETE /api/system/messages/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 标记消息已读
`POST /api/system/messages/{id}/mark-read/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [Message](#schemamessage) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

**Response Example:**
```json
{
  "id": 0,
  "recipient": 0,
  "recipient_name": "string",
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "message_type_display": "string",
  "status": "draft",
  "status_display": "string",
  "sent_at": "2019-08-24T14:15:22Z",
  "read_at": "2019-08-24T14:15:22Z",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`GET /api/users/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "phone": "string",
      "nickname": "string",
      "avatar": "http://example.com",
      "email": "user@example.com",
      "points": 0,
      "status": "active",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 用户视图集
`POST /api/users/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户地址视图集
`GET /api/users/addresses/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "user": {
        "id": 0,
        "phone": "string",
        "nickname": "string",
        "avatar": "http://example.com",
        "email": "user@example.com",
        "points": 0,
        "status": "active",
        "created_at": "2019-08-24T14:15:22Z"
      },
      "recipient_name": "string",
      "phone": "string",
      "province": "string",
      "city": "string",
      "district": "string",
      "address": "string",
      "is_default": true,
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 用户地址视图集
`POST /api/users/addresses/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [UserAddressCreate](#schemauseraddresscreate) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true
}
```

**Response Example:**
```json
{
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true
}
```

---

### 用户地址视图集
`GET /api/users/addresses/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "user": {
    "id": 0,
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com",
    "points": 0,
    "status": "active",
    "created_at": "2019-08-24T14:15:22Z"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户地址视图集
`PUT /api/users/addresses/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [UserAddress](#schemauseraddress) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "user": {
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "user": {
    "id": 0,
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com",
    "points": 0,
    "status": "active",
    "created_at": "2019-08-24T14:15:22Z"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户地址视图集
`PATCH /api/users/addresses/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [UserAddress](#schemauseraddress) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "user": {
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "user": {
    "id": 0,
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com",
    "points": 0,
    "status": "active",
    "created_at": "2019-08-24T14:15:22Z"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户地址视图集
`DELETE /api/users/addresses/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

### 设为默认地址
`POST /api/users/addresses/{id}/set-default/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [UserAddress](#schemauseraddress) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "user": {
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true
}
```

**Response Example:**
```json
{
  "id": 0,
  "user": {
    "id": 0,
    "phone": "string",
    "nickname": "string",
    "avatar": "http://example.com",
    "email": "user@example.com",
    "points": 0,
    "status": "active",
    "created_at": "2019-08-24T14:15:22Z"
  },
  "recipient_name": "string",
  "phone": "string",
  "province": "string",
  "city": "string",
  "district": "string",
  "address": "string",
  "is_default": true,
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户登录
`POST /api/users/auth/login/`

---

### 用户注册
`POST /api/users/auth/register/`

---

### 获取当前用户信息
`GET /api/users/me/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| ordering | query | string | 否 | 用于排序结果的字段。 |
| page | query | integer | 否 | 分页结果集中的页码。 |
| page_size | query | integer | 否 | 每页返回的结果数量。 |

**Response Example:**
```json
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "phone": "string",
      "nickname": "string",
      "avatar": "http://example.com",
      "email": "user@example.com",
      "points": 0,
      "status": "active",
      "created_at": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---

### 更新当前用户资料
`PUT /api/users/profile/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 修改当前用户密码
`POST /api/users/change-password/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**Response Example:**
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

---

### 获取当前用户的浏览历史列表
`GET /api/users/browsing-history/list_history/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| limit | query | integer | 否 | 返回的记录数，默认为20 |
| offset | query | integer | 否 | 跳过的记录数，用于分页 |

**Response Example:**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "product_id": 123,
      "product_name": "高性能刹车片",
      "product_image": "https://example.com/image.jpg",
      "product_price": "299.99",
      "viewed_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### 添加商品浏览记录（自动去重，如果已存在则更新浏览时间）
`POST /api/users/browsing-history/add/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| body | body | object | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "product_id": 1,
  "product_name": "string",
  "product_image": "http://example.com",
  "product_price": "99.99"
}
```

**Response Example:**
```json
{
  "code": 201,
  "message": "添加成功",
  "data": {
    "id": 1,
    "product_id": 123,
    "product_name": "高性能刹车片",
    "product_image": "https://example.com/image.jpg",
    "product_price": "299.99",
    "viewed_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### 清空当前用户的所有浏览记录
`DELETE /api/users/browsing-history/clear/`

**Response Example:**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": {
    "deleted_count": 15
  }
}
```

---

### 用户视图集
`GET /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`PUT /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`PATCH /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |
| body | body | [User](#schemauser) | 是 | See Request Body Example |

**Request Body Example:**
```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

**Response Example:**
```json
{
  "id": 0,
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com",
  "points": 0,
  "status": "active",
  "created_at": "2019-08-24T14:15:22Z"
}
```

---

### 用户视图集
`DELETE /api/users/{id}/`

**Request Parameters:**
| Name | In | Type | Required | Description |
|---|---|---|---|---|
| id | path | string | 是 | none |

---

