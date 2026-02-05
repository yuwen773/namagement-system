# 汽车改装件销售推荐平台 - 实施计划

> 本文档为 AI 开发者提供逐步实施指南。遵循"先后端开发，提供接口文档，再前端开发"的原则。

---

## 项目概览

| 项目 | 说明 |
| :--- | :--- |
| **项目名称** | 汽车改装件销售推荐平台 |
| **技术栈** | Django 5.2+ / DRF + Vue.js 3.x / Element Plus |
| **数据库** | MySQL 8.0+ |
| **架构模式** | 前后端分离 |

---

## 第一阶段：项目初始化与基础设施

### 1.1 创建 Django 后端项目结构
> 后端的开发标准见 [](.\dev-standards\backend-api-standards.md)
#### 1.1.1 创建项目目录结构

**操作步骤：**
1. 在项目根目录创建 `backend` 文件夹
2. 在 `backend` 内创建以下子目录：
   - `config/` - 项目配置（settings.py、urls.py）
   - `apps/` - Django 应用目录
   - `utils/` - 工具函数和公共模块
   - `static/` - 静态文件
   - `media/` - 上传文件存储
   - `scripts/` - 数据库脚本和工具

**验证方法：**
- 检查目录结构是否符合以下预期：
  ```
  backend/
  ├── config/
  │   ├── __init__.py
  │   ├── settings.py
  │   ├── urls.py
  │   └── wsgi.py
  ├── apps/
  ├── utils/
  ├── static/
  ├── media/
  ├── scripts/
  ├── manage.py
  └── requirements.txt
  ```

#### 1.1.2 配置 Python 虚拟环境和依赖

**操作步骤：**
1. 使用 Python 3.10+ 创建虚拟环境：`python -m venv venv`
2. 安装核心依赖包：
   - `django>=5.2`
   - `djangorestframework>=3.15`
   - `mysqlclient>=2.2` 或 `pymysql`
   - `django-cors-headers>=4.3`
   - `python-jose>=3.3`（JWT认证）
   - `passlib>=1.7`（密码加密） 当前明文
   - `pillow>=10.0`（图片处理）
   - `django-filter>=23.5`（过滤支持）
   - `django-simple-history>=3.5`（历史记录）
3. 创建 `requirements.txt` 文件

**验证方法：**
1. 执行 `python -c "import django; print(django.VERSION)"` 确认 Django 版本 >= 5.2
2. 执行 `pip list` 确认所有依赖包已安装

#### 1.1.3 配置 Django 项目基础设置

**操作步骤：**
1. 在 `config/settings.py` 中配置：
   - `ALLOWED_HOSTS = ['*']`（开发环境）或指定域名
   - `INSTALLED_APPS` 添加 `rest_framework`、`corsheaders`、`django_filters`
   - `MIDDLEWARE` 添加 `corsheaders.middleware.CorsMiddleware`
   - 配置数据库连接（MySQL）
   - 配置静态文件和媒体文件路径
   - 配置 REST Framework 默认设置（分页、认证类）

2. 创建 `.env` 文件存储敏感配置：
   ```env
   DB_NAME=car_parts
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

**验证方法：**
1. 执行 `python manage.py check` 无错误
2. 执行 `python manage.py runserver` 能正常启动
3. 访问 `http://localhost:8000/api/` 返回 DRF API 根视图

---

## 第二阶段：数据库设计与模型开发

### 2.1 设计并创建数据库

#### 2.1.1 创建数据库和用户

**操作步骤：**
1. 登录 MySQL：`mysql -u root -p`
2. 创建数据库：`CREATE DATABASE car_parts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
3. 创建专用用户并授权：
   ```sql
   CREATE USER 'car_parts_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON car_parts.* TO 'car_parts_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

**验证方法：**
- 执行 `SHOW DATABASES;` 确认 `car_parts` 数据库存在
- 执行 `SHOW GRANTS FOR 'car_parts_user'@'localhost';` 确认用户权限正确

### 2.2 创建 Django 数据模型

#### 2.2.1 创建用户认证模块 (users)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp users`
2. 在 `apps/users/models.py` 定义模型：
   - `User` 模型（扩展 AbstractUser）：
     - 手机号（unique）
     - 头像URL
     - 积分
     - 状态（active/banned）
     - 注册时间
   - `UserAddress` 模型：
     - 关联 User
     - 收货人姓名、手机号、详细地址
     - 是否默认地址

**验证方法：**
1. 执行 `python manage.py makemigrations users`
2. 执行 `python manage.py migrate`
3. 执行 `python manage.py check` 无错误

