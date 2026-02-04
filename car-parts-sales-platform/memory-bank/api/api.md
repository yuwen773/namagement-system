---
title: 默认模块
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# 默认模块

汽车改装件销售推荐平台 RESTful API 文档

## 功能模块
- **用户管理**: 用户注册、登录、个人信息、收货地址
- **商品管理**: 商品分类、商品列表、商品详情、商品评价
- **订单管理**: 购物车、订单创建、订单列表、订单详情、退换货
- **营销管理**: 优惠券领取、我的优惠券
- **推荐管理**: 热门推荐、新品推荐、个性化推荐
- **内容管理**: 改装案例、常见问题
- **系统管理**: 系统配置、站内消息、操作日志

## 认证方式
本 API 使用 JWT (JSON Web Token) 进行身份认证。

### 获取 Token
1. **注册**: `POST /api/auth/register/`
2. **登录**: `POST /api/auth/login/`

### 使用 Token
在请求头中添加:
```
Authorization: Bearer <your_access_token>
```

## 统一响应格式
所有 API 返回格式:
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {...}
}
```

分页响应格式:
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "page": 1,
        "page_size": 20,
        "results": [...]
    }
}
```

Base URLs:

# Authentication

- HTTP Authentication, scheme: basic

# api

<a id="opIdapi_list"></a>

## GET api_list

GET /api/

API 根视图 - 返回所有可用的 API 端点

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|None|

<a id="opIdapi_auth_list"></a>

## GET api_auth_list

