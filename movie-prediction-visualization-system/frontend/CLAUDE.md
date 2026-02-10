# 前端开发指南

## 项目结构

```
frontend/
├── src/
│   ├── api/                    # API 接口封装
│   │   ├── auth.js             # 认证相关接口
│   │   ├── movie.js            # 影片相关接口
│   │   ├── cinema.js           # 影院相关接口
│   │   ├── boxoffice.js        # 票房相关接口
│   │   ├── visualization.js    # 可视化相关接口
│   │   ├── prediction.js       # 预测相关接口
│   │   └── user.js             # 用户相关接口
│   ├── assets/                 # 静态资源
│   ├── components/             # 公共组件
│   │   └── HelloWorld.vue
│   ├── constants/              # 常量定义
│   │   └── index.js
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── stores/                 # Pinia 状态管理
│   │   ├── app.js              # 应用状态
│   │   └── user.js             # 用户状态
│   ├── utils/                  # 工具函数
│   │   └── request.js          # Axios 封装
│   ├── views/                  # 页面视图
│   │   ├── layouts/            # 布局组件
│   │   │   ├── AdminLayout.vue
│   │   │   └── UserLayout.vue
│   │   ├── auth/               # 认证页面
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── admin/              # 管理端页面
│   │   │   ├── Dashboard.vue
│   │   │   ├── Movies.vue
│   │   │   ├── MovieTypes.vue
│   │   │   ├── Cinemas.vue
│   │   │   ├── Regions.vue
│   │   │   ├── BoxOffice.vue
│   │   │   ├── Prediction.vue
│   │   │   └── Users.vue
│   │   ├── user/               # 用户端页面
│   │   │   ├── Dashboard.vue
│   │   │   ├── BoxOffice.vue
│   │   │   ├── Visualization.vue
│   │   │   ├── Prediction.vue
│   │   │   └── Profile.vue
│   │   └── NotFound.vue
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 开发规范

### 组件命名
- 页面组件：PascalCase（如 `Dashboard.vue`）
- 公共组件：PascalCase（如 `ChartCard.vue`）

### API 响应处理
```javascript
// 成功
{ code: 0, data: {...}, total: n }

// 错误
{ code: -1, message: "错误描述" }
```

### ECharts 使用
```javascript
// 初始化
const chart = echarts.init(dom)

// 设置选项
chart.setOption(option)

// 销毁（防止内存泄漏）
onUnmounted(() => {
  chart.dispose()
})
```

### 路由配置
- `meta.requiresAuth`: 是否需要登录
- `meta.roles`: 允许访问的角色 ['admin', 'user']

## 常用命令

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 页面路径

| 路径 | 说明 |
|------|------|
| `/login` | 登录页 |
| `/register` | 注册页 |
| `/admin/dashboard` | 管理端首页 |
| `/admin/movies` | 影片管理 |
| `/admin/cinemas` | 影院管理 |
| `/admin/boxoffice` | 票房录入 |
| `/admin/prediction` | 预测分析 |
| `/admin/users` | 用户管理 |
| `/user/dashboard` | 用户端首页 |
| `/user/boxoffice` | 票房查询 |
| `/user/visualization` | 可视化图表 |
| `/user/prediction` | 未来预测 |
| `/user/profile` | 个人中心 |