#### 2.2.2 创建商品管理模块 (products)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp products`
2. 定义以下模型：
   - `Category` 模型（支持多级分类）：
     - 名称
     - 父分类（自关联）
     - 排序权重
     - 是否启用
   - `Product` 模型：
     - 名称、描述、价格
     - 关联分类
     - 库存数量
     - 图片URL（主图）
     - 状态（draft/pending/published/archived）
     - 销量、浏览量
     - 创建/更新时间
   - `ProductImage` 模型：
     - 关联 Product
     - 图片URL
     - 排序
   - `ProductAttribute` 模型：
     - 关联 Product
     - 属性名称（如"适配车型"、"材质"、"颜色"）
     - 属性值

**验证方法：**
1. 执行 `python manage.py makemigrations products`
2. 执行 `python manage.py migrate`
3. 登录 Django Admin 确认模型已注册且可正常添加数据

#### 2.2.3 创建订单管理模块 (orders)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp orders`
2. 定义以下模型：
   - `Order` 模型：
     - 订单号（唯一）
     - 关联 User
     - 收货地址信息（冗余存储）
     - 订单状态（pending_payment/shipped/completed/cancelled）
     - 优惠券（可选）
     - 优惠金额
     - 支付金额
     - 物流公司、物流单号
     - 创建/更新时间
   - `OrderItem` 模型：
     - 关联 Order 和 Product
     - 购买单价
     - 购买数量
   - `ReturnRequest` 模型：
     - 关联 Order
     - 申请类型（退货/换货）
     - 原因描述
     - 凭证图片URL
     - 状态（pending/approved/rejected）
     - 处理意见
     - 创建/处理时间

**验证方法：**
1. 执行 `python manage.py makemigrations orders`
2. 执行 `python manage.py migrate`
3. 验证订单状态流转逻辑正确

#### 2.2.4 创建营销管理模块 (marketing)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp marketing`
2. 定义以下模型：
   - `Coupon` 模型：
     - 名称、描述
     - 优惠类型（满减/折扣）
     - 使用门槛、优惠金额/折扣率
     - 有效期（开始/结束）
     - 发放总量、每人限领数量
     - 已发放数量
     - 状态（active/inactive）
   - `UserCoupon` 模型：
     - 关联 User 和 Coupon
     - 获取时间
     - 使用状态（unused/used/expired）
     - 使用时间（关联订单）

**验证方法：**
1. 执行 `python manage.py makemigrations marketing`
2. 执行 `python manage.py migrate`
3. 验证优惠券有效期和数量限制逻辑

#### 2.2.5 创建推荐管理模块 (recommendations)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp recommendations`
2. 定义以下模型：
   - `RecommendationRule` 模型：
     - 规则名称（如"热门推荐"、"新品推荐"）
     - 规则类型（hot/new/collaborative）
     - 配置参数（JSON格式）
     - 优先级
     - 启用状态
   - `RecommendedProduct` 模型：
     - 关联 Rule 和 Product
     - 排序权重

**验证方法：**
1. 执行 `python manage.py makemigrations recommendations`
2. 执行 `python manage.py migrate`

#### 2.2.6 创建内容管理模块 (content)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp content`
2. 定义以下模型：
   - `ModificationCase` 模型（改装案例）：
     - 标题、摘要、内容
     - 封面图片
     - 作者
     - 状态（draft/published）
     - 创建/更新时间
   - `FAQ` 模型（常见问题）：
     - 问题、答案
     - 分类
     - 排序
     - 是否启用

**验证方法：**
1. 执行 `python manage.py makemigrations content`
2. 执行 `python manage.py migrate`

#### 2.2.7 创建系统管理模块 (system)

**操作步骤：**
1. 创建 Django App：`python manage.py startapp system`
2. 定义以下模型：
   - `SystemConfig` 模型：
     - 配置键、配置值
     - 描述
   - `Message` 模型（站内消息）：
     - 关联 User（可为空表示全员）
     - 标题、内容
     - 类型（announcement/notification）
     - 创建时间
   - `OperationLog` 模型（操作日志）：
     - 操作人、操作类型
     - 操作对象、详情
     - IP地址、时间

**验证方法：**
1. 执行 `python manage.py makemigrations system`
2. 执行 `python manage.py migrate`

---

## 第三阶段：后端 API 开发

> **注意**：所有 API 接口必须使用 `utils/response.py` 中的 `ApiResponse` 类进行统一响应封装，确保返回格式为 `{ "code": 200, "message": "...", "data": {...} }`。

