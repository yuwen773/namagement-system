# 汽车改装件销售推荐平台

基于 Django + Vue 3 的汽车改装件电商平台，提供商品管理、订单处理、优惠券营销和个性化推荐功能。

## 项目简介

本平台是一个专注于汽车改装件销售的电子商务系统，主要功能包括：

- **商品管理**：多级分类、商品属性、库存管理、上下架控制
- **用户系统**：手机号注册登录、收货地址管理、个人信息维护
- **订单流程**：购物车、下单、支付模拟、发货、评价、退换货
- **营销系统**：满减/折扣优惠券、促销活动
- **推荐系统**：热门推荐、新品推荐、个性化推荐、分类推荐

## 技术栈

### 后端

| 技术 | 用途 |
|:-----|:-----|
| Python 3.12 | 编程语言 |
| Django 6.0 | Web 框架 |
| Django REST Framework | REST API |
| MySQL 8.0 | 数据库 |
| JWT (djangorestframework-simplejwt) | 认证授权 |
| drf-yasg | API 文档 |

### 前端

| 技术 | 用途 |
|:-----|:-----|
| Vue 3 | 框架 |
| Vite | 构建工具 |
| Element Plus | UI 组件库 |
| Pinia | 状态管理 |
| Vue Router | 路由 |
| Axios | HTTP 客户端 |
| Tailwind CSS | 样式 |

## 快速开始

### 1. 数据库配置

```bash
mysql -u root -p
CREATE DATABASE car_parts CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动服务
python manage.py runserver  # 运行在 http://localhost:8000
```

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev  # 运行在 http://localhost:5173
```

### 4. 生成测试数据

```bash
# 生成 1000+ 商品、用户、订单数据
python scripts/seed_data.py

# 验证数据完整性
python scripts/verify_data.py
```

## 目录结构

```
car-parts-sales-platform/
├── backend/
│   ├── config/              # Django 项目配置
│   ├── apps/
│   │   ├── users/           # 用户认证、地址、浏览历史
│   │   ├── products/        # 商品、分类、评价、图片、属性
│   │   ├── orders/          # 订单、购物车、退换货
│   │   ├── marketing/       # 优惠券、促销
│   │   ├── recommendations/  # 推荐规则
│   │   ├── content/         # 改装案例、FAQ
│   │   └── system/          # 系统配置、消息、日志
│   ├── utils/               # 响应封装、分页、常量
│   ├── scripts/             # 数据种子脚本
│   └── docs/                # 导出的 API 文档
├── frontend/
│   ├── src/
│   │   ├── api/             # API 接口封装
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── router/          # Vue 路由
│   │   ├── views/           # 页面组件
│   │   └── components/      # 公共组件
│   └── public/
├── memory-bank/
│   ├── PRD.md               # 产品需求文档
│   ├── architecture.md      # 架构设计
│   └── dev-standards/       # 开发规范
└── README.md
```

## API 文档

开发阶段可访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 测试账号

| 角色 | 用户名 | 密码 |
|:-----|:-------|:-----|
| 管理员 | admin | admin123 |
| 普通用户 | (手机号) | 123456 |

数据种子脚本会生成：
- 5 个管理员账号
- 20 个普通用户账号
- 1000+ 商品数据
- 100 张优惠券
- 订单、购物车、评价等数据

## 核心业务流程

```
商品上架 → 用户浏览 → 加入购物车 → 下单支付 → 管理员发货 → 用户收货 → 评价
                                    ↓
                              退换货申请 → 管理员审核
```

## 状态机

### 订单状态

```
pending_payment(待付款) → pending_shipment(待发货) → shipped(已发货) → completed(已完成)
         ↓                        ↓                      ↓
     cancelled(已取消)        cancelled(已取消)      return_processing(退货中)
```

### 商品状态

```
draft(草稿) → pending(待审核) → published(已上架) → archived(已归档)
```

## API 响应格式

### 成功响应

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {...}
}
```

### 分页响应

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

### 错误响应

```json
{
    "code": 400,
    "message": "错误信息",
    "data": null,
    "errors": {...}
}
```

## 开发规范

- **后端开发**: 参考 `memory-bank/dev-standards/backend-api-standards.md`
- **前端开发**: 参考 `memory-bank/dev-standards/frontend-api-standards.md`

## License

MIT
