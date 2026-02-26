# 非物质文化遗产数据可视化系统 - 前端

基于 Vue 3 + TypeScript + Element Plus + ECharts + Tailwind CSS 构建的前端应用。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **语言**: TypeScript
- **UI 组件库**: Element Plus
- **样式**: Tailwind CSS
- **图表**: ECharts
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 请求封装
│   │   ├── auth.ts       # 认证相关接口
│   │   ├── dashboard.ts  # 驾驶舱接口
│   │   ├── heritage.ts   # 非遗项目接口
│   │   ├── inheritor.ts  # 传承人接口
│   │   ├── category.ts   # 分类接口
│   │   └── region.ts     # 地区接口
│   ├── components/       # 公共组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态管理
│   │   └── user.ts       # 用户状态
│   ├── types/            # TypeScript 类型定义
│   │   └── index.ts      # 全局类型
│   ├── utils/            # 工具函数
│   │   └── request.ts    # Axios 封装
│   ├── views/            # 页面组件
│   │   ├── admin/        # 管理页面
│   │   ├── Dashboard.vue # 驾驶舱
│   │   ├── Login.vue     # 登录页
│   │   └── ...
│   ├── App.vue           # 根组件
│   ├── main.ts           # 入口文件
│   └── style.css         # 全局样式
├── public/               # 静态资源
├── index.html            # HTML 模板
├── vite.config.ts        # Vite 配置
├── tailwind.config.js    # Tailwind 配置
├── tsconfig.json         # TypeScript 配置
└── package.json          # 依赖配置
```

## 开发指南

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 功能模块

### 已完成（阶段 8.1-8.4）

- ✅ Vue 3 + TypeScript 项目搭建
- ✅ Element Plus 和 Tailwind CSS 配置
- ✅ 目录结构和基础组件创建
- ✅ 路由和状态管理实现
- ✅ API 请求封装（axios + 拦截器）
- ✅ 类型定义（TypeScript）
- ✅ 登录页面
- ✅ 路由守卫（认证和权限检查）

### 待开发

- ⏳ 驾驶舱页面（统计卡片、地图、图表）
- ⏳ 非遗项目列表和详情页
- ⏳ 传承人列表页
- ⏳ 管理功能页面（CRUD）
- ⏳ 数据导入页面

## API 对接

所有 API 请求通过 `/api/v1` 前缀代理到后端服务（http://127.0.0.1:8000）。

详细的 API 文档请参考：`docs/api-reference.md`

## 认证流程

1. 用户在登录页输入用户名和密码
2. 调用 `/api/v1/auth/login/` 获取 access token 和 refresh token
3. Token 保存在 localStorage 和 Pinia store
4. 后续请求自动在 header 中添加 `Authorization: Bearer <access_token>`
5. Token 过期时自动跳转到登录页

## 权限控制

- **普通用户（user）**: 只能查看数据，无法进行增删改操作
- **管理员（admin）**: 拥有所有权限，可以管理数据和导入数据

路由守卫会自动检查用户权限，未授权访问会被重定向。

## 样式规范

- 使用 Tailwind CSS 工具类进行样式开发
- 主题色：暖色调（橙色系 + 金色 + 青铜色）
- 字体：Inter（正文）+ Playfair Display（标题）
- 遵循 2 空格缩进
- 组件使用 PascalCase 命名

## 注意事项

1. **ECharts 内存泄漏**: 确保在组件卸载时调用 `chart.dispose()`
2. **API 响应格式**: 统一使用 `{ code, message, data, total? }` 格式
3. **错误处理**: 所有 API 调用都应该有适当的错误处理
4. **类型安全**: 充分利用 TypeScript 类型检查

## 测试账号

- 管理员: `admin` / `password123`
- 普通用户: `user` / `password123`