### 3.1 认证与授权 API

#### 3.1.1 用户注册接口

**接口规格：**
- URL: `POST /api/auth/register/`
- 请求体: `{ "username": "手机号", "password": "密码", "nickname": "昵称" }`
- 响应: 
  ```json
  {
      "code": 200,
      "message": "注册成功",
      "data": { 
          "token": "jwt_token", 
          "user": { "id": 1, "nickname": "xxx", "phone": "xxx" } 
      }
  }
  ```

**验证方法：**
1. 使用 Postman 或 curl 发送注册请求
2. 验证数据库中用户已创建（**注意：当前阶段密码以明文存储**）
3. 返回有效的 JWT Token
4. 验证响应结构符合统一规范

#### 3.1.2 用户登录接口

**接口规格：**
- URL: `POST /api/auth/login/`
- 请求体: `{ "username": "手机号", "password": "密码" }`
- 响应:
  ```json
  {
      "code": 200,
      "message": "登录成功",
      "data": { 
          "token": "jwt_token", 
          "user": {...} 
      }
  }
  ```

**验证方法：**
1. 使用正确密码登录成功
2. 使用错误密码登录失败（返回 400 且包含错误信息）
3. 验证 Token 能在后续请求中正常使用

#### 3.1.2.1 密码重置接口

**接口规格：**
- URL: `POST /api/auth/password/reset/`
- 请求体: `{ "username": "手机号", "new_password": "新密码", "code": "验证码(模拟)" }`

**验证方法：**
1. 重置后使用新密码可登录

#### 3.1.3 获取当前用户信息

**接口规格：**
- URL: `GET /api/auth/me/`
- 请求头: `Authorization: Bearer <token>`
- 响应:
  ```json
  {
      "code": 200,
      "message": "获取成功",
      "data": { 
          "id": 1, 
          "nickname": "xxx", 
          "phone": "xxx", 
          "points": 100 
      }
  }
  ```

**验证方法：**
1. 携带有效 Token 请求返回用户信息
2. 不携带 Token 请求返回 401

### 3.2 用户管理 API

#### 3.2.0 管理员用户管理接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| GET | /api/users/users/ | 用户列表（管理员） |
| GET | /api/users/users/{id}/ | 用户详情（管理员） |
| PATCH | /api/users/users/{id}/status/ | 禁用/启用用户 |

**验证方法：**
1. 管理员可查看所有用户
2. 禁用后用户无法登录

#### 3.2.1 用户地址管理接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| GET | /api/users/addresses/ | 获取地址列表 |
| POST | /api/users/addresses/ | 新增地址 |
| PUT | /api/users/addresses/{id}/ | 更新地址 |
| DELETE | /api/users/addresses/{id}/ | 删除地址 |
| PATCH | /api/users/addresses/{id}/set-default/ | 设为默认 |

**验证方法：**
1. 创建地址后能在列表中查看
2. 设置默认地址后 API 返回正确的默认地址
3. 删除地址后不再出现在列表中

#### 3.2.2 用户信息更新接口

**接口规格：**
- URL: `PUT /api/users/profile/`
- 请求体: `{ "nickname": "新昵称", "avatar": "头像URL" }`

**验证方法：**
1. 更新昵称后再次查询确认已更改
2. 更新头像 URL 有效

### 3.3 商品管理 API

#### 3.3.0.1 商品分类管理接口（管理员）

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| POST | /api/products/categories/ | 创建分类 |
| PUT | /api/products/categories/{id}/ | 更新分类 |
| DELETE | /api/products/categories/{id}/ | 删除分类 |

**验证方法：**
1. 增删改分类正常

#### 3.3.1 商品分类接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| GET | /api/products/categories/ | 获取分类树 |

**验证方法：**
1. 返回多级分类结构（父子关系正确）
2. 包含分类名称和 ID

#### 3.3.2 商品列表接口

**接口规格：**
- URL: `GET /api/products/products/`
- 查询参数: `category_id`, `min_price`, `max_price`, `ordering`, `page`
- 响应: 分页结果，包含商品基本信息

**验证方法：**
1. 不带参数返回商品列表
2. 按分类筛选返回正确结果
3. 按价格排序返回正确结果
4. 分页功能正常

#### 3.3.3 商品详情接口

**接口规格：**
- URL: `GET /api/products/products/{id}/`
- 响应: 商品完整信息（包含图片、属性、销量）

**验证方法：**
1. 返回商品所有字段
2. 返回关联的图片和属性列表

