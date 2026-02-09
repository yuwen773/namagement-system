# 系统架构

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Element Plus + ECharts + Tailwind CSS |
| 后端 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (3307) |
| 爬虫 | TaobaoMtopAPI + Python Threading |

---

## 目录结构

```
backend/
├── tmall_project/       # Django 配置 (settings.py, urls.py)
├── users/               # 用户认证 (models.py, views.py, serializers.py)
├── products/            # 商品管理 (models.py, views.py, serializers.py)
├── crawler/             # 爬虫模块
│   ├── services.py      # 爬虫服务层
│   ├── views.py         # API 视图
│   ├── serializers.py   # 序列化器
│   └── spiders/         # 爬虫实现 (taobao_mtop_api.py)
└── manage.py

frontend/
├── src/
│   ├── api/             # API 封装 (authApi, productApi, crawlerApi, statisticsApi)
│   ├── components/
│   │   ├── Layout/      # AdminLayout.vue, UserLayout.vue
│   │   └── common/      # Pagination.vue, DataTable.vue, ChartContainer.vue
│   ├── views/           # Login.vue, admin/*, user/*
│   ├── router/          # 路由配置 + 守卫
│   ├── stores/          # Pinia user store
│   ├── utils/           # Axios 拦截器
│   └── main.js
├── vite.config.js       # 路径别名 @, API 代理
└── tailwind.config.js
```

---

## 数据模型

### User
```
id: UUID | username: string | password: bcrypt
role: admin/user | status: active/frozen
```

### Product
```
id: UUID | title, price, sales, shop
image_url, detail_url | brand, category
batch_no, crawl_time
```

### CrawlLog
```
id: UUID | task_id: string | status: pending/running/success/failed/cancelled
mode: demo/batch | source_type: mtop_api/real_api/json/playwright
items_collected/success/failed
start_time, end_time, log_content, error_message
```

### PriceHistory
```
id: UUID | product: FK(Product) | price, sales | record_date
```

---

## 爬虫架构

### 执行流程
```
前端请求 → Django API → CrawlerService.start_crawl()
                            ↓
                       创建 CrawlLog (running)
                            ↓
                       启动后台线程
                            ↓
                  TaobaoMtopAPI.search()
                            ↓
                    保存数据到 Product
                            ↓
                  更新 CrawlLog (success/failed)
```

### 状态查询
```
前端轮询 → Django API → CrawlerService.get_status()
                            ↓
                  查询 CrawlLog 表
                            ↓
              返回 {status, items_collected, ...}
```

---

## 路由与权限

```
/login         → 公开
/admin/*       → admin 角色
/user/*        → user 角色

守卫逻辑：无 Token → /login | 角色不匹配 → 对应首页
```

---

## API 响应格式

```json
{ "code": 0, "data": {...}, "total": n }   // 成功
{ "code": -1, "message": "错误" }         // 失败
```

---

## 环境配置

| 配置项 | 值 |
|--------|-----|
| 后端端口 | 8000 |
| 前端端口 | 5173 |
| MySQL | 3307, 密码 yuwen123 |
| JWT Token | 2h (access) / 7d (refresh) |

---

## 部署要求

### 运行服务
- **必需**: Django 服务 (`python manage.py runserver`)
- **可选**: 无需额外服务

### 启动命令
```bash
# 后端
cd backend
python manage.py runserver

# 前端
cd frontend
npm run dev
```

---

最后更新: 2026-02-08
