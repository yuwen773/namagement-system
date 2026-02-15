# 前端项目结构说明

## 技术栈

- **构建工具**: Vite 6.x
- **框架**: Vue 3.5 (Composition API)
- **路由**: Vue Router 4.x
- **状态管理**: Pinia 2.x
- **UI 组件库**: Element Plus 2.x
- **图表库**: ECharts 5.x
- **HTTP 客户端**: Axios 1.x
- **样式**: Tailwind CSS 3.x

## 项目结构

```
frontend/
├── src/
│   ├── api/                # API 接口模块
│   │   ├── auth.js         # 认证相关接口
│   │   ├── airquality.js   # 空气质量数据接口
│   │   └── admin.js        # 管理端接口
│   ├── assets/             # 静态资源
│   ├── components/         # 公共组件（待开发）
│   ├── layouts/            # 布局组件
│   │   ├── UserLayout.vue  # 用户端布局
│   │   └── AdminLayout.vue # 管理端布局
│   ├── router/             # 路由配置
│   │   └── index.js        # 路由定义与导航守卫
│   ├── stores/             # Pinia 状态管理
│   │   ├── user.js         # 用户状态
│   │   ├── city.js         # 城市选择状态
│   │   └── admin.js        # 管理端状态
│   ├── utils/              # 工具函数
│   │   └── request.js      # Axios 封装（拦截器、错误处理）
│   ├── views/              # 页面组件
│   │   ├── auth/           # 认证页面
│   │   │   ├── Login.vue   # 登录页
│   │   │   └── Register.vue # 注册页
│   │   ├── user/           # 用户端页面
│   │   │   ├── Overview.vue        # 全国概览
│   │   │   ├── CityDetail.vue      # 城市详情
│   │   │   ├── StationDetail.vue   # 站点详情
│   │   │   ├── HistoricalData.vue  # 历史数据
│   │   │   ├── Analysis.vue        # 数据分析
│   │   │   ├── ProtectionGuide.vue # 防护指南
│   │   │   ├── KnowledgeBase.vue   # 科普知识
│   │   │   └── ArticleDetail.vue   # 文章详情
│   │   └── admin/          # 管理端页面
│   │       ├── Dashboard.vue       # 仪表盘
│   │       ├── DataImport.vue      # 数据导入
│   │       ├── AirQualityManage.vue # 数据管理
│   │       ├── RulesManage.vue     # 规则管理
│   │       ├── UsersManage.vue     # 用户管理
│   │       ├── ArticlesManage.vue  # 文章管理
│   │       └── SystemLogs.vue      # 系统日志
│   ├── App.vue             # 根组件
│   ├── main.js             # 入口文件
│   └── style.css           # 全局样式
├── index.html              # HTML 模板
├── vite.config.js          # Vite 配置
├── tailwind.config.js      # Tailwind CSS 配置
├── postcss.config.js       # PostCSS 配置
├── package.json            # 依赖清单
└── .gitignore              # Git 忽略规则
```

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器（默认端口 5173）
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 配置说明

### API 代理配置

开发环境下，`/api` 路径会被代理到后端服务器（http://127.0.0.1:8000），配置在 `vite.config.js`：

```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true
    }
  }
}
```

### Element Plus 按需引入

使用 `unplugin-vue-components` 和 `unplugin-auto-import` 实现自动按需引入组件和 API。

### 路由说明

- 用户端路由：`/` 为前缀，使用 `UserLayout` 布局
- 管理端路由：`/admin` 为前缀，使用 `AdminLayout` 布局，需要管理员权限
- 认证路由：`/login`、`/register`

### 状态管理说明

- `userStore`：管理用户登录状态、用户信息、token
- `cityStore`：管理用户选择的城市和站点
- `adminStore`：管理管理端 UI 状态（菜单展开/收起、当前激活菜单）

### API 请求说明

所有 API 请求通过 `utils/request.js` 封装的 Axios 实例发起：
- 自动添加 token 到请求头
- 统一处理错误响应
- 401 自动跳转登录页

## 下一步开发

阶段二第 2.2 步：路由与状态管理（已完成基础配置）
阶段二第 2.3 步：公共组件开发（待开发）
- ECharts 通用组件
- 数据表格组件
