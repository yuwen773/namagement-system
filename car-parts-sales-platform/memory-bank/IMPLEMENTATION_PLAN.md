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
| POST | /api/orders/orders/{id}/cancel/ | 取消订单 |
| POST | /api/orders/orders/{id}/confirm/ | 确认收货 |
| POST | /api/orders/orders/{id}/return/ | 申请退换货 |

**验证方法：**
1. 未发货订单可取消
2. 已发货订单可确认收货
3. 完成后订单可申请退换货

#### 3.4.6 管理员订单处理接口

**接口规格：**
- URL: `POST /api/orders/orders/{id}/ship/`
- 请求体: `{ "express_company": "顺丰", "tracking_number": "SF123456" }`

**验证方法：**
1. 待发货订单发货成功
2. 订单状态变为 shipped

### 3.5 优惠券 API

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
### 7.1 公共组件开发

#### 7.1.1 布局组件

**开发内容：**
- Header 组件（Logo、搜索、导航、用户信息）
- Footer 组件（链接、版权信息）
- 侧边栏组件（管理员侧边导航）

**验证方法：**
1. 页面布局正常显示
2. 响应式适配正确

#### 7.1.2 通用组件

**开发内容：**
- Pagination 组件
- ImageUploader 组件
- Dialog 组件
- Message 消息提示

**验证方法：**
1. 组件在不同场景下正常显示和交互

### 7.2 用户端页面开发

#### 7.2.1 首页

**开发内容：**
- 轮播图（营销 Banner）
- 分类导航
- 热门推荐商品
- 新品推荐商品

**验证方法：**
1. 页面加载时间 < 2秒
2. 商品数据正确显示

#### 7.2.2 商品列表页

**开发内容：**
- 分类筛选
- 价格排序
- 商品卡片列表
- 分页功能

**验证方法：**
1. 筛选和排序功能正常
2. 分页切换正常

#### 7.2.3 商品详情页

**开发内容：**
- 商品大图展示
- 属性信息
- 加入购物车
- 相关推荐
- 用户评价

**验证方法：**
1. 图片放大功能正常
2. 加入购物车成功
3. 评价列表正确显示

#### 7.2.4 购物车页面

**开发内容：**
- 商品列表
- 数量调整
- 优惠券选择
- 价格计算
- 结算按钮

**验证方法：**
1. 商品数量修改实时更新价格
2. 优惠券正确抵扣

#### 7.2.5 订单流程页面

**开发内容：**
- 确认订单页（地址选择、优惠券）
- 支付页面（模拟支付）
- 订单列表页
- 订单详情页

**验证方法：**
1. 完整订单流程可执行
2. 订单状态更新正确

#### 7.2.6 用户中心

**开发内容：**
- 个人资料编辑
- 收货地址管理
- 我的优惠券
- 我的评价

**验证方法：**
1. 所有功能正常可用

### 7.3 管理员端页面开发

#### 7.3.1 商品管理页面

**开发内容：**
- 商品列表（带筛选）
- 商品编辑表单
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
- 订单列表（多状态筛选）
- 订单详情
- 发货操作
- 退换货处理

**验证方法：**
1. 发货后物流信息正确保存
2. 退换货流程完整

#### 7.3.4 营销管理页面

**开发内容：**
- 优惠券创建/列表
- 优惠券发放统计

**验证方法：**
1. 优惠券创建后用户可领取

#### 7.3.5 系统管理页面

**开发内容：**
- 改装案例管理
- FAQ 管理
- 系统配置
- 操作日志

**验证方法：**
1. 内容管理功能正常

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
- [ ] 用户端页面完整
- [ ] 管理员端页面完整
- [ ] 响应式布局正常
- [ ] 功能测试全部通过

### 总体检查项
- [ ] 页面加载 < 2秒
- [ ] API 响应 < 500ms
- [ ] 安全测试通过
- [ ] 部署文档完整
