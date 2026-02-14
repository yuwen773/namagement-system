# 管理端概览统计接口实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 Dashboard 所需的多个接口整合为单一统计接口，一次请求获取全部数据。

**Architecture:** 在 visualization 模块新增 OverviewStatsView，使用 Django ORM 聚合查询一次获取影片数、影院数、累计票房、用户数和最近票房记录。

**Tech Stack:** Django 5.2 + DRF + Vue 3

---

## Task 1: 后端 - 新增 OverviewStatsView

**Files:**
- Modify: `backend/visualization/views.py` - 在文件末尾添加新视图类
- Modify: `backend/visualization/urls.py` - 添加路由

**Step 1: 添加 OverviewStatsView**

在 `backend/visualization/views.py` 文件末尾添加：

```python
class OverviewStatsView(APIView):
    """
    管理端概览统计数据视图

    提供 Dashboard 所需的综合统计数据，包括：
    - 影片总数
    - 影院总数
    - 历史累计票房
    - 注册用户数
    - 最近5条票房记录

    一次请求获取全部数据，优化前端性能。
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取管理端概览统计',
        description=(
            '获取管理端 Dashboard 所需的综合统计数据，包括：'
            '影片总数、影院总数、累计票房、用户总数、最近5条票房记录。'
            '一次请求获取全部数据，避免多次接口调用。'
        ),
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'example': 0},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'total_movies': {'type': 'integer', 'description': '影片总数'},
                            'total_cinemas': {'type': 'integer', 'description': '影院总数'},
                            'total_box_office': {'type': 'number', 'description': '累计票房（元）'},
                            'total_users': {'type': 'integer', 'description': '用户总数'},
                            'recent_records': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'date': {'type': 'string', 'format': 'date'},
                                        'movie_title': {'type': 'string'},
                                        'cinema_name': {'type': 'string'},
                                        'box_office': {'type': 'number'},
                                        'show_times': {'type': 'integer'},
                                        'viewer_count': {'type': 'integer'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        tags=['数据可视化']
    )
    def get(self, request):
        from accounts.models import User

        # 1. 影片总数
        total_movies = Movie.objects.count()

        # 2. 影院总数
        total_cinemas = Cinema.objects.count()

        # 3. 累计票房（后端直接计算，避免传输大量数据）
        total_box_office = BoxOfficeRecord.objects.aggregate(
            total=Coalesce(Sum('daily_box_office'), Value(Decimal('0'), output_field=DecimalField()))
        )['total']

        # 4. 用户总数
        total_users = User.objects.count()

        # 5. 最近5条票房记录
        recent_records = BoxOfficeRecord.objects.select_related(
            'movie', 'cinema'
        ).order_by('-record_date')[:5]

        recent_data = []
        for record in recent_records:
            recent_data.append({
                'id': record.id,
                'date': record.record_date,
                'movie_title': record.movie.title if record.movie else None,
                'cinema_name': record.cinema.name if record.cinema else None,
                'box_office': record.daily_box_office,
                'show_times': record.screening_count,
                'viewer_count': record.audience_count
            })

        return Response({
            'code': 0,
            'data': {
                'total_movies': total_movies,
                'total_cinemas': total_cinemas,
                'total_box_office': total_box_office,
                'total_users': total_users,
                'recent_records': recent_data
            }
        })
```

**Step 2: 添加 URL 路由**

在 `backend/visualization/urls.py` 添加：

```python
from .views import OverviewStatsView

# 在 urlpatterns 中添加
path('stats/overview/', OverviewStatsView.as_view(), name='overview-stats'),
```

**Step 3: 测试接口**

运行开发服务器并测试：
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/visualization/stats/overview/
```

预期返回：
```json
{
  "code": 0,
  "data": {
    "total_movies": 120,
    "total_cinemas": 45,
    "total_box_office": 50000000,
    "total_users": 25,
    "recent_records": [...]
  }
}
```

---

## Task 2: 前端 - 新增 API 函数

**Files:**
- Modify: `frontend/src/api/visualization.js` - 添加 getOverviewStats 函数

**Step 1: 添加 API 函数**

在 `frontend/src/api/visualization.js` 添加：

```javascript
// 获取管理端概览统计数据
export const getOverviewStats = () => {
  return request({
    url: '/visualization/stats/overview/',
    method: 'get'
  })
}
```

---

## Task 3: 前端 - 修改 Dashboard 页面

**Files:**
- Modify: `frontend/src/views/admin/Dashboard.vue` - 修改 loadStats 和 loadRecentRecords 函数

**Step 1: 修改 import 语句**

将：
```javascript
import { getMovies } from '@/api/movie'
import { getCinemas } from '@/api/cinema'
import { getBoxOfficeRecords } from '@/api/boxoffice'
import { getUsers } from '@/api/user'
```

改为：
```javascript
import { getOverviewStats } from '@/api/visualization'
```

**Step 2: 修改 loadStats 函数**

将原来的 loadStats 和 loadRecentRecords 合并为：

```javascript
// 加载统计数据
const loadStats = async () => {
  try {
    loading.value = true
    const res = await getOverviewStats()

    if (res.code === 0) {
      stats.value = {
        movies: res.data.total_movies || 0,
        cinemas: res.data.total_cinemas || 0,
        totalBoxOffice: res.data.total_box_office || 0,
        users: res.data.total_users || 0
      }
      recentRecords.value = res.data.recent_records || []
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}
```

**Step 3: 删除不再需要的 loadRecentRecords 函数调用**

在 onMounted 中，删除 `loadRecentRecords()` 调用，只保留 `loadStats()`。

---

## Task 4: 测试验证

**Step 1: 启动后端服务**

```bash
cd backend
python manage.py runserver
```

**Step 2: 启动前端服务**

```bash
cd frontend
npm run dev
```

**Step 3: 登录管理端账号，访问 Dashboard**

验证：
1. 页面正常显示统计数据
2. 影片总数、影院总数、累计票房、用户数正确
3. 最近票房记录表格显示正确
4. 打开浏览器开发者工具 Network 面板，确认只发起一次 API 请求

---

## 执行方式选择

**Plan complete and saved to `docs/plans/2025-02-13-overview-stats-design.md`.**

Two execution options:

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