#### 3.3.4 商品管理后台接口（管理员）

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| POST | /api/products/products/ | 创建商品 |
| PUT | /api/products/products/{id}/ | 完整更新 |
| PATCH | /api/products/products/{id}/ | 部分更新 |
| DELETE | /api/products/products/{id}/ | 删除商品 |
| PATCH | /api/products/products/{id}/publish/ | 发布商品 |

**验证方法：**
1. 普通用户无法访问（返回 403）
2. 管理员可正常 CRUD
3. 发布后商品状态变为 published

### 3.4 订单管理 API

#### 3.4.1 购物车接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| GET | /api/orders/cart/ | 获取购物车 |
| POST | /api/orders/cart/items/ | 添加商品 |
| PUT | /api/orders/cart/items/{id}/ | 更新数量 |
| DELETE | /api/orders/cart/items/{id}/ | 删除商品 |

**验证方法：**
1. 添加商品后购物车包含该商品
2. 修改数量后数据正确更新
3. 删除后商品不在购物车中

#### 3.4.2 订单创建接口

**接口规格：**
- URL: `POST /api/orders/orders/`
- 请求体: `{ "address_id": 1, "coupon_id": (可选) }`
- 响应: 
  ```json
  {
      "code": 201,
      "message": "订单创建成功",
      "data": {
          "order_no": "20260203xxxx",
          "pay_url": "..."
      }
  }
  ```

**验证方法：**
1. 从购物车创建订单成功
2. 使用优惠券金额正确计算
3. 订单状态为 pending_payment
4. 响应代码为 201 (Created)

#### 3.4.3 订单列表接口

**接口规格：**
- URL: `GET /api/orders/orders/`
- 查询参数: `status`（pending_payment/shipped/completed/cancelled）
- 响应: 
  ```json
  {
      "code": 200,
      "message": "获取成功",
      "data": {
          "count": 10,
          "results": [...]
      }
  }
  ```

**验证方法：**
1. 返回用户所有订单
2. 按状态筛选返回正确结果

#### 3.4.4 订单详情接口

**接口规格：**
- URL: `GET /api/orders/orders/{id}/`
- 响应: 订单完整信息（商品列表、物流信息）

**验证方法：**
1. 返回订单所有字段
2. 返回关联的订单商品详情

#### 3.4.5 订单操作接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| POST | /api/orders/orders/{id}/pay/ | 模拟支付 |
| POST | /api/orders/orders/{id}/cancel/ | 取消订单 |
| POST | /api/orders/orders/{id}/confirm/ | 确认收货 |
| POST | /api/orders/orders/{id}/return/ | 申请退换货 |
| GET | /api/orders/returns/ | 售后申请列表 |
| GET | /api/orders/returns/{id}/ | 售后申请详情 |

**验证方法：**
1. 支付后状态变为待发货
2. 未发货订单可取消
3. 已发货订单可确认收货
4. 完成后订单可申请退换货

#### 3.4.6 管理员订单处理接口

**接口规格：**
- URL: `GET /api/orders/admin/orders/` (管理员列表)
- URL: `GET /api/orders/admin/orders/{id}/` (管理员详情)
- URL: `POST /api/orders/orders/{id}/ship/`
- 请求体: `{ "express_company": "顺丰", "tracking_number": "SF123456" }`
- URL: `POST /api/orders/returns/{id}/audit/` (售后审核)

**验证方法：**
1. 待发货订单发货成功
2. 订单状态变为 shipped
3. 售后审核通过/拒绝正常

#### 3.4.7 交易统计接口

**接口规格：**
- URL: `GET /api/orders/stats/`
- 响应: 销售趋势、状态分布、热销商品

**验证方法：**
1. 返回正确的统计数据

### 3.5 优惠券 API

#### 3.5.0.1 营销管理接口（管理员）

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| POST | /api/marketing/coupons/ | 创建优惠券 |
| PUT | /api/marketing/coupons/{id}/ | 更新优惠券 |
| DELETE | /api/marketing/coupons/{id}/ | 删除优惠券 |
| GET | /api/marketing/stats/ | 优惠券发放统计 |
| POST | /api/marketing/promotions/ | 创建促销活动 |
| GET | /api/marketing/promotions/ | 促销活动列表 |
| POST | /api/marketing/banners/ | 上传 Banner |
| GET | /api/marketing/banners/ | 获取 Banner 列表 |

**验证方法：**
1. 管理员可管理优惠券、活动、Banner

#### 3.5.1 优惠券列表接口