GET /api/auth/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[User](#schemauser)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» phone|string|true|none|手机号|none|
|»» nickname|string|false|none|昵称|none|
|»» avatar|string(uri)¦null|false|none|头像URL|none|
|»» email|string(email)|false|none|电子邮件地址|none|
|»» points|integer|false|read-only|积分|none|
|»» status|string|false|read-only|状态|none|
|»» created_at|string(date-time)|false|read-only|注册时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_auth_create"></a>

## POST api_auth_create

POST /api/auth/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[User](#schemauser)|

<a id="opIdapi_auth_addresses_list"></a>

## GET api_auth_addresses_list

GET /api/auth/addresses/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[UserAddress](#schemauseraddress)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» user|[User](#schemauser)|false|none||none|
|»»» id|integer|false|read-only|ID|none|
|»»» phone|string|true|none|手机号|none|
|»»» nickname|string|false|none|昵称|none|
|»»» avatar|string(uri)¦null|false|none|头像URL|none|
|»»» email|string(email)|false|none|电子邮件地址|none|
|»»» points|integer|false|read-only|积分|none|
|»»» status|string|false|read-only|状态|none|
|»»» created_at|string(date-time)|false|read-only|注册时间|none|
|»» recipient_name|string|true|none|收货人姓名|none|
|»» phone|string|true|none|收货人手机号|none|
|»» province|string|false|none|省份|none|
|»» city|string|false|none|城市|none|
|»» district|string|false|none|区县|none|
|»» address|string|true|none|详细地址|none|
|»» is_default|boolean|false|none|是否默认地址|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_auth_addresses_create"></a>

## POST api_auth_addresses_create

POST /api/auth/addresses/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[UserAddressCreate](#schemauseraddresscreate)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserAddressCreate](#schemauseraddresscreate)|

<a id="opIdapi_auth_addresses_read"></a>

## GET api_auth_addresses_read

GET /api/auth/addresses/{id}/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_auth_addresses_update"></a>

## PUT api_auth_addresses_update

PUT /api/auth/addresses/{id}/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_auth_addresses_partial_update"></a>

## PATCH api_auth_addresses_partial_update

PATCH /api/auth/addresses/{id}/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_auth_addresses_delete"></a>

## DELETE api_auth_addresses_delete

DELETE /api/auth/addresses/{id}/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_auth_addresses_set_default"></a>

## POST api_auth_addresses_set_default

POST /api/auth/addresses/{id}/set-default/

设为默认地址

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_auth_auth_login"></a>

## POST api_auth_auth_login

POST /api/auth/auth/login/

用户登录

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|None|

<a id="opIdapi_auth_auth_register"></a>

## POST api_auth_auth_register

POST /api/auth/auth/register/

用户注册

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|None|

<a id="opIdapi_auth_me"></a>

## GET api_auth_me

GET /api/auth/me/

获取当前用户信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[User](#schemauser)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» phone|string|true|none|手机号|none|
|»» nickname|string|false|none|昵称|none|
|»» avatar|string(uri)¦null|false|none|头像URL|none|
|»» email|string(email)|false|none|电子邮件地址|none|
|»» points|integer|false|read-only|积分|none|
|»» status|string|false|read-only|状态|none|
|»» created_at|string(date-time)|false|read-only|注册时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_auth_profile"></a>

## PUT api_auth_profile

PUT /api/auth/profile/

更新当前用户资料

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_auth_read"></a>

## GET api_auth_read

GET /api/auth/{id}/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_auth_update"></a>

## PUT api_auth_update

PUT /api/auth/{id}/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_auth_partial_update"></a>

## PATCH api_auth_partial_update

PATCH /api/auth/{id}/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_auth_delete"></a>

## DELETE api_auth_delete

DELETE /api/auth/{id}/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_content_cases_list"></a>

## GET api_content_cases_list

GET /api/content/cases/

获取案例列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|status|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ModificationCaseList](#schemamodificationcaselist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» title|string|true|none|标题|none|
|»» summary|string|false|none|摘要|none|
|»» cover_image|string|false|none|封面图片URL|none|
|»» author|string|false|none|作者|none|
|»» status|string|false|none|状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» view_count|integer|false|read-only|浏览量|none|
|»» published_at|string(date-time)¦null|false|none|发布时间|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|published|

<a id="opIdapi_content_cases_create"></a>

## POST api_content_cases_create

POST /api/content/cases/

创建案例

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ModificationCaseCreate](#schemamodificationcasecreate)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ModificationCaseCreate](#schemamodificationcasecreate)|

<a id="opIdapi_content_cases_read"></a>

## GET api_content_cases_read

GET /api/content/cases/{id}/

获取案例详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ModificationCaseDetail](#schemamodificationcasedetail)|

<a id="opIdapi_content_cases_update"></a>

## PUT api_content_cases_update

PUT /api/content/cases/{id}/

更新案例

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ModificationCaseCreate](#schemamodificationcasecreate)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ModificationCaseCreate](#schemamodificationcasecreate)|

<a id="opIdapi_content_cases_partial_update"></a>

## PATCH api_content_cases_partial_update

PATCH /api/content/cases/{id}/

部分更新（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ModificationCaseUpdate](#schemamodificationcaseupdate)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ModificationCaseUpdate](#schemamodificationcaseupdate)|

<a id="opIdapi_content_cases_delete"></a>

## DELETE api_content_cases_delete

DELETE /api/content/cases/{id}/

删除案例

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_content_faqs_list"></a>

## GET api_content_faqs_list

GET /api/content/faqs/

获取问题列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|category|query|string| 否 |none|
|is_active|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[FAQ](#schemafaq)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» question|string|true|none|问题|none|
|»» answer|string|true|none|答案|none|
|»» category|string|false|none|分类|none|
|»» category_display|string|false|read-only|Category display|none|
|»» sort_order|integer|false|none|排序|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|category|order|
|category|payment|
|category|shipping|
|category|product|
|category|return|
|category|account|
|category|other|

<a id="opIdapi_content_faqs_create"></a>

## POST api_content_faqs_create

POST /api/content/faqs/

创建问题

> Body 请求参数

```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[FAQ](#schemafaq)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[FAQ](#schemafaq)|

<a id="opIdapi_content_faqs_read"></a>

## GET api_content_faqs_read

GET /api/content/faqs/{id}/

获取问题详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[FAQ](#schemafaq)|

<a id="opIdapi_content_faqs_update"></a>

## PUT api_content_faqs_update

PUT /api/content/faqs/{id}/

更新问题

> Body 请求参数

```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[FAQ](#schemafaq)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[FAQ](#schemafaq)|

<a id="opIdapi_content_faqs_partial_update"></a>

## PATCH api_content_faqs_partial_update

PATCH /api/content/faqs/{id}/

部分更新（管理员）

> Body 请求参数

```json
{
  "question": "string",
  "answer": "string",
  "category": "order",
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[FAQ](#schemafaq)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[FAQ](#schemafaq)|

<a id="opIdapi_content_faqs_delete"></a>

## DELETE api_content_faqs_delete

DELETE /api/content/faqs/{id}/

删除问题

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_marketing_coupons_list"></a>

## GET api_marketing_coupons_list

GET /api/marketing/coupons/

获取优惠券列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[CouponList](#schemacouponlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|优惠券名称|none|
|»» description|string|false|none|优惠券描述|none|
|»» discount_type|string|false|none|优惠类型|none|
|»» min_amount|string(decimal)|false|none|使用门槛|none|
|»» discount_amount|string(decimal)|false|none|优惠金额|none|
|»» discount_rate|string(decimal)¦null|false|none|折扣率|none|
|»» valid_from|string(date-time)|true|none|有效期开始|none|
|»» valid_until|string(date-time)|true|none|有效期结束|none|
|»» total_quantity|integer|false|none|发放总量|none|
|»» issued_quantity|integer|false|none|已发放数量|none|
|»» is_active|boolean|false|none|是否启用|none|

#### 枚举值

|属性|值|
|---|---|
|discount_type|full_reduction|
|discount_type|discount|

<a id="opIdapi_marketing_coupons_create"></a>

## POST api_marketing_coupons_create

POST /api/marketing/coupons/

创建优惠券

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Coupon](#schemacoupon)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Coupon](#schemacoupon)|

<a id="opIdapi_marketing_coupons_my_coupons"></a>

## GET 获取当前用户的优惠券

GET /api/marketing/coupons/my-coupons/

查询参数：
- status: 状态筛选（unused/used/expired）

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[Coupon](#schemacoupon)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|优惠券名称|none|
|»» description|string|false|none|优惠券描述|none|
|»» discount_type|string|false|none|优惠类型|none|
|»» min_amount|string(decimal)|false|none|使用门槛|none|
|»» discount_amount|string(decimal)|false|none|优惠金额|none|
|»» discount_rate|string(decimal)¦null|false|none|折扣率|none|
|»» valid_from|string(date-time)|true|none|有效期开始|none|
|»» valid_until|string(date-time)|true|none|有效期结束|none|
|»» total_quantity|integer|false|none|发放总量|none|
|»» per_user_limit|integer|false|none|每人限领数量|none|
|»» issued_quantity|integer|false|read-only|已发放数量|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|discount_type|full_reduction|
|discount_type|discount|

<a id="opIdapi_marketing_coupons_read"></a>

## GET api_marketing_coupons_read

GET /api/marketing/coupons/{id}/

获取优惠券详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Coupon](#schemacoupon)|

<a id="opIdapi_marketing_coupons_update"></a>

## PUT api_marketing_coupons_update

PUT /api/marketing/coupons/{id}/

更新优惠券

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Coupon](#schemacoupon)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Coupon](#schemacoupon)|

<a id="opIdapi_marketing_coupons_partial_update"></a>

## PATCH api_marketing_coupons_partial_update

PATCH /api/marketing/coupons/{id}/

部分更新（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Coupon](#schemacoupon)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Coupon](#schemacoupon)|

<a id="opIdapi_marketing_coupons_delete"></a>

## DELETE api_marketing_coupons_delete

DELETE /api/marketing/coupons/{id}/

删除优惠券

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_marketing_coupons_claim"></a>

## POST 领取优惠券

POST /api/marketing/coupons/{id}/claim/

业务逻辑：
1. 检查优惠券是否存在且有效
2. 检查是否在有效期内
3. 检查是否还有剩余数量
4. 检查用户是否超过限领数量
5. 记录领取信息并增加已发放数量

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Coupon](#schemacoupon)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Coupon](#schemacoupon)|

<a id="opIdapi_marketing_user-coupons_list"></a>

## GET api_marketing_user-coupons_list

GET /api/marketing/user-coupons/

获取用户优惠券列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[UserCoupon](#schemausercoupon)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» coupon|[Coupon](#schemacoupon)|false|none||none|
|»»» id|integer|false|read-only|ID|none|
|»»» name|string|true|none|优惠券名称|none|
|»»» description|string|false|none|优惠券描述|none|
|»»» discount_type|string|false|none|优惠类型|none|
|»»» min_amount|string(decimal)|false|none|使用门槛|none|
|»»» discount_amount|string(decimal)|false|none|优惠金额|none|
|»»» discount_rate|string(decimal)¦null|false|none|折扣率|none|
|»»» valid_from|string(date-time)|true|none|有效期开始|none|
|»»» valid_until|string(date-time)|true|none|有效期结束|none|
|»»» total_quantity|integer|false|none|发放总量|none|
|»»» per_user_limit|integer|false|none|每人限领数量|none|
|»»» issued_quantity|integer|false|read-only|已发放数量|none|
|»»» is_active|boolean|false|none|是否启用|none|
|»»» created_at|string(date-time)|false|read-only|创建时间|none|
|»»» updated_at|string(date-time)|false|read-only|更新时间|none|
|»» coupon_id|integer|true|none|Coupon id|none|
|»» status|string|false|read-only|使用状态|none|
|»» used_order|integer¦null|false|read-only|使用的订单|none|
|»» obtained_at|string(date-time)|false|read-only|领取时间|none|
|»» used_at|string(date-time)¦null|false|read-only|使用时间|none|

#### 枚举值

|属性|值|
|---|---|
|discount_type|full_reduction|
|discount_type|discount|
|status|unused|
|status|used|
|status|expired|

<a id="opIdapi_marketing_user-coupons_create"></a>

## POST api_marketing_user-coupons_create

POST /api/marketing/user-coupons/

用户优惠券管理 ViewSet

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[UserCoupon](#schemausercoupon)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserCoupon](#schemausercoupon)|

<a id="opIdapi_marketing_user-coupons_read"></a>

## GET api_marketing_user-coupons_read

GET /api/marketing/user-coupons/{id}/

获取用户优惠券详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserCoupon](#schemausercoupon)|

<a id="opIdapi_marketing_user-coupons_update"></a>

## PUT api_marketing_user-coupons_update

PUT /api/marketing/user-coupons/{id}/

用户优惠券管理 ViewSet

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserCoupon](#schemausercoupon)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserCoupon](#schemausercoupon)|

<a id="opIdapi_marketing_user-coupons_partial_update"></a>

## PATCH api_marketing_user-coupons_partial_update

PATCH /api/marketing/user-coupons/{id}/

用户优惠券管理 ViewSet

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserCoupon](#schemausercoupon)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserCoupon](#schemausercoupon)|

<a id="opIdapi_marketing_user-coupons_delete"></a>

## DELETE api_marketing_user-coupons_delete

DELETE /api/marketing/user-coupons/{id}/

用户优惠券管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_orders_cart_list"></a>

## GET 获取购物车

GET /api/orders/cart/

返回购物车信息及所有商品列表

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|None|

<a id="opIdapi_orders_cart_clear_cart"></a>

## DELETE 清空购物车

DELETE /api/orders/cart/clear/

删除购物车中的所有商品

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_orders_cart_cart_count"></a>

## GET 获取购物车商品数量

GET /api/orders/cart/count/

返回购物车中商品的总数量

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|None|

<a id="opIdapi_orders_cart_add_item"></a>

## POST 添加商品到购物车

POST /api/orders/cart/items/

请求参数：
- product: 商品ID
- quantity: 数量（可选，默认为1）

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|None|

<a id="opIdapi_orders_cart_remove_item"></a>

## DELETE 删除购物车商品

DELETE /api/orders/cart/items/{item_id}/

URL参数：
- item_id: 购物车商品ID

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|item_id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_orders_orders_list"></a>

## GET api_orders_orders_list

GET /api/orders/orders/

列表查询

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[OrderList](#schemaorderlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» order_no|string|false|read-only|订单号|none|
|»» user|integer|true|none|所属用户|none|
|»» user_phone|string|false|read-only|User phone|none|
|»» user_nickname|string|false|read-only|User nickname|none|
|»» total_amount|string(decimal)|false|none|订单总额|none|
|»» discount_amount|string(decimal)|false|none|优惠金额|none|
|»» pay_amount|string(decimal)|false|none|实付金额|none|
|»» status|string|false|none|订单状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» items_count|integer|false|read-only|Items count|none|
|»» express_company|string|false|none|物流公司|none|
|»» tracking_number|string|false|none|物流单号|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|pending_shipment|
|status|shipped|
|status|completed|
|status|cancelled|

<a id="opIdapi_orders_orders_create"></a>

## POST api_orders_orders_create

POST /api/orders/orders/

创建订单

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[OrderCreate](#schemaordercreate)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OrderCreate](#schemaordercreate)|

<a id="opIdapi_orders_orders_my_orders"></a>

## GET 我的订单

GET /api/orders/orders/my-orders/

查询参数：
- status: 订单状态筛选（可选）

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[OrderDetail](#schemaorderdetail)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» order_no|string|false|read-only|订单号|none|
|»» user|integer|false|read-only|所属用户|none|
|»» user_phone|string|false|read-only|User phone|none|
|»» user_nickname|string|false|read-only|User nickname|none|
|»» recipient_name|string|true|none|收货人姓名|none|
|»» recipient_phone|string|true|none|收货人手机号|none|
|»» recipient_province|string|false|none|省份|none|
|»» recipient_city|string|false|none|城市|none|
|»» recipient_district|string|false|none|区县|none|
|»» recipient_address|string|true|none|详细地址|none|
|»» full_address|string|false|read-only|Full address|none|
|»» total_amount|string(decimal)|false|read-only|订单总额|none|
|»» discount_amount|string(decimal)|false|read-only|优惠金额|none|
|»» shipping_fee|string(decimal)|false|none|运费|none|
|»» pay_amount|string(decimal)|false|read-only|实付金额|none|
|»» coupon|integer¦null|false|none|使用的优惠券|none|
|»» coupon_name|string¦null|false|read-only|Coupon name|none|
|»» status|string|false|none|订单状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» express_company|string|false|none|物流公司|none|
|»» tracking_number|string|false|none|物流单号|none|
|»» remark|string|false|none|订单备注|none|
|»» items|[[OrderItem](#schemaorderitem)]|false|read-only||none|
|»»» id|integer|false|read-only|ID|none|
|»»» product|integer¦null|false|none|商品|none|
|»»» product_name|string|true|none|商品名称|none|
|»»» product_image|string(uri)|false|none|商品图片|none|
|»»» product_price|string(decimal)|true|none|购买单价|none|
|»»» quantity|integer|false|none|购买数量|none|
|»»» subtotal|string(decimal)|false|read-only|小计金额|none|
|»»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|
|»» paid_at|string(date-time)¦null|false|none|付款时间|none|
|»» shipped_at|string(date-time)¦null|false|none|发货时间|none|
|»» completed_at|string(date-time)¦null|false|none|完成时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|pending_shipment|
|status|shipped|
|status|completed|
|status|cancelled|

<a id="opIdapi_orders_orders_read"></a>

## GET api_orders_orders_read

GET /api/orders/orders/{id}/

详情查询

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OrderDetail](#schemaorderdetail)|

<a id="opIdapi_orders_orders_update"></a>

## PUT api_orders_orders_update

PUT /api/orders/orders/{id}/

更新订单

> Body 请求参数

```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderUpdate](#schemaorderupdate)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OrderUpdate](#schemaorderupdate)|

<a id="opIdapi_orders_orders_partial_update"></a>

## PATCH 订单视图集

PATCH /api/orders/orders/{id}/

提供订单的 CRUD 操作：
- list: 获取订单列表
- retrieve: 获取订单详情
- create: 创建订单
- update: 更新订单
- destroy: 删除订单

> Body 请求参数

```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderUpdate](#schemaorderupdate)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OrderUpdate](#schemaorderupdate)|

<a id="opIdapi_orders_orders_delete"></a>

## DELETE api_orders_orders_delete

DELETE /api/orders/orders/{id}/

删除订单

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_orders_orders_cancel"></a>

## POST 取消订单

POST /api/orders/orders/{id}/cancel/

只有待付款和待发货的订单可以取消

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderDetail](#schemaorderdetail)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OrderDetail](#schemaorderdetail)|

<a id="opIdapi_orders_orders_confirm"></a>

## POST 确认收货

POST /api/orders/orders/{id}/confirm/

只有已发货的订单可以确认收货

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderDetail](#schemaorderdetail)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OrderDetail](#schemaorderdetail)|

<a id="opIdapi_orders_orders_return_order"></a>

## POST 申请退换货

POST /api/orders/orders/{id}/return/

从订单直接申请退换货，自动关联订单信息

请求参数：
- request_type: 申请类型 (return/refund)
- reason: 原因描述
- evidence_images: 凭证图片列表（可选）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderDetail](#schemaorderdetail)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OrderDetail](#schemaorderdetail)|

<a id="opIdapi_orders_orders_ship"></a>

## POST 订单发货（管理员操作）

POST /api/orders/orders/{id}/ship/

请求参数：
- express_company: 物流公司
- tracking_number: 物流单号

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OrderDetail](#schemaorderdetail)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OrderDetail](#schemaorderdetail)|

<a id="opIdapi_orders_returns_list"></a>

## GET api_orders_returns_list

GET /api/orders/returns/

列表查询

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ReturnRequestList](#schemareturnrequestlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» order|integer|true|none|关联订单|none|
|»» order_no|string|false|read-only|Order no|none|
|»» user_phone|string|false|read-only|User phone|none|
|»» request_type|string|false|none|申请类型|none|
|»» request_type_display|string|false|read-only|Request type display|none|
|»» reason|string|true|none|退换货原因|none|
|»» status|string|false|none|处理状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» created_at|string(date-time)|false|read-only|申请时间|none|
|»» processed_at|string(date-time)¦null|false|read-only|处理时间|none|

#### 枚举值

|属性|值|
|---|---|
|request_type|return|
|request_type|exchange|
|status|pending|
|status|approved|
|status|rejected|
|status|completed|

<a id="opIdapi_orders_returns_create"></a>

## POST api_orders_returns_create

POST /api/orders/returns/

创建退换货申请

> Body 请求参数

```json
{
  "order": 0,
  "request_type": "return",
  "reason": "string",
  "evidence_images": {}
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ReturnRequestCreate](#schemareturnrequestcreate)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "order": 0,
  "request_type": "return",
  "reason": "string",
  "evidence_images": {}
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ReturnRequestCreate](#schemareturnrequestcreate)|

<a id="opIdapi_orders_returns_read"></a>

## GET api_orders_returns_read

GET /api/orders/returns/{id}/

详情查询

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ReturnRequestDetail](#schemareturnrequestdetail)|

<a id="opIdapi_orders_returns_update"></a>

## PUT 退换货申请视图集

PUT /api/orders/returns/{id}/

提供退换货申请的 CRUD 操作：
- list: 获取退换货申请列表
- retrieve: 获取退换货申请详情
- create: 创建退换货申请
- update: 更新退换货申请（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ReturnRequestDetail](#schemareturnrequestdetail)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ReturnRequestDetail](#schemareturnrequestdetail)|

<a id="opIdapi_orders_returns_partial_update"></a>

## PATCH 退换货申请视图集

PATCH /api/orders/returns/{id}/

提供退换货申请的 CRUD 操作：
- list: 获取退换货申请列表
- retrieve: 获取退换货申请详情
- create: 创建退换货申请
- update: 更新退换货申请（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ReturnRequestDetail](#schemareturnrequestdetail)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ReturnRequestDetail](#schemareturnrequestdetail)|

<a id="opIdapi_orders_returns_delete"></a>

## DELETE 退换货申请视图集

DELETE /api/orders/returns/{id}/

提供退换货申请的 CRUD 操作：
- list: 获取退换货申请列表
- retrieve: 获取退换货申请详情
- create: 创建退换货申请
- update: 更新退换货申请（管理员）

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_orders_returns_process"></a>

## POST 处理退换货申请（管理员操作）

POST /api/orders/returns/{id}/process/

请求参数：
- status: 处理状态 (approved/rejected/completed)
- admin_note: 处理意见

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ReturnRequestDetail](#schemareturnrequestdetail)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ReturnRequestDetail](#schemareturnrequestdetail)|

<a id="opIdapi_products_attributes_list"></a>

## GET api_products_attributes_list

GET /api/products/attributes/

商品属性管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|product|query|string| 否 |none|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ProductAttribute](#schemaproductattribute)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» attr_name|string|true|none|属性名称|none|
|»» attr_value|string|true|none|属性值|none|
|»» sort_order|integer|false|none|排序|none|
|»» created_at|string(date-time)|false|none|创建时间|none|

<a id="opIdapi_products_attributes_create"></a>

## POST api_products_attributes_create

POST /api/products/attributes/

商品属性管理 ViewSet

> Body 请求参数

```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ProductAttribute](#schemaproductattribute)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductAttribute](#schemaproductattribute)|

<a id="opIdapi_products_attributes_read"></a>

## GET api_products_attributes_read

GET /api/products/attributes/{id}/

商品属性管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductAttribute](#schemaproductattribute)|

<a id="opIdapi_products_attributes_update"></a>

## PUT api_products_attributes_update

PUT /api/products/attributes/{id}/

商品属性管理 ViewSet

> Body 请求参数

```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductAttribute](#schemaproductattribute)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductAttribute](#schemaproductattribute)|

<a id="opIdapi_products_attributes_partial_update"></a>

## PATCH api_products_attributes_partial_update

PATCH /api/products/attributes/{id}/

商品属性管理 ViewSet

> Body 请求参数

```json
{
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductAttribute](#schemaproductattribute)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductAttribute](#schemaproductattribute)|

<a id="opIdapi_products_attributes_delete"></a>

## DELETE api_products_attributes_delete

DELETE /api/products/attributes/{id}/

商品属性管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_products_categories_list"></a>

## GET api_products_categories_list

GET /api/products/categories/

获取分类列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[Category](#schemacategory)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|分类名称|none|
|»» parent|integer¦null|false|none|父分类|none|
|»» parent_name|string|false|read-only|Parent name|none|
|»» sort_order|integer|false|none|排序权重|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|
|»» children_count|string|false|read-only|Children count|none|

<a id="opIdapi_products_categories_create"></a>

## POST api_products_categories_create

POST /api/products/categories/

创建分类

> Body 请求参数

```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Category](#schemacategory)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Category](#schemacategory)|

<a id="opIdapi_products_categories_tree"></a>

## GET api_products_categories_tree

GET /api/products/categories/tree/

获取完整分类树

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[Category](#schemacategory)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|分类名称|none|
|»» parent|integer¦null|false|none|父分类|none|
|»» parent_name|string|false|read-only|Parent name|none|
|»» sort_order|integer|false|none|排序权重|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|
|»» children_count|string|false|read-only|Children count|none|

<a id="opIdapi_products_categories_read"></a>

## GET api_products_categories_read

GET /api/products/categories/{id}/

获取分类详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Category](#schemacategory)|

<a id="opIdapi_products_categories_update"></a>

## PUT api_products_categories_update

PUT /api/products/categories/{id}/

更新分类

> Body 请求参数

```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Category](#schemacategory)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Category](#schemacategory)|

<a id="opIdapi_products_categories_partial_update"></a>

## PATCH api_products_categories_partial_update

PATCH /api/products/categories/{id}/

部分更新

> Body 请求参数

```json
{
  "name": "string",
  "parent": 0,
  "sort_order": -2147483648,
  "is_active": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Category](#schemacategory)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Category](#schemacategory)|

<a id="opIdapi_products_categories_delete"></a>

## DELETE api_products_categories_delete

DELETE /api/products/categories/{id}/

删除分类

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_products_images_list"></a>

## GET api_products_images_list

GET /api/products/images/

商品图片管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|product|query|string| 否 |none|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ProductImage](#schemaproductimage)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» image_url|string|true|none|图片URL|none|
|»» sort_order|integer|false|none|排序|none|
|»» created_at|string(date-time)|false|none|创建时间|none|

<a id="opIdapi_products_images_create"></a>

## POST api_products_images_create

POST /api/products/images/

商品图片管理 ViewSet

> Body 请求参数

```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ProductImage](#schemaproductimage)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductImage](#schemaproductimage)|

<a id="opIdapi_products_images_read"></a>

## GET api_products_images_read

GET /api/products/images/{id}/

商品图片管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductImage](#schemaproductimage)|

<a id="opIdapi_products_images_update"></a>

## PUT api_products_images_update

PUT /api/products/images/{id}/

商品图片管理 ViewSet

> Body 请求参数

```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductImage](#schemaproductimage)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductImage](#schemaproductimage)|

<a id="opIdapi_products_images_partial_update"></a>

## PATCH api_products_images_partial_update

PATCH /api/products/images/{id}/

商品图片管理 ViewSet

> Body 请求参数

```json
{
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductImage](#schemaproductimage)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductImage](#schemaproductimage)|

<a id="opIdapi_products_images_delete"></a>

## DELETE api_products_images_delete

DELETE /api/products/images/{id}/

商品图片管理 ViewSet

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_products_products_list"></a>

## GET api_products_products_list

GET /api/products/products/

获取商品列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|category|query|string| 否 |none|
|category__in|query|string| 否 |none|
|price__gte|query|string| 否 |none|
|price__lte|query|string| 否 |none|
|status|query|string| 否 |none|
|is_featured|query|string| 否 |none|
|is_new|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ProductList](#schemaproductlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|商品名称|none|
|»» price|string(decimal)|true|none|销售价格|none|
|»» original_price|string(decimal)|false|none|原价|none|
|»» category|integer¦null|false|none|商品分类|none|
|»» category_name|string|false|read-only|Category name|none|
|»» main_image|string|false|none|主图URL|none|
|»» status|string|false|none|商品状态|none|
|»» sales_count|integer|false|read-only|销量|none|
|»» view_count|integer|false|read-only|浏览量|none|
|»» is_featured|boolean|false|none|是否推荐|none|
|»» is_new|boolean|false|none|是否新品|none|
|»» stock_quantity|integer|false|none|库存数量|none|
|»» image_count|string|false|read-only|Image count|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<a id="opIdapi_products_products_create"></a>

## POST api_products_products_create

POST /api/products/products/

创建商品

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_featured"></a>

## GET api_products_products_featured

GET /api/products/products/featured/

获取推荐商品

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|category|query|string| 否 |none|
|category__in|query|string| 否 |none|
|price__gte|query|string| 否 |none|
|price__lte|query|string| 否 |none|
|status|query|string| 否 |none|
|is_featured|query|string| 否 |none|
|is_new|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ProductList](#schemaproductlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|商品名称|none|
|»» price|string(decimal)|true|none|销售价格|none|
|»» original_price|string(decimal)|false|none|原价|none|
|»» category|integer¦null|false|none|商品分类|none|
|»» category_name|string|false|read-only|Category name|none|
|»» main_image|string|false|none|主图URL|none|
|»» status|string|false|none|商品状态|none|
|»» sales_count|integer|false|read-only|销量|none|
|»» view_count|integer|false|read-only|浏览量|none|
|»» is_featured|boolean|false|none|是否推荐|none|
|»» is_new|boolean|false|none|是否新品|none|
|»» stock_quantity|integer|false|none|库存数量|none|
|»» image_count|string|false|read-only|Image count|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<a id="opIdapi_products_products_new_arrivals"></a>

## GET api_products_products_new_arrivals

GET /api/products/products/new-arrivals/

获取新品上市

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|category|query|string| 否 |none|
|category__in|query|string| 否 |none|
|price__gte|query|string| 否 |none|
|price__lte|query|string| 否 |none|
|status|query|string| 否 |none|
|is_featured|query|string| 否 |none|
|is_new|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ProductList](#schemaproductlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|商品名称|none|
|»» price|string(decimal)|true|none|销售价格|none|
|»» original_price|string(decimal)|false|none|原价|none|
|»» category|integer¦null|false|none|商品分类|none|
|»» category_name|string|false|read-only|Category name|none|
|»» main_image|string|false|none|主图URL|none|
|»» status|string|false|none|商品状态|none|
|»» sales_count|integer|false|read-only|销量|none|
|»» view_count|integer|false|read-only|浏览量|none|
|»» is_featured|boolean|false|none|是否推荐|none|
|»» is_new|boolean|false|none|是否新品|none|
|»» stock_quantity|integer|false|none|库存数量|none|
|»» image_count|string|false|read-only|Image count|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<a id="opIdapi_products_products_read"></a>

## GET api_products_products_read

GET /api/products/products/{id}/

获取商品详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductDetail](#schemaproductdetail)|

<a id="opIdapi_products_products_update"></a>

## PUT api_products_products_update

PUT /api/products/products/{id}/

更新商品

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_partial_update"></a>

## PATCH api_products_products_partial_update

PATCH /api/products/products/{id}/

部分更新（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_delete"></a>

## DELETE api_products_products_delete

DELETE /api/products/products/{id}/

删除商品

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_products_products_archive"></a>

## POST api_products_products_archive

POST /api/products/products/{id}/archive/

下架商品

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_publish"></a>

## POST api_products_products_publish

POST /api/products/products/{id}/publish/

发布商品

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_reviews_read"></a>

## GET api_products_products_reviews_read

GET /api/products/products/{id}/reviews/

获取或提交商品评价

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_products_reviews_create"></a>

## POST api_products_products_reviews_create

POST /api/products/products/{id}/reviews/

获取或提交商品评价

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[ProductList](#schemaproductlist)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ProductList](#schemaproductlist)|

<a id="opIdapi_products_reviews_list"></a>

## GET api_products_reviews_list

GET /api/products/reviews/

获取评价列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|product|query|string| 否 |none|
|rating|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[ReviewList](#schemareviewlist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» rating|integer|false|none|评分|none|
|»» comment|string|false|none|评价内容|none|
|»» images|object|false|none|评价图片|none|
|»» user_id_display|string|false|read-only|User id display|none|
|»» is_anonymous|boolean|false|none|匿名评价|none|
|»» created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|rating|1|
|rating|2|
|rating|3|
|rating|4|
|rating|5|

<a id="opIdapi_products_reviews_create"></a>

## POST 提交商品评价

POST /api/products/reviews/

请求参数：
- product_id: 商品ID（URL中）
- rating: 评分（1-5）
- comment: 评价内容
- images: 评价图片列表
- is_anonymous: 是否匿名
- order_item_id: 订单项ID（可选）

> Body 请求参数

```json
{
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ReviewCreate](#schemareviewcreate)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ReviewCreate](#schemareviewcreate)|

<a id="opIdapi_products_reviews_read"></a>

## GET api_products_reviews_read

GET /api/products/reviews/{id}/

获取评价详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Review](#schemareview)|

<a id="opIdapi_products_reviews_update"></a>

## PUT 商品评价 ViewSet

PUT /api/products/reviews/{id}/

提供以下接口：
- GET /api/products/reviews/ - 获取评价列表
- GET /api/products/reviews/{id}/ - 获取评价详情
- POST /api/products/products/{product_id}/reviews/ - 提交评价
- GET /api/products/products/{product_id}/reviews/ - 获取商品评价列表

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Review](#schemareview)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Review](#schemareview)|

<a id="opIdapi_products_reviews_partial_update"></a>

## PATCH 商品评价 ViewSet

PATCH /api/products/reviews/{id}/

提供以下接口：
- GET /api/products/reviews/ - 获取评价列表
- GET /api/products/reviews/{id}/ - 获取评价详情
- POST /api/products/products/{product_id}/reviews/ - 提交评价
- GET /api/products/products/{product_id}/reviews/ - 获取商品评价列表

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Review](#schemareview)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Review](#schemareview)|

<a id="opIdapi_products_reviews_delete"></a>

## DELETE api_products_reviews_delete

DELETE /api/products/reviews/{id}/

删除评价（管理员）

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_recommendations_products_list"></a>

## GET api_recommendations_products_list

GET /api/recommendations/products/

获取推荐商品列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|rule|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[RecommendedProduct](#schemarecommendedproduct)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» rule|integer|true|none|推荐规则|none|
|»» rule_name|string|false|read-only|Rule name|none|
|»» product|[ProductList](#schemaproductlist)|false|none||none|
|»»» id|integer|false|read-only|ID|none|
|»»» name|string|true|none|商品名称|none|
|»»» price|string(decimal)|true|none|销售价格|none|
|»»» original_price|string(decimal)|false|none|原价|none|
|»»» category|integer¦null|false|none|商品分类|none|
|»»» category_name|string|false|read-only|Category name|none|
|»»» main_image|string|false|none|主图URL|none|
|»»» status|string|false|none|商品状态|none|
|»»» sales_count|integer|false|read-only|销量|none|
|»»» view_count|integer|false|read-only|浏览量|none|
|»»» is_featured|boolean|false|none|是否推荐|none|
|»»» is_new|boolean|false|none|是否新品|none|
|»»» stock_quantity|integer|false|none|库存数量|none|
|»»» image_count|string|false|read-only|Image count|none|
|»»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» sort_order|integer|false|none|排序权重|none|
|»» remark|string|false|none|备注|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<a id="opIdapi_recommendations_products_create"></a>

## POST api_recommendations_products_create

POST /api/recommendations/products/

添加推荐商品

> Body 请求参数

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[RecommendedProductCreate](#schemarecommendedproductcreate)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[RecommendedProductCreate](#schemarecommendedproductcreate)|

<a id="opIdapi_recommendations_products_read"></a>

## GET api_recommendations_products_read

GET /api/recommendations/products/{id}/

获取推荐商品详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendedProduct](#schemarecommendedproduct)|

<a id="opIdapi_recommendations_products_update"></a>

## PUT api_recommendations_products_update

PUT /api/recommendations/products/{id}/

更新推荐商品

> Body 请求参数

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[RecommendedProductCreate](#schemarecommendedproductcreate)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendedProductCreate](#schemarecommendedproductcreate)|

<a id="opIdapi_recommendations_products_partial_update"></a>

## PATCH api_recommendations_products_partial_update

PATCH /api/recommendations/products/{id}/

部分更新（管理员）

> Body 请求参数

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[RecommendedProductCreate](#schemarecommendedproductcreate)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendedProductCreate](#schemarecommendedproductcreate)|

<a id="opIdapi_recommendations_products_delete"></a>

## DELETE api_recommendations_products_delete

DELETE /api/recommendations/products/{id}/

删除推荐商品

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_recommendations_rules_list"></a>

## GET api_recommendations_rules_list

GET /api/recommendations/rules/

获取推荐规则列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|rule_type|query|string| 否 |none|
|is_active|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[RecommendationRule](#schemarecommendationrule)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|规则名称|none|
|»» rule_type|string|false|none|规则类型|none|
|»» rule_type_display|string|false|read-only|Rule type display|none|
|»» description|string|false|none|规则描述|none|
|»» config|object|false|none|配置参数|none|
|»» priority|integer|false|none|优先级|none|
|»» limit|integer|false|none|限制数量|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» product_count|string|false|read-only|Product count|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|rule_type|hot|
|rule_type|new|
|rule_type|personalized|
|rule_type|category|

<a id="opIdapi_recommendations_rules_create"></a>

## POST api_recommendations_rules_create

POST /api/recommendations/rules/

创建推荐规则

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[RecommendationRule](#schemarecommendationrule)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[RecommendationRule](#schemarecommendationrule)|

<a id="opIdapi_recommendations_rules_active"></a>

## GET api_recommendations_rules_active

GET /api/recommendations/rules/active/

获取启用的推荐规则

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|rule_type|query|string| 否 |none|
|is_active|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[RecommendationRule](#schemarecommendationrule)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» name|string|true|none|规则名称|none|
|»» rule_type|string|false|none|规则类型|none|
|»» rule_type_display|string|false|read-only|Rule type display|none|
|»» description|string|false|none|规则描述|none|
|»» config|object|false|none|配置参数|none|
|»» priority|integer|false|none|优先级|none|
|»» limit|integer|false|none|限制数量|none|
|»» is_active|boolean|false|none|是否启用|none|
|»» product_count|string|false|read-only|Product count|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|rule_type|hot|
|rule_type|new|
|rule_type|personalized|
|rule_type|category|

<a id="opIdapi_recommendations_rules_read"></a>

## GET api_recommendations_rules_read

GET /api/recommendations/rules/{id}/

获取规则详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendationRuleDetail](#schemarecommendationruledetail)|

<a id="opIdapi_recommendations_rules_update"></a>

## PUT api_recommendations_rules_update

PUT /api/recommendations/rules/{id}/

更新推荐规则

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[RecommendationRule](#schemarecommendationrule)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendationRule](#schemarecommendationrule)|

<a id="opIdapi_recommendations_rules_partial_update"></a>

## PATCH api_recommendations_rules_partial_update

PATCH /api/recommendations/rules/{id}/

部分更新（管理员）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[RecommendationRule](#schemarecommendationrule)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RecommendationRule](#schemarecommendationrule)|

<a id="opIdapi_recommendations_rules_delete"></a>

## DELETE api_recommendations_rules_delete

DELETE /api/recommendations/rules/{id}/

删除推荐规则

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_system_configs_list"></a>

## GET api_system_configs_list

GET /api/system/configs/

获取配置列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|category|query|string| 否 |none|
|is_editable|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[SystemConfigList](#schemasystemconfiglist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» key|string|true|none|配置键|none|
|»» value|string|true|none|配置值|none|
|»» description|string|false|none|描述|none|
|»» category|string|false|none|分类|none|
|»» is_editable|boolean|false|none|是否可编辑|none|

#### 枚举值

|属性|值|
|---|---|
|category|basic|
|category|seo|
|category|trade|
|category|other|

<a id="opIdapi_system_configs_create"></a>

## POST api_system_configs_create

POST /api/system/configs/

创建配置

> Body 请求参数

```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[SystemConfig](#schemasystemconfig)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[SystemConfig](#schemasystemconfig)|

<a id="opIdapi_system_configs_read"></a>

## GET api_system_configs_read

GET /api/system/configs/{id}/

获取配置详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SystemConfig](#schemasystemconfig)|

<a id="opIdapi_system_configs_update"></a>

## PUT api_system_configs_update

PUT /api/system/configs/{id}/

更新配置

> Body 请求参数

```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[SystemConfig](#schemasystemconfig)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SystemConfig](#schemasystemconfig)|

<a id="opIdapi_system_configs_partial_update"></a>

## PATCH api_system_configs_partial_update

PATCH /api/system/configs/{id}/

部分更新（管理员）

> Body 请求参数

```json
{
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[SystemConfig](#schemasystemconfig)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SystemConfig](#schemasystemconfig)|

<a id="opIdapi_system_configs_delete"></a>

## DELETE api_system_configs_delete

DELETE /api/system/configs/{id}/

删除配置

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_system_logs_list"></a>

## GET api_system_logs_list

GET /api/system/logs/

获取日志列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|action_type|query|string| 否 |none|
|object_type|query|string| 否 |none|
|status|query|string| 否 |none|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[OperationLogList](#schemaoperationloglist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» operator|integer¦null|false|none|操作人|none|
|»» operator_name|string|false|read-only|Operator name|none|
|»» action_type|string|false|none|操作类型|none|
|»» action_type_display|string|false|read-only|Action type display|none|
|»» object_type|string|false|none|操作对象类型|none|
|»» detail|string|false|none|操作详情|none|
|»» status|string|false|none|状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|action_type|create|
|action_type|update|
|action_type|delete|
|action_type|login|
|action_type|logout|
|action_type|other|
|status|success|
|status|failed|

<a id="opIdapi_system_logs_create"></a>

## POST api_system_logs_create

POST /api/system/logs/

操作日志 ViewSet（仅管理员可访问）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[OperationLog](#schemaoperationlog)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[OperationLog](#schemaoperationlog)|

<a id="opIdapi_system_logs_read"></a>

## GET api_system_logs_read

GET /api/system/logs/{id}/

获取日志详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OperationLog](#schemaoperationlog)|

<a id="opIdapi_system_logs_update"></a>

## PUT api_system_logs_update

PUT /api/system/logs/{id}/

操作日志 ViewSet（仅管理员可访问）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OperationLog](#schemaoperationlog)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OperationLog](#schemaoperationlog)|

<a id="opIdapi_system_logs_partial_update"></a>

## PATCH api_system_logs_partial_update

PATCH /api/system/logs/{id}/

操作日志 ViewSet（仅管理员可访问）

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[OperationLog](#schemaoperationlog)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[OperationLog](#schemaoperationlog)|

<a id="opIdapi_system_logs_delete"></a>

## DELETE api_system_logs_delete

DELETE /api/system/logs/{id}/

操作日志 ViewSet（仅管理员可访问）

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_system_messages_list"></a>

## GET api_system_messages_list

GET /api/system/messages/

获取消息列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[MessageList](#schemamessagelist)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» title|string|true|none|标题|none|
|»» message_type|string|false|none|消息类型|none|
|»» message_type_display|string|false|read-only|Message type display|none|
|»» status|string|false|none|状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» sent_at|string(date-time)¦null|false|none|发送时间|none|
|»» read_at|string(date-time)¦null|false|none|阅读时间|none|
|»» created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|message_type|announcement|
|message_type|notification|
|message_type|promotion|
|message_type|system|
|status|draft|
|status|sent|
|status|read|

<a id="opIdapi_system_messages_create"></a>

## POST api_system_messages_create

POST /api/system/messages/

发送消息

> Body 请求参数

```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[MessageCreate](#schemamessagecreate)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[MessageCreate](#schemamessagecreate)|

<a id="opIdapi_system_messages_my_messages"></a>

## GET 获取当前用户的消息

GET /api/system/messages/my-messages/

查询参数：
- status: 状态筛选（draft/sent/read）
- message_type: 消息类型

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|search|query|string| 否 |搜索关键词。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[Message](#schemamessage)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» recipient|integer¦null|false|none|接收用户|none|
|»» recipient_name|string|false|read-only|Recipient name|none|
|»» title|string|true|none|标题|none|
|»» content|string|true|none|内容|none|
|»» message_type|string|false|none|消息类型|none|
|»» message_type_display|string|false|read-only|Message type display|none|
|»» status|string|false|none|状态|none|
|»» status_display|string|false|read-only|Status display|none|
|»» sent_at|string(date-time)¦null|false|read-only|发送时间|none|
|»» read_at|string(date-time)¦null|false|read-only|阅读时间|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|message_type|announcement|
|message_type|notification|
|message_type|promotion|
|message_type|system|
|status|draft|
|status|sent|
|status|read|

<a id="opIdapi_system_messages_read"></a>

## GET api_system_messages_read

GET /api/system/messages/{id}/

获取消息详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Message](#schemamessage)|

<a id="opIdapi_system_messages_update"></a>

## PUT api_system_messages_update

PUT /api/system/messages/{id}/

更新消息

> Body 请求参数

```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Message](#schemamessage)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Message](#schemamessage)|

<a id="opIdapi_system_messages_partial_update"></a>

## PATCH api_system_messages_partial_update

PATCH /api/system/messages/{id}/

站内消息 ViewSet

> Body 请求参数

```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Message](#schemamessage)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Message](#schemamessage)|

<a id="opIdapi_system_messages_delete"></a>

## DELETE api_system_messages_delete

DELETE /api/system/messages/{id}/

删除消息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_system_messages_mark_read"></a>

## POST api_system_messages_mark_read

POST /api/system/messages/{id}/mark-read/

标记消息已读

> Body 请求参数

```json
{
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement",
  "status": "draft"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[Message](#schemamessage)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Message](#schemamessage)|

<a id="opIdapi_users_list"></a>

## GET api_users_list

GET /api/users/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[User](#schemauser)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» phone|string|true|none|手机号|none|
|»» nickname|string|false|none|昵称|none|
|»» avatar|string(uri)¦null|false|none|头像URL|none|
|»» email|string(email)|false|none|电子邮件地址|none|
|»» points|integer|false|read-only|积分|none|
|»» status|string|false|read-only|状态|none|
|»» created_at|string(date-time)|false|read-only|注册时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_users_create"></a>

## POST api_users_create

POST /api/users/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[User](#schemauser)|

<a id="opIdapi_users_addresses_list"></a>

## GET api_users_addresses_list

GET /api/users/addresses/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[UserAddress](#schemauseraddress)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» user|[User](#schemauser)|false|none||none|
|»»» id|integer|false|read-only|ID|none|
|»»» phone|string|true|none|手机号|none|
|»»» nickname|string|false|none|昵称|none|
|»»» avatar|string(uri)¦null|false|none|头像URL|none|
|»»» email|string(email)|false|none|电子邮件地址|none|
|»»» points|integer|false|read-only|积分|none|
|»»» status|string|false|read-only|状态|none|
|»»» created_at|string(date-time)|false|read-only|注册时间|none|
|»» recipient_name|string|true|none|收货人姓名|none|
|»» phone|string|true|none|收货人手机号|none|
|»» province|string|false|none|省份|none|
|»» city|string|false|none|城市|none|
|»» district|string|false|none|区县|none|
|»» address|string|true|none|详细地址|none|
|»» is_default|boolean|false|none|是否默认地址|none|
|»» created_at|string(date-time)|false|read-only|创建时间|none|
|»» updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_users_addresses_create"></a>

## POST api_users_addresses_create

POST /api/users/addresses/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[UserAddressCreate](#schemauseraddresscreate)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserAddressCreate](#schemauseraddresscreate)|

<a id="opIdapi_users_addresses_read"></a>

## GET api_users_addresses_read

GET /api/users/addresses/{id}/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_users_addresses_update"></a>

## PUT api_users_addresses_update

PUT /api/users/addresses/{id}/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_users_addresses_partial_update"></a>

## PATCH api_users_addresses_partial_update

PATCH /api/users/addresses/{id}/

用户地址视图集

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_users_addresses_delete"></a>

## DELETE api_users_addresses_delete

DELETE /api/users/addresses/{id}/

用户地址视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

<a id="opIdapi_users_addresses_set_default"></a>

## POST api_users_addresses_set_default

POST /api/users/addresses/{id}/set-default/

设为默认地址

> Body 请求参数

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

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[UserAddress](#schemauseraddress)| 是 |none|

> 返回示例

> 201 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserAddress](#schemauseraddress)|

<a id="opIdapi_users_auth_login"></a>

## POST api_users_auth_login

POST /api/users/auth/login/

用户登录

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|None|

<a id="opIdapi_users_auth_register"></a>

## POST api_users_auth_register

POST /api/users/auth/register/

用户注册

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|None|

<a id="opIdapi_users_me"></a>

## GET api_users_me

GET /api/users/me/

获取当前用户信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ordering|query|string| 否 |用于排序结果的字段。|
|page|query|integer| 否 |分页结果集中的页码。|
|page_size|query|integer| 否 |每页返回的结果数量。|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» count|integer|true|none||none|
|» next|string(uri)¦null|false|none||none|
|» previous|string(uri)¦null|false|none||none|
|» results|[[User](#schemauser)]|true|none||none|
|»» id|integer|false|read-only|ID|none|
|»» phone|string|true|none|手机号|none|
|»» nickname|string|false|none|昵称|none|
|»» avatar|string(uri)¦null|false|none|头像URL|none|
|»» email|string(email)|false|none|电子邮件地址|none|
|»» points|integer|false|read-only|积分|none|
|»» status|string|false|read-only|状态|none|
|»» created_at|string(date-time)|false|read-only|注册时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<a id="opIdapi_users_profile"></a>

## PUT api_users_profile

PUT /api/users/profile/

更新当前用户资料

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_users_read"></a>

## GET api_users_read

GET /api/users/{id}/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_users_update"></a>

## PUT api_users_update

PUT /api/users/{id}/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_users_partial_update"></a>

## PATCH api_users_partial_update

PATCH /api/users/{id}/

用户视图集

> Body 请求参数

```json
{
  "phone": "string",
  "nickname": "string",
  "avatar": "http://example.com",
  "email": "user@example.com"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

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

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIdapi_users_delete"></a>

## DELETE api_users_delete

DELETE /api/users/{id}/

用户视图集

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|string| 是 |none|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|none|None|

# 数据模型

<h2 id="tocS_User">User</h2>

<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|phone|string|true|none|手机号|none|
|nickname|string|false|none|昵称|none|
|avatar|string(uri)¦null|false|none|头像URL|none|
|email|string(email)|false|none|电子邮件地址|none|
|points|integer|false|read-only|积分|none|
|status|string|false|read-only|状态|none|
|created_at|string(date-time)|false|read-only|注册时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|active|
|status|banned|

<h2 id="tocS_UserAddress">UserAddress</h2>

<a id="schemauseraddress"></a>
<a id="schema_UserAddress"></a>
<a id="tocSuseraddress"></a>
<a id="tocsuseraddress"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|user|[User](#schemauser)|false|none||none|
|recipient_name|string|true|none|收货人姓名|none|
|phone|string|true|none|收货人手机号|none|
|province|string|false|none|省份|none|
|city|string|false|none|城市|none|
|district|string|false|none|区县|none|
|address|string|true|none|详细地址|none|
|is_default|boolean|false|none|是否默认地址|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

<h2 id="tocS_UserAddressCreate">UserAddressCreate</h2>

<a id="schemauseraddresscreate"></a>
<a id="schema_UserAddressCreate"></a>
<a id="tocSuseraddresscreate"></a>
<a id="tocsuseraddresscreate"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|recipient_name|string|true|none|收货人姓名|none|
|phone|string|true|none|收货人手机号|none|
|province|string|false|none|省份|none|
|city|string|false|none|城市|none|
|district|string|false|none|区县|none|
|address|string|true|none|详细地址|none|
|is_default|boolean|false|none|是否默认地址|none|

<h2 id="tocS_ModificationCaseList">ModificationCaseList</h2>

<a id="schemamodificationcaselist"></a>
<a id="schema_ModificationCaseList"></a>
<a id="tocSmodificationcaselist"></a>
<a id="tocsmodificationcaselist"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|title|string|true|none|标题|none|
|summary|string|false|none|摘要|none|
|cover_image|string|false|none|封面图片URL|none|
|author|string|false|none|作者|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|view_count|integer|false|read-only|浏览量|none|
|published_at|string(date-time)¦null|false|none|发布时间|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|published|

<h2 id="tocS_ModificationCaseCreate">ModificationCaseCreate</h2>

<a id="schemamodificationcasecreate"></a>
<a id="schema_ModificationCaseCreate"></a>
<a id="tocSmodificationcasecreate"></a>
<a id="tocsmodificationcasecreate"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|title|string|true|none|标题|none|
|summary|string|false|none|摘要|none|
|content|string|true|none|内容|none|
|cover_image|string|false|none|封面图片URL|none|
|author|string|false|none|作者|none|
|status|string|false|none|状态|none|
|sort_order|integer|false|none|排序权重|none|
|published_at|string(date-time)¦null|false|none|发布时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|published|

<h2 id="tocS_ModificationCaseDetail">ModificationCaseDetail</h2>

<a id="schemamodificationcasedetail"></a>
<a id="schema_ModificationCaseDetail"></a>
<a id="tocSmodificationcasedetail"></a>
<a id="tocsmodificationcasedetail"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|title|string|true|none|标题|none|
|summary|string|false|none|摘要|none|
|content|string|true|none|内容|none|
|cover_image|string|false|none|封面图片URL|none|
|author|string|false|none|作者|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|view_count|integer|false|read-only|浏览量|none|
|sort_order|integer|false|none|排序权重|none|
|published_at|string(date-time)¦null|false|none|发布时间|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|published|

<h2 id="tocS_ModificationCaseUpdate">ModificationCaseUpdate</h2>

<a id="schemamodificationcaseupdate"></a>
<a id="schema_ModificationCaseUpdate"></a>
<a id="tocSmodificationcaseupdate"></a>
<a id="tocsmodificationcaseupdate"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|title|string|false|none|标题|none|
|summary|string|false|none|摘要|none|
|content|string|false|none|内容|none|
|cover_image|string|false|none|封面图片URL|none|
|author|string|false|none|作者|none|
|status|string|false|none|状态|none|
|sort_order|integer|false|none|排序权重|none|
|published_at|string(date-time)¦null|false|none|发布时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|published|

<h2 id="tocS_FAQ">FAQ</h2>

<a id="schemafaq"></a>
<a id="schema_FAQ"></a>
<a id="tocSfaq"></a>
<a id="tocsfaq"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|question|string|true|none|问题|none|
|answer|string|true|none|答案|none|
|category|string|false|none|分类|none|
|category_display|string|false|read-only|Category display|none|
|sort_order|integer|false|none|排序|none|
|is_active|boolean|false|none|是否启用|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|category|order|
|category|payment|
|category|shipping|
|category|product|
|category|return|
|category|account|
|category|other|

<h2 id="tocS_CouponList">CouponList</h2>

<a id="schemacouponlist"></a>
<a id="schema_CouponList"></a>
<a id="tocScouponlist"></a>
<a id="tocscouponlist"></a>

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
  "issued_quantity": -2147483648,
  "is_active": true
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|优惠券名称|none|
|description|string|false|none|优惠券描述|none|
|discount_type|string|false|none|优惠类型|none|
|min_amount|string(decimal)|false|none|使用门槛|none|
|discount_amount|string(decimal)|false|none|优惠金额|none|
|discount_rate|string(decimal)¦null|false|none|折扣率|none|
|valid_from|string(date-time)|true|none|有效期开始|none|
|valid_until|string(date-time)|true|none|有效期结束|none|
|total_quantity|integer|false|none|发放总量|none|
|issued_quantity|integer|false|none|已发放数量|none|
|is_active|boolean|false|none|是否启用|none|

#### 枚举值

|属性|值|
|---|---|
|discount_type|full_reduction|
|discount_type|discount|

<h2 id="tocS_Coupon">Coupon</h2>

<a id="schemacoupon"></a>
<a id="schema_Coupon"></a>
<a id="tocScoupon"></a>
<a id="tocscoupon"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|优惠券名称|none|
|description|string|false|none|优惠券描述|none|
|discount_type|string|false|none|优惠类型|none|
|min_amount|string(decimal)|false|none|使用门槛|none|
|discount_amount|string(decimal)|false|none|优惠金额|none|
|discount_rate|string(decimal)¦null|false|none|折扣率|none|
|valid_from|string(date-time)|true|none|有效期开始|none|
|valid_until|string(date-time)|true|none|有效期结束|none|
|total_quantity|integer|false|none|发放总量|none|
|per_user_limit|integer|false|none|每人限领数量|none|
|issued_quantity|integer|false|read-only|已发放数量|none|
|is_active|boolean|false|none|是否启用|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|discount_type|full_reduction|
|discount_type|discount|

<h2 id="tocS_UserCoupon">UserCoupon</h2>

<a id="schemausercoupon"></a>
<a id="schema_UserCoupon"></a>
<a id="tocSusercoupon"></a>
<a id="tocsusercoupon"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|coupon|[Coupon](#schemacoupon)|false|none||none|
|coupon_id|integer|true|none|Coupon id|none|
|status|string|false|read-only|使用状态|none|
|used_order|integer¦null|false|read-only|使用的订单|none|
|obtained_at|string(date-time)|false|read-only|领取时间|none|
|used_at|string(date-time)¦null|false|read-only|使用时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|unused|
|status|used|
|status|expired|

<h2 id="tocS_OrderList">OrderList</h2>

<a id="schemaorderlist"></a>
<a id="schema_OrderList"></a>
<a id="tocSorderlist"></a>
<a id="tocsorderlist"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|order_no|string|false|read-only|订单号|none|
|user|integer|true|none|所属用户|none|
|user_phone|string|false|read-only|User phone|none|
|user_nickname|string|false|read-only|User nickname|none|
|total_amount|string(decimal)|false|none|订单总额|none|
|discount_amount|string(decimal)|false|none|优惠金额|none|
|pay_amount|string(decimal)|false|none|实付金额|none|
|status|string|false|none|订单状态|none|
|status_display|string|false|read-only|Status display|none|
|items_count|integer|false|read-only|Items count|none|
|express_company|string|false|none|物流公司|none|
|tracking_number|string|false|none|物流单号|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|pending_shipment|
|status|shipped|
|status|completed|
|status|cancelled|

<h2 id="tocS_OrderItemCreate">OrderItemCreate</h2>

<a id="schemaorderitemcreate"></a>
<a id="schema_OrderItemCreate"></a>
<a id="tocSorderitemcreate"></a>
<a id="tocsorderitemcreate"></a>

```json
{
  "product": 0,
  "quantity": 4294967295
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|product|integer¦null|false|none|商品|none|
|quantity|integer|false|none|购买数量|none|

<h2 id="tocS_OrderCreate">OrderCreate</h2>

<a id="schemaordercreate"></a>
<a id="schema_OrderCreate"></a>
<a id="tocSordercreate"></a>
<a id="tocsordercreate"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|recipient_name|string|true|none|收货人姓名|none|
|recipient_phone|string|true|none|收货人手机号|none|
|recipient_province|string|false|none|省份|none|
|recipient_city|string|false|none|城市|none|
|recipient_district|string|false|none|区县|none|
|recipient_address|string|true|none|详细地址|none|
|total_amount|string(decimal)|false|none|订单总额|none|
|discount_amount|string(decimal)|false|none|优惠金额|none|
|shipping_fee|string(decimal)|false|none|运费|none|
|pay_amount|string(decimal)|false|none|实付金额|none|
|coupon_id|integer¦null|false|none|Coupon id|none|
|items|[[OrderItemCreate](#schemaorderitemcreate)]|true|none||none|
|remark|string|false|none|订单备注|none|

<h2 id="tocS_OrderItem">OrderItem</h2>

<a id="schemaorderitem"></a>
<a id="schema_OrderItem"></a>
<a id="tocSorderitem"></a>
<a id="tocsorderitem"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|product|integer¦null|false|none|商品|none|
|product_name|string|true|none|商品名称|none|
|product_image|string(uri)|false|none|商品图片|none|
|product_price|string(decimal)|true|none|购买单价|none|
|quantity|integer|false|none|购买数量|none|
|subtotal|string(decimal)|false|read-only|小计金额|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

<h2 id="tocS_OrderDetail">OrderDetail</h2>

<a id="schemaorderdetail"></a>
<a id="schema_OrderDetail"></a>
<a id="tocSorderdetail"></a>
<a id="tocsorderdetail"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|order_no|string|false|read-only|订单号|none|
|user|integer|false|read-only|所属用户|none|
|user_phone|string|false|read-only|User phone|none|
|user_nickname|string|false|read-only|User nickname|none|
|recipient_name|string|true|none|收货人姓名|none|
|recipient_phone|string|true|none|收货人手机号|none|
|recipient_province|string|false|none|省份|none|
|recipient_city|string|false|none|城市|none|
|recipient_district|string|false|none|区县|none|
|recipient_address|string|true|none|详细地址|none|
|full_address|string|false|read-only|Full address|none|
|total_amount|string(decimal)|false|read-only|订单总额|none|
|discount_amount|string(decimal)|false|read-only|优惠金额|none|
|shipping_fee|string(decimal)|false|none|运费|none|
|pay_amount|string(decimal)|false|read-only|实付金额|none|
|coupon|integer¦null|false|none|使用的优惠券|none|
|coupon_name|string¦null|false|read-only|Coupon name|none|
|status|string|false|none|订单状态|none|
|status_display|string|false|read-only|Status display|none|
|express_company|string|false|none|物流公司|none|
|tracking_number|string|false|none|物流单号|none|
|remark|string|false|none|订单备注|none|
|items|[[OrderItem](#schemaorderitem)]|false|read-only||none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|
|paid_at|string(date-time)¦null|false|none|付款时间|none|
|shipped_at|string(date-time)¦null|false|none|发货时间|none|
|completed_at|string(date-time)¦null|false|none|完成时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|pending_shipment|
|status|shipped|
|status|completed|
|status|cancelled|

<h2 id="tocS_OrderUpdate">OrderUpdate</h2>

<a id="schemaorderupdate"></a>
<a id="schema_OrderUpdate"></a>
<a id="tocSorderupdate"></a>
<a id="tocsorderupdate"></a>

```json
{
  "status": "pending_payment",
  "express_company": "string",
  "tracking_number": "string",
  "remark": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|status|string|false|none|订单状态|none|
|express_company|string|false|none|物流公司|none|
|tracking_number|string|false|none|物流单号|none|
|remark|string|false|none|订单备注|none|

#### 枚举值

|属性|值|
|---|---|
|status|pending_payment|
|status|pending_shipment|
|status|shipped|
|status|completed|
|status|cancelled|

<h2 id="tocS_ReturnRequestList">ReturnRequestList</h2>

<a id="schemareturnrequestlist"></a>
<a id="schema_ReturnRequestList"></a>
<a id="tocSreturnrequestlist"></a>
<a id="tocsreturnrequestlist"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|order|integer|true|none|关联订单|none|
|order_no|string|false|read-only|Order no|none|
|user_phone|string|false|read-only|User phone|none|
|request_type|string|false|none|申请类型|none|
|request_type_display|string|false|read-only|Request type display|none|
|reason|string|true|none|退换货原因|none|
|status|string|false|none|处理状态|none|
|status_display|string|false|read-only|Status display|none|
|created_at|string(date-time)|false|read-only|申请时间|none|
|processed_at|string(date-time)¦null|false|read-only|处理时间|none|

#### 枚举值

|属性|值|
|---|---|
|request_type|return|
|request_type|exchange|
|status|pending|
|status|approved|
|status|rejected|
|status|completed|

<h2 id="tocS_ReturnRequestCreate">ReturnRequestCreate</h2>

<a id="schemareturnrequestcreate"></a>
<a id="schema_ReturnRequestCreate"></a>
<a id="tocSreturnrequestcreate"></a>
<a id="tocsreturnrequestcreate"></a>

```json
{
  "order": 0,
  "request_type": "return",
  "reason": "string",
  "evidence_images": {}
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|order|integer|true|none|关联订单|none|
|request_type|string|false|none|申请类型|none|
|reason|string|true|none|退换货原因|none|
|evidence_images|object¦null|false|none|凭证图片URL列表|none|

#### 枚举值

|属性|值|
|---|---|
|request_type|return|
|request_type|exchange|

<h2 id="tocS_ReturnRequestDetail">ReturnRequestDetail</h2>

<a id="schemareturnrequestdetail"></a>
<a id="schema_ReturnRequestDetail"></a>
<a id="tocSreturnrequestdetail"></a>
<a id="tocsreturnrequestdetail"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|order|integer|true|none|关联订单|none|
|order_info|[OrderList](#schemaorderlist)|false|none||none|
|request_type|string|false|none|申请类型|none|
|request_type_display|string|false|read-only|Request type display|none|
|reason|string|true|none|退换货原因|none|
|evidence_images|object¦null|false|none|凭证图片URL列表|none|
|status|string|false|none|处理状态|none|
|status_display|string|false|read-only|Status display|none|
|admin_note|string|false|none|处理意见|none|
|created_at|string(date-time)|false|read-only|申请时间|none|
|processed_at|string(date-time)¦null|false|read-only|处理时间|none|

#### 枚举值

|属性|值|
|---|---|
|request_type|return|
|request_type|exchange|
|status|pending|
|status|approved|
|status|rejected|
|status|completed|

<h2 id="tocS_ProductAttribute">ProductAttribute</h2>

<a id="schemaproductattribute"></a>
<a id="schema_ProductAttribute"></a>
<a id="tocSproductattribute"></a>
<a id="tocsproductattribute"></a>

```json
{
  "id": 0,
  "attr_name": "string",
  "attr_value": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|attr_name|string|true|none|属性名称|none|
|attr_value|string|true|none|属性值|none|
|sort_order|integer|false|none|排序|none|
|created_at|string(date-time)|false|none|创建时间|none|

<h2 id="tocS_Category">Category</h2>

<a id="schemacategory"></a>
<a id="schema_Category"></a>
<a id="tocScategory"></a>
<a id="tocscategory"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|分类名称|none|
|parent|integer¦null|false|none|父分类|none|
|parent_name|string|false|read-only|Parent name|none|
|sort_order|integer|false|none|排序权重|none|
|is_active|boolean|false|none|是否启用|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|
|children_count|string|false|read-only|Children count|none|

<h2 id="tocS_ProductImage">ProductImage</h2>

<a id="schemaproductimage"></a>
<a id="schema_ProductImage"></a>
<a id="tocSproductimage"></a>
<a id="tocsproductimage"></a>

```json
{
  "id": 0,
  "image_url": "string",
  "sort_order": -2147483648,
  "created_at": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|image_url|string|true|none|图片URL|none|
|sort_order|integer|false|none|排序|none|
|created_at|string(date-time)|false|none|创建时间|none|

<h2 id="tocS_ProductList">ProductList</h2>

<a id="schemaproductlist"></a>
<a id="schema_ProductList"></a>
<a id="tocSproductlist"></a>
<a id="tocsproductlist"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|商品名称|none|
|price|string(decimal)|true|none|销售价格|none|
|original_price|string(decimal)|false|none|原价|none|
|category|integer¦null|false|none|商品分类|none|
|category_name|string|false|read-only|Category name|none|
|main_image|string|false|none|主图URL|none|
|status|string|false|none|商品状态|none|
|sales_count|integer|false|read-only|销量|none|
|view_count|integer|false|read-only|浏览量|none|
|is_featured|boolean|false|none|是否推荐|none|
|is_new|boolean|false|none|是否新品|none|
|stock_quantity|integer|false|none|库存数量|none|
|image_count|string|false|read-only|Image count|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<h2 id="tocS_ProductDetail">ProductDetail</h2>

<a id="schemaproductdetail"></a>
<a id="schema_ProductDetail"></a>
<a id="tocSproductdetail"></a>
<a id="tocsproductdetail"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|商品名称|none|
|description|string|false|none|商品描述|none|
|price|string(decimal)|true|none|销售价格|none|
|original_price|string(decimal)|false|none|原价|none|
|category|integer¦null|false|none|商品分类|none|
|category_name|string|false|read-only|Category name|none|
|main_image|string|false|none|主图URL|none|
|status|string|false|none|商品状态|none|
|stock_quantity|integer|false|none|库存数量|none|
|sales_count|integer|false|read-only|销量|none|
|view_count|integer|false|read-only|浏览量|none|
|is_featured|boolean|false|none|是否推荐|none|
|is_new|boolean|false|none|是否新品|none|
|images|[[ProductImage](#schemaproductimage)]|false|read-only||none|
|attributes|[[ProductAttribute](#schemaproductattribute)]|false|read-only||none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|status|draft|
|status|pending|
|status|published|
|status|archived|

<h2 id="tocS_ReviewList">ReviewList</h2>

<a id="schemareviewlist"></a>
<a id="schema_ReviewList"></a>
<a id="tocSreviewlist"></a>
<a id="tocsreviewlist"></a>

```json
{
  "id": 0,
  "rating": 1,
  "comment": "string",
  "images": {},
  "user_id_display": "string",
  "is_anonymous": true,
  "created_at": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|rating|integer|false|none|评分|none|
|comment|string|false|none|评价内容|none|
|images|object|false|none|评价图片|none|
|user_id_display|string|false|read-only|User id display|none|
|is_anonymous|boolean|false|none|匿名评价|none|
|created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|rating|1|
|rating|2|
|rating|3|
|rating|4|
|rating|5|

<h2 id="tocS_ReviewCreate">ReviewCreate</h2>

<a id="schemareviewcreate"></a>
<a id="schema_ReviewCreate"></a>
<a id="tocSreviewcreate"></a>
<a id="tocsreviewcreate"></a>

```json
{
  "order_item_id": -2147483648,
  "rating": 1,
  "comment": "string",
  "images": {},
  "is_anonymous": true
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|order_item_id|integer¦null|false|none|订单项ID|none|
|rating|integer|false|none|评分|none|
|comment|string|false|none|评价内容|none|
|images|object|false|none|评价图片|none|
|is_anonymous|boolean|false|none|匿名评价|none|

#### 枚举值

|属性|值|
|---|---|
|rating|1|
|rating|2|
|rating|3|
|rating|4|
|rating|5|

<h2 id="tocS_Review">Review</h2>

<a id="schemareview"></a>
<a id="schema_Review"></a>
<a id="tocSreview"></a>
<a id="tocsreview"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|product|integer|true|none|商品|none|
|product_name|string|false|read-only|Product name|none|
|user_id|integer|true|none|用户ID|none|
|user_id_display|string|false|read-only|User id display|none|
|order_item_id|integer¦null|false|none|订单项ID|none|
|rating|integer|false|none|评分|none|
|comment|string|false|none|评价内容|none|
|images|object|false|none|评价图片|none|
|is_anonymous|boolean|false|none|匿名评价|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|rating|1|
|rating|2|
|rating|3|
|rating|4|
|rating|5|

<h2 id="tocS_RecommendedProduct">RecommendedProduct</h2>

<a id="schemarecommendedproduct"></a>
<a id="schema_RecommendedProduct"></a>
<a id="tocSrecommendedproduct"></a>
<a id="tocsrecommendedproduct"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|rule|integer|true|none|推荐规则|none|
|rule_name|string|false|read-only|Rule name|none|
|product|[ProductList](#schemaproductlist)|false|none||none|
|sort_order|integer|false|none|排序权重|none|
|remark|string|false|none|备注|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

<h2 id="tocS_RecommendedProductCreate">RecommendedProductCreate</h2>

<a id="schemarecommendedproductcreate"></a>
<a id="schema_RecommendedProductCreate"></a>
<a id="tocSrecommendedproductcreate"></a>
<a id="tocsrecommendedproductcreate"></a>

```json
{
  "rule": 0,
  "product": 0,
  "sort_order": -2147483648,
  "remark": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|rule|integer|true|none|推荐规则|none|
|product|integer|true|none|商品|none|
|sort_order|integer|false|none|排序权重|none|
|remark|string|false|none|备注|none|

<h2 id="tocS_RecommendationRule">RecommendationRule</h2>

<a id="schemarecommendationrule"></a>
<a id="schema_RecommendationRule"></a>
<a id="tocSrecommendationrule"></a>
<a id="tocsrecommendationrule"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|规则名称|none|
|rule_type|string|false|none|规则类型|none|
|rule_type_display|string|false|read-only|Rule type display|none|
|description|string|false|none|规则描述|none|
|config|object|false|none|配置参数|none|
|priority|integer|false|none|优先级|none|
|limit|integer|false|none|限制数量|none|
|is_active|boolean|false|none|是否启用|none|
|product_count|string|false|read-only|Product count|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|rule_type|hot|
|rule_type|new|
|rule_type|personalized|
|rule_type|category|

<h2 id="tocS_RecommendationRuleDetail">RecommendationRuleDetail</h2>

<a id="schemarecommendationruledetail"></a>
<a id="schema_RecommendationRuleDetail"></a>
<a id="tocSrecommendationruledetail"></a>
<a id="tocsrecommendationruledetail"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|name|string|true|none|规则名称|none|
|rule_type|string|false|none|规则类型|none|
|rule_type_display|string|false|read-only|Rule type display|none|
|description|string|false|none|规则描述|none|
|config|object|false|none|配置参数|none|
|priority|integer|false|none|优先级|none|
|limit|integer|false|none|限制数量|none|
|is_active|boolean|false|none|是否启用|none|
|recommended_products|string|false|read-only|Recommended products|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|rule_type|hot|
|rule_type|new|
|rule_type|personalized|
|rule_type|category|

<h2 id="tocS_SystemConfigList">SystemConfigList</h2>

<a id="schemasystemconfiglist"></a>
<a id="schema_SystemConfigList"></a>
<a id="tocSsystemconfiglist"></a>
<a id="tocssystemconfiglist"></a>

```json
{
  "id": 0,
  "key": "string",
  "value": "string",
  "description": "string",
  "category": "basic",
  "is_editable": true
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|key|string|true|none|配置键|none|
|value|string|true|none|配置值|none|
|description|string|false|none|描述|none|
|category|string|false|none|分类|none|
|is_editable|boolean|false|none|是否可编辑|none|

#### 枚举值

|属性|值|
|---|---|
|category|basic|
|category|seo|
|category|trade|
|category|other|

<h2 id="tocS_SystemConfig">SystemConfig</h2>

<a id="schemasystemconfig"></a>
<a id="schema_SystemConfig"></a>
<a id="tocSsystemconfig"></a>
<a id="tocssystemconfig"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|key|string|true|none|配置键|none|
|value|string|true|none|配置值|none|
|description|string|false|none|描述|none|
|category|string|false|none|分类|none|
|is_editable|boolean|false|none|是否可编辑|none|
|created_at|string(date-time)|false|read-only|创建时间|none|
|updated_at|string(date-time)|false|read-only|更新时间|none|

#### 枚举值

|属性|值|
|---|---|
|category|basic|
|category|seo|
|category|trade|
|category|other|

<h2 id="tocS_OperationLogList">OperationLogList</h2>

<a id="schemaoperationloglist"></a>
<a id="schema_OperationLogList"></a>
<a id="tocSoperationloglist"></a>
<a id="tocsoperationloglist"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|operator|integer¦null|false|none|操作人|none|
|operator_name|string|false|read-only|Operator name|none|
|action_type|string|false|none|操作类型|none|
|action_type_display|string|false|read-only|Action type display|none|
|object_type|string|false|none|操作对象类型|none|
|detail|string|false|none|操作详情|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|action_type|create|
|action_type|update|
|action_type|delete|
|action_type|login|
|action_type|logout|
|action_type|other|
|status|success|
|status|failed|

<h2 id="tocS_OperationLog">OperationLog</h2>

<a id="schemaoperationlog"></a>
<a id="schema_OperationLog"></a>
<a id="tocSoperationlog"></a>
<a id="tocsoperationlog"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|operator|integer¦null|false|none|操作人|none|
|operator_name|string|false|read-only|Operator name|none|
|action_type|string|false|none|操作类型|none|
|action_type_display|string|false|read-only|Action type display|none|
|object_type|string|false|none|操作对象类型|none|
|object_id|string|false|none|操作对象ID|none|
|detail|string|false|none|操作详情|none|
|ip_address|string¦null|false|none|IP地址|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|error_message|string|false|none|错误信息|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|action_type|create|
|action_type|update|
|action_type|delete|
|action_type|login|
|action_type|logout|
|action_type|other|
|status|success|
|status|failed|

<h2 id="tocS_MessageList">MessageList</h2>

<a id="schemamessagelist"></a>
<a id="schema_MessageList"></a>
<a id="tocSmessagelist"></a>
<a id="tocsmessagelist"></a>

```json
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

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|title|string|true|none|标题|none|
|message_type|string|false|none|消息类型|none|
|message_type_display|string|false|read-only|Message type display|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|sent_at|string(date-time)¦null|false|none|发送时间|none|
|read_at|string(date-time)¦null|false|none|阅读时间|none|
|created_at|string(date-time)|false|none|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|message_type|announcement|
|message_type|notification|
|message_type|promotion|
|message_type|system|
|status|draft|
|status|sent|
|status|read|

<h2 id="tocS_MessageCreate">MessageCreate</h2>

<a id="schemamessagecreate"></a>
<a id="schema_MessageCreate"></a>
<a id="tocSmessagecreate"></a>
<a id="tocsmessagecreate"></a>

```json
{
  "id": 0,
  "recipient": 0,
  "title": "string",
  "content": "string",
  "message_type": "announcement"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|recipient|integer¦null|false|none|接收用户|none|
|title|string|true|none|标题|none|
|content|string|true|none|内容|none|
|message_type|string|true|none|消息类型|none|

#### 枚举值

|属性|值|
|---|---|
|message_type|announcement|
|message_type|notification|
|message_type|promotion|
|message_type|system|

<h2 id="tocS_Message">Message</h2>

<a id="schemamessage"></a>
<a id="schema_Message"></a>
<a id="tocSmessage"></a>
<a id="tocsmessage"></a>

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

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only|ID|none|
|recipient|integer¦null|false|none|接收用户|none|
|recipient_name|string|false|read-only|Recipient name|none|
|title|string|true|none|标题|none|
|content|string|true|none|内容|none|
|message_type|string|false|none|消息类型|none|
|message_type_display|string|false|read-only|Message type display|none|
|status|string|false|none|状态|none|
|status_display|string|false|read-only|Status display|none|
|sent_at|string(date-time)¦null|false|read-only|发送时间|none|
|read_at|string(date-time)¦null|false|read-only|阅读时间|none|
|created_at|string(date-time)|false|read-only|创建时间|none|

#### 枚举值

|属性|值|
|---|---|
|message_type|announcement|
|message_type|notification|
|message_type|promotion|
|message_type|system|
|status|draft|
|status|sent|
|status|read|

