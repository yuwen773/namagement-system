# 系统架构

## 后端结构

```
backend/
├── tourist/            # 项目配置
│   ├── settings.py     # DB/JWT/CORS
│   └── urls.py
├── accounts/           # 账号管理
├── attractions/        # 景点管理
├── comments/           # 评论 + 收藏
├── notifications/      # 消息通知
├── statistics/         # 数据统计
└── recommendations/    # 推荐算法
```

## API 路由

### /api/accounts/
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /register/ | 注册 |
| POST | /login/ | 登录 |
| GET/PUT | /profile/ | 个人信息 |

### /api/attractions/
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 列表 |
| GET | /{id}/ | 详情 |
| GET | /search/ | 搜索 |
| POST | / | 创建* |

### /api/comments/
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | / | 发表评论 |
| GET | /my/ | 我的评论 |
| GET | /attraction/{id}/ | 景点评论 |
| POST | /favorites/ | 添加收藏 |
| GET | /favorites/my/ | 我的收藏 |

### /api/notifications/
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 我的通知 |
| POST | /mark_read/ | 标记已读 |
| POST | /announcement/ | 发布公告* |

### /api/statistics/
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /hot/ | 热门景点 |
| GET | /monthly/ | 月度报告* |
| GET | /dashboard/ | 数据看板* |
| GET | /users/ | 用户列表* |
| PUT | /users/{id}/status/ | 用户状态* |

### /api/recommendations/
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /popular/ | 热门推荐 |
| GET | /personalized/ | 个性化推荐 |
| GET | /similar/{id}/ | 相似景点 |

> * = 需要 ADMIN 角色

## 推荐算法

**热度公式**：`热度 = 浏览量*0.2 + 评论数*0.3 + 平均评分*浏览量*0.5`

| 场景 | 策略 |
|------|------|
| 冷启动 | 热门推荐 |
| 个性化 | 同类景点推荐 |
| 相似推荐 | 类别 + 地区优先 |