**接口规格：**
- URL: `GET /api/marketing/coupons/`
- 查询参数: `status`（active/expired）

**验证方法：**
1. 返回当前可领取的优惠券
2. 显示使用条件和有效期

#### 3.5.2 领取优惠券接口

**接口规格：**
- URL: `POST /api/marketing/coupons/{id}/claim/`

**验证方法：**
1. 领取成功记录到 UserCoupon
2. 超过限领数量时返回错误
3. 过期优惠券不可领取

#### 3.5.3 我的优惠券接口

**接口规格：**
- URL: `GET /api/marketing/my-coupons/`

**验证方法：**
1. 返回用户已领取的优惠券
2. 显示每张券的使用状态

### 3.6 推荐 API

#### 3.6.1 推荐商品接口

**接口规格：**
- URL: `GET /api/recommendations/products/`
- 查询参数: `type`（hot/new/personalized）

**验证方法：**
1. 返回推荐商品列表
2. 不同 type 返回不同推荐结果

#### 3.6.2 热门推荐配置接口（管理员）

**接口规格：**
- URL: `GET/POST/PUT/DELETE /api/recommendations/rules/`

**验证方法：**
1. 管理员可配置推荐规则
2. 规则变更影响推荐结果

### 3.7 内容管理 API

#### 3.7.1 改装案例接口

**接口规格：**
- URL: `GET /api/content/cases/`（用户）
- URL: `POST /api/content/cases/`（管理员）

**验证方法：**
1. 用户可查看已发布案例列表
2. 管理员可创建和发布案例

#### 3.7.2 FAQ 接口

**接口规格：**
- URL: `GET /api/content/faqs/`

**验证方法：**
1. 返回启用的 FAQ 列表

### 3.8 评价 API

#### 3.8.1 提交评价接口

**接口规格：**
- URL: `POST /api/products/products/{id}/reviews/`
- 请求体: `{ "rating": 5, "comment": "评论内容", "images": ["url1"] }`

**验证方法：**
1. 已完成订单可评价
2. 评价成功计入商品评分

#### 3.8.2 商品评价列表接口

**接口规格：**
- URL: `GET /api/products/products/{id}/reviews/`

**验证方法：**
1. 返回该商品的所有评价
2. 包含评分和图片

#### 3.8.3 我的评价接口

**接口规格：**
- URL: `GET /api/products/reviews/me/`

**验证方法：**
1. 返回当前用户的所有评价

### 3.9 系统管理 API

#### 3.9.1 系统配置与日志接口

**接口规格：**
| 方法 | URL | 描述 |
| :--- | :--- | :--- |
| GET | /api/system/config/ | 获取系统配置 |
| POST | /api/system/config/ | 更新配置(管理员) |
| POST | /api/system/messages/ | 发布消息(管理员) |
| GET | /api/system/messages/ | 获取我的消息 |
| GET | /api/system/logs/ | 获取操作日志(管理员) |

**验证方法：**
1. 配置更新生效
2. 消息发布后用户可接收
3. 敏感操作有日志记录

---

## 第四阶段：数据迁移与模拟数据

### 4.1 创建数据库迁移脚本

#### 4.1.1 编写数据填充脚本

**操作步骤：**
1. 创建 `scripts/seed_data.py` 脚本
2. 实现以下数据生成功能：
   - 创建 20 个模拟用户（包含浏览记录、购物车、订单）
   - 创建 5 个管理员用户
   - 创建商品分类（至少3级）
   - 创建 1000+ 商品数据
   - 创建 100+ 优惠券
   - 创建 50+ 改装案例
   - 创建 30+ FAQ

**验证方法：**
1. 执行脚本后数据库数据量符合预期
2. 用户之间的数据有合理的关联性

### 4.2 验证数据完整性

**操作步骤：**
1. 执行 SQL 查询验证数据：
   - 用户数 >= 20
   - 商品数 >= 1000
   - 每个商品至少有一张图片
   - 订单状态分布合理

**验证方法：**
1. 所有查询返回预期结果
2. 外键约束无报错

---

## 第五阶段：接口文档生成

### 5.1 使用 DRF 自动生成文档

**操作步骤：**
1. 安装 `drf-yasg` 或 `drf-spectacular`
2. 配置 Schema 生成
3. 访问 `/swagger/` 或 `/redoc/` 验证文档

**验证方法：**
1. 访问 Swagger UI 可正常显示所有 API
2. 每个接口有完整的参数说明和响应示例

---

