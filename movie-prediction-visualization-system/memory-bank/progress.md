# 项目进度

## 阶段一：项目初始化 ✅
- Django 5.2 + DRF 后端项目
- MySQL 8.0 数据库 (UTF8MB4)
- Vue 3 + Vite 前端项目

## 阶段二：后端核心功能 ✅
| 模块 | 功能 |
|------|------|
| accounts | JWT认证、用户注册/登录、用户管理 |
| movies | 影片/类型CRUD、搜索筛选 |
| cinemas | 影院/地域CRUD、层级结构 |
| boxoffice | 票房记录管理、批量操作、统计 |
| prediction | 线性回归/移动平均预测算法 |
| visualization | Top10/大盘/类型占比/地域分布/时间走势 |

## 阶段三：前端开发 ⏳

### 3.1 前端基础架构 ✅
- 路由 (21个，含认证守卫)
- Pinia stores (user, app)
- API模块 (7个文件)
- HTTP工具 (Axios封装)
- 布局组件 (Admin/UserLayout)
- 认证页面 (Login/Register)

### 3.2 管理员页面 ✅
| 页面 | 功能 |
|------|------|
| Dashboard | 统计卡片、快捷入口、最近票房 |
| Movies | 影片CRUD、搜索、分页、类型选择 |
| MovieTypes | 类型CRUD、搜索、分页 |
| Cinemas | 影院CRUD、地域筛选、分页 |
| Regions | 地域CRUD、层级结构、分页 |
| BoxOffice | 票房录入/编辑/删除、批量操作 |
| Prediction | 预测配置、ECharts图表、历史记录 |
| Users | 用户CRUD、状态切换、角色管理 |

### 待完成
- 3.3 用户端页面

## 阶段四：系统集成与测试 ⏳
尚未开始

## 阶段五：部署与文档 ⏳
尚未开始