## 第六阶段：Vue.js 前端项目初始化
> 使用 frontend-design skill  设计页面
### 6.1 创建前端项目结构

**操作步骤：**
1. 使用 Vite 创建 Vue 3 项目：`npm create vite@latest frontend -- --template vue`
2. 安装核心依赖：
   - `vue-router`
   - `pinia`（状态管理）
   - `axios`（HTTP 请求）
   - `element-plus`
   - `tailwindcss`
   - `echarts`
   - `@vueuse/core`（工具函数）
3. 配置 Tailwind CSS

**验证方法：**
1. 执行 `npm run dev` 能正常启动
2. 访问 `http://localhost:5173` 显示 Vue 默认页面

### 6.2 配置前端项目结构

**操作步骤：**
1. 创建以下目录结构：
   ```
   src/
   ├── api/          # API 接口封装
   ├── components/   # 公共组件
   ├── views/        # 页面组件
   ├── router/       # 路由配置
   ├── stores/       # Pinia 状态管理
   ├── utils/        # 工具函数
   ├── styles/       # 样式文件
   └── assets/       # 静态资源
   ```

**验证方法：**
1. 目录结构符合预期
2. ESLint/Prettier 配置正确

---

## 第七阶段：前端页面开发
> 前端接口对接遵循 [后端 API 标准](dev-standards/frontend-api-standards.md)
> **MUST**:使用 frontend-design skill  设计页面
> **MUST**: 所有页面必须符合 [前端设计系统](docs/frontend-design-system.md) 规范
> **MUST**: 接口对接必须遵循 [后端接口文档](api\api.md) 规范
### 7.1 公共组件开发

#### 7.1.1 布局组件

**开发内容：**
- Header 组件（Logo、搜索框、导航菜单、用户信息、消息中心入口、购物车图标）
- Footer 组件（友情链接、版权信息、备案号）
- 侧边栏组件（管理员侧边导航菜单）
- 面包屑导航组件

**验证方法：**
1. 页面布局正常显示
2. 响应式适配正确（移动端/桌面端）
3. 消息中心入口显示未读消息数量角标

#### 7.1.2 通用组件

**开发内容：**
- Pagination 组件（分页器）
- ImageUploader 组件（图片上传与预览）
- ImagePreview 组件（图片放大查看）
- Dialog 组件（弹窗确认）
- Message 消息提示
- Rating 组件（星级评分）
- Timeline 组件（时间轴展示）

**验证方法：**
1. 组件在不同场景下正常显示和交互

### 7.2 用户端页面开发

#### 7.2.0 认证页面

**开发内容：**
- 登录页面
- 注册页面
- 忘记密码页面

**验证方法：**
1. 注册/登录流程正常
2. Token 正确存储和过期处理

#### 7.2.1 首页

**开发内容：**
- 轮播图（营销 Banner/活动海报）
- 分类导航（图标+文字）
- 热门推荐商品（按销量排序）
- 新品推荐商品（按创建时间排序）
- 猜你喜欢（个性化推荐，基于用户浏览历史）
- 优惠券领券中心入口

**验证方法：**
1. 页面加载时间 < 2秒
2. 商品数据正确显示
3. 未登录用户"猜你喜欢"显示热门商品
4. 已登录用户显示个性化推荐结果

#### 7.2.2 商品列表页

**开发内容：**
- 分类筛选（左侧树形分类导航）
- 价格区间筛选
- 销量/价格/上架时间排序
- 商品卡片列表（含主图、名称、价格、销量）
- 分页功能

**验证方法：**
1. 筛选和排序功能正常
2. 分页切换正常
3. URL 参数同步（支持刷新保持筛选状态）

#### 7.2.3 搜索结果页

**开发内容：**
- 搜索框（顶部 Header + 独立搜索页）
- 关键词高亮显示
- 搜索结果列表（复用商品卡片组件）
- 搜索历史记录
- 热门搜索推荐

**验证方法：**
1. 输入关键词后按回车或点击搜索触发查询
2. 搜索结果中关键词高亮显示
3. 无结果时显示推荐商品
4. 搜索历史本地存储，下次访问时显示

#### 7.2.4 商品详情页

**开发内容：**
- 商品主图展示（多图切换、放大镜预览）
- 商品属性信息（适配车型、材质、规格等）
- 价格/库存/销量显示
- 加入购物车按钮
- 立即购买按钮
- 相关推荐商品
- 用户评价列表（支持图片预览、评分展示）
- 评价提交（星级评分+文字+图片上传）

**验证方法：**
1. 图片放大/切换功能正常
2. 加入购物车后提示成功
3. 评价列表支持图片点击放大
4. 评价提交后实时更新评价统计

#### 7.2.5 购物车页面

**开发内容：**
- 商品列表（勾选、数量调整、删除）
- 优惠券选择下拉框
- 价格实时计算（商品金额、优惠、运费、总额）
- 结算按钮
- 空购物车提示

**验证方法：**
1. 商品数量修改实时更新价格
2. 优惠券选择后正确抵扣金额
3. 全选/反选功能正常
4. 删除商品有二次确认

#### 7.2.6 订单流程页面
> **MUST**:使用 frontend-design skill  设计页面
**开发内容：**
- **确认订单页**：收货地址选择/新增、可用优惠券列表、商品清单、金额明细、提交订单按钮
- **支付页面**（模拟）：订单信息、支付方式选择、支付按钮、支付结果页
- **订单列表页**：订单状态 Tabs（全部/待付款/待发货/待收货/已完成）、订单搜索
- **订单详情页**：订单状态、商品信息、物流信息（时间轴展示）、价格明细、操作按钮

**验证方法：**
1. 完整下单流程可执行（购物车→确认订单→支付→完成）
2. 订单状态实时同步
3. 物流信息正确展示

#### 7.2.7 用户中心
> **MUST**:使用 frontend-design skill  设计页面
**开发内容：**
- **个人资料**：昵称、头像、手机号修改，密码修改
- **收货地址管理**：地址列表、新增/编辑/删除、设为默认
- **我的积分**：当前积分展示、积分明细（获得/消费记录）
- **我的优惠券**：可用/已使用/已过期 Tabs
- **我的评价**：评价列表、查看/删除评价
- **售后/退换货**：申请列表、申请详情页（含进度时间轴）
- **消息中心**：系统通知列表、已读/未读状态、消息详情

**验证方法：**
1. 所有功能正常可用
2. 积分变化实时更新
3. 售后申请详情显示完整的处理进度时间轴

#### 7.2.8 浏览历史页面
> **MUST**:使用 frontend-design skill  设计页面
**开发内容：**
- 按时间倒序展示浏览记录
- 商品卡片展示（缩略图、名称、价格）
- 清空浏览历史功能
- 快速加入购物车/购买按钮

**验证方法：**
1. 浏览商品后历史列表自动更新
2. 点击商品卡片跳转到商品详情
3. 清空历史后列表为空

### 7.3 管理员端页面开发
> 管理端布局必须是 **侧导航栏 + 主内容区域**
> **MUST**:使用 frontend-design skill  设计页面
#### 7.3.1 商品管理页面

**开发内容：**
- 商品分类管理（树形结构编辑）
- 商品列表（带筛选、审核）
- 商品编辑表单（含属性管理）
- 商品图片上传
- 库存管理

**验证方法：**
1. CRUD 操作正常
2. 图片上传成功

#### 7.3.2 用户管理页面

**开发内容：**
- 用户列表
- 用户详情（地址、积分）
- 账号禁用/启用

**验证方法：**
1. 禁用用户后无法登录

#### 7.3.3 订单管理页面

**开发内容：**
- 订单列表（多状态筛选、订单号搜索、用户搜索）
- 订单详情（商品信息、收货地址、物流信息）
- 发货操作（物流公司、物流单号录入）
- 退换货处理（申请审核、处理意见填写）

**验证方法：**
1. 发货后物流信息正确保存
2. 退换货流程完整

#### 7.3.4 交易统计页面（新增）

**开发内容：**
- **销售趋势图表**：日/周/月销售额折线图（使用 ECharts）
- **订单统计**：订单数量、待处理订单、已完成订单统计卡片
- **订单状态分布**：各状态订单数量饼图
- **热销商品排行**：按销量/销售额排序的商品 TOP10
- **优惠券核销统计**：已领取/已使用/过期优惠券数量
- **时间筛选器**：选择统计时间段

**验证方法：**
1. 图表数据实时更新
2. 时间筛选后数据正确变化
3. 图表交互正常（鼠标悬停显示详情）

#### 7.3.5 营销管理页面

**开发内容：**
- **优惠券管理**：创建/编辑优惠券、优惠券列表、发放统计
- **促销活动管理**（新增）：
  - 活动列表（进行中/已结束/未开始）
  - 活动创建表单（活动类型、时间范围、参与商品、优惠规则）
  - 活动效果统计（参与人数、销售额、订单数）
- **营销素材管理**：Banner 图上传与排序、活动海报管理

**验证方法：**
1. 优惠券创建后用户可在领券中心领取
2. 促销活动创建后对应商品显示活动标签
3. Banner 图在首页轮播正确显示

#### 7.3.6 推荐管理页面

**开发内容：**
- **推荐规则配置**：
  - 热门推荐规则（销量权重、浏览量权重）
  - 新品推荐规则（上架时间范围）
  - 个性化推荐参数（浏览历史权重、购买历史权重）
- **推荐内容管理**：手动添加/移除推荐商品、设置推荐权重排序
- **推荐效果监控**：推荐位点击率统计、转化率统计

**验证方法：**
1. 规则修改后首页推荐结果即时更新
2. 手动干预商品显示在推荐位首位

#### 7.3.7 系统管理页面

**开发内容：**
- **改装案例管理**：案例列表、新增/编辑/删除（富文本编辑器）、封面图上传、发布状态切换
- **FAQ 管理**：FAQ 列表、分类管理、排序调整、启用/禁用
- **消息通知发布**：消息列表、新建消息（全员/指定用户）、发送状态
- **系统配置**：网站名称、Logo、SEO 信息、客服联系方式等基础设置
- **操作日志**（新增）：
  - 日志列表（操作人、操作类型、操作对象、IP、时间）
  - 筛选功能（按操作类型、操作人、时间范围）
  - 敏感操作高亮显示（删除商品、修改订单状态等）

**验证方法：**
1. 改装案例在用户端正确显示
2. 发布消息后用户消息中心收到通知
3. 操作日志记录完整且可查询

---

## 第八阶段：测试与优化

### 8.1 后端单元测试

**操作步骤：**
1. 为每个 API 编写测试用例
2. 覆盖正常流程和异常场景
3. 使用 Django TestCase

**验证方法：**
1. 执行 `python manage.py test` 所有测试通过
2. 测试覆盖率 >= 80%

### 8.2 前端功能测试

**操作步骤：**
1. 测试所有用户流程
2. 测试管理员流程
3. 验证响应式布局

**验证方法：**
1. 所有页面功能正常
2. 无明显的 UI 错误

### 8.3 性能测试

**操作步骤：**
1. 测试页面加载时间
2. 测试 API 响应时间
3. 优化慢查询

**验证方法：**
1. 页面加载 < 2秒
2. API 响应 < 500ms

### 8.4 安全测试

**操作步骤：**
1. 测试未授权访问
2. 测试越权操作
3. 测试 XSS/CSRF 防护

**验证方法：**
1. 所有安全测试通过

---

## 第九阶段：部署准备

### 9.1 配置文件整理

**操作步骤：**
1. 创建生产环境配置文件
2. 整理环境变量
3. 配置静态文件收集

**验证方法：**
1. `python manage.py collectstatic` 成功执行

### 9.2 部署文档

**操作步骤：**
1. 编写 Dockerfile
2. 编写 docker-compose.yml
3. 编写部署说明文档

**验证方法：**
1. 使用 Docker 能正常启动所有服务

---

## 实施检查清单

在每个阶段完成后，标记以下检查项：

### 后端检查项
- [ ] 项目结构创建完成
- [ ] 所有模型创建并迁移成功
- [ ] 认证 API 正常工作
- [ ] 商品管理 API 完整
- [ ] 订单管理 API 完整
- [ ] 优惠券 API 完整
- [ ] 推荐 API 完整
- [ ] 接口文档可访问
- [ ] 单元测试覆盖 >= 80%
- [ ] 模拟数据填充完成

### 前端检查项
- [ ] 项目初始化完成
- [ ] API 封装完成

**用户端页面：**
- [ ] 登录/注册页面
- [ ] 首页（含个性化推荐）
- [ ] 商品列表页
- [ ] 搜索结果页
- [ ] 商品详情页（含评价图片预览）
- [ ] 购物车页面
- [ ] 订单流程（确认订单/支付/订单列表/订单详情）
- [ ] 用户中心（含我的积分）
- [ ] 浏览历史页面
- [ ] 售后详情页

**管理员端页面：**
- [ ] 商品管理
- [ ] 用户管理
- [ ] 订单管理
- [ ] 交易统计（新增）
- [ ] 营销管理（含促销活动）
- [ ] 推荐管理
- [ ] 系统管理（含操作日志）
- [ ] 响应式布局正常
- [ ] 功能测试全部通过

### 总体检查项
- [ ] 页面加载 < 2秒
- [ ] API 响应 < 500ms
- [ ] 安全测试通过
- [ ] 部署文档完整
