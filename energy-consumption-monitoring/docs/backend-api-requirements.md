# 后端 API 需求文档

本文档描述了前端页面需要但后端尚未实现的 API 接口。

## 📋 目录

1. [费率管理 API](#1-费率管理-api) - `frontend/src/views/admin/Configuration.vue`
2. [用户余额 API](#2-用户余额-api) - `frontend/src/views/user/CostPayment.vue`
3. [排名与对比 API](#3-排名与对比-api) - `frontend/src/views/user/Comparison.vue`
4. [节能知识 API](#4-节能知识-api) - `frontend/src/views/user/Notices.vue`
5. [成就系统 API](#5-成就系统-api) - `frontend/src/views/user/Comparison.vue`

---

## 1. 费率管理 API

### 🎯 前端页面
- **页面路径**: `frontend/src/views/admin/Configuration.vue`
- **使用位置**: 费率设置模块
- **当前状态**: 使用硬编码静态数据

```javascript
// 当前代码位置：frontend/src/views/admin/Configuration.vue:477-489
const electricityRates = ref({
  peak: 1.2,
  flat: 0.8,
  valley: 0.4,
})

const waterTiers = ref([
  { name: '第一阶梯', range: '0-15m³', rate: 3.5 },
  { name: '第二阶梯', range: '15-25m³', rate: 4.5 },
  { name: '第三阶梯', range: '25m³以上', rate: 5.5 },
])

const gasRate = ref(2.8)
```

### 1.1 电价管理

#### 获取电价配置
```
GET /api/rates/electricity/
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "peak_rate": 1.2,
    "flat_rate": 0.8,
    "valley_rate": 0.4,
    "peak_hours": "08:00-12:00,18:00-22:00",
    "flat_hours": "12:00-18:00",
    "valley_hours": "22:00-08:00",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 更新电价配置（管理员）
```
PUT /api/rates/electricity/
```

**请求体：**
```json
{
  "peak_rate": 1.2,
  "flat_rate": 0.8,
  "valley_rate": 0.4
}
```

### 1.2 水价管理

#### 获取水价配置
```
GET /api/rates/water/
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "tiers": [
      {
        "tier": 1,
        "name": "第一阶梯",
        "min_consumption": 0,
        "max_consumption": 15,
        "rate": 3.5,
        "unit": "元/m³"
      },
      {
        "tier": 2,
        "name": "第二阶梯",
        "min_consumption": 15,
        "max_consumption": 25,
        "rate": 4.5,
        "unit": "元/m³"
      },
      {
        "tier": 3,
        "name": "第三阶梯",
        "min_consumption": 25,
        "max_consumption": null,
        "rate": 5.5,
        "unit": "元/m³"
      }
    ],
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 更新水价配置（管理员）
```
PUT /api/rates/water/
```

### 1.3 气价管理

#### 获取气价配置
```
GET /api/rates/gas/
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "rate": 2.8,
    "unit": "元/m³",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 2. 用户余额 API

### 🎯 前端页面
- **页面路径**: `frontend/src/views/user/CostPayment.vue`
- **使用位置**: 费用支付页面顶部余额卡片
- **当前状态**: 使用硬编码静态数据 `balance = ref('358.60')`

```vue
<!-- 当前代码位置：frontend/src/views/user/CostPayment.vue:13-18 -->
<div class="balance-card">
  <div class="balance-label">账户余额</div>
  <div class="balance-value">
    <span class="balance-currency">¥</span>
    <span class="balance-amount">{{ balance }}</span>
  </div>
</div>
```

### 2.1 数据模型变更

需要在 `backend/apps/accounts/models.py` 的 `UserProfile` 模型中添加余额字段：

```python
class UserProfile(models.Model):
    # ... 现有字段 ...

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="账户余额"
    )
    total_recharged = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="累计充值"
    )
    reward_points = models.IntegerField(
        default=0,
        verbose_name="节能积分"
    )
```

### 2.2 API 端点

#### 获取用户余额
```
GET /api/profile/balance/
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "balance": "358.60",
    "total_recharged": "1200.00",
    "reward_points": 250,
    "currency": "CNY"
  }
}
```

#### 充值（扩展现有接口）
```
POST /api/recharges/simulate/
```

**请求体：**
```json
{
  "room_id": 123,
  "amount": 100.00,
  "payment_method": "wechat"
}
```

**响应需包含：**
```json
{
  "code": 0,
  "data": {
    "recharge_id": 456,
    "amount": "100.00",
    "balance_after": "458.60",
    "status": "success",
    "transaction_id": "TXN20240115123456"
  }
}
```

### 2.3 前端调用示例

```javascript
// 需要在 frontend/src/api/profile.js 中添加
export function getMyBalance() {
  return request({
    url: '/profile/balance/',
    method: 'get',
  })
}

// 在 CostPayment.vue 中使用
import { getMyBalance } from '@/api/profile'

async function loadBalance() {
  const response = await getMyBalance()
  if (response.code === 0) {
    balance.value = response.data.balance
  }
}
```

---

## 3. 排名与对比 API

### 🎯 前端页面
- **页面路径**: `frontend/src/views/user/Comparison.vue`
- **使用位置**:
  - `myRank`, `rankTrend` - 我的排名和趋势
  - `comparisonStats` - 对比统计数据（vs全校平均、节能指数、碳排放）

```javascript
// 当前代码位置：frontend/src/views/user/Comparison.vue:229-260
const myRank = ref(15)           // 需要从 API 获取
const rankTrend = ref(3)         // 需要从 API 获取

const comparisonStats = ref([
  {
    label: 'vs 全校平均',
    value: '-18%',
    icon: 'icon-ep-trend-charts',
    color: '#22c55e',
    indicator: '优于平均',
    indicatorClass: 'good',
  },
  // ... 更多统计项
])
```

### 3.1 获取我的排名

#### 获取当前用户排名
```
GET /api/analysis/my-ranking/
```

**查询参数：**
- `period`: `week` | `month` | `year`（默认：week）
- `type`: `building` | `room` | `department`（默认：room）

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "current_rank": 15,
    "total_count": 120,
    "rank_trend": 3,
    "rank_change": "上升 3 位",
    "my_consumption": {
      "electricity": 125.5,
      "water": 8.2,
      "gas": 3.1,
      "total": 136.8
    },
    "average_consumption": {
      "electricity": 150.0,
      "water": 10.0,
      "gas": 4.0,
      "total": 164.0
    },
    "vs_average": "-18%"
  }
}
```

### 3.2 对比统计数据

#### 获取对比分析数据
```
GET /api/analysis/comparison-stats/
```

**查询参数：**
- `period`: `week` | `month` | `year`

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "vs_school_average": {
      "value": "-18%",
      "status": "better",
      "description": "优于平均"
    },
    "efficiency_score": {
      "value": 82,
      "max_value": 100,
      "level": "良好"
    },
    "carbon_emission": {
      "value": -12,
      "unit": "kg",
      "description": "减少排放"
    },
    "saving_amount": {
      "value": 28.50,
      "currency": "CNY",
      "description": "节省费用"
    }
  }
}
```

### 3.3 前端调用示例

```javascript
// 需要在 frontend/src/api/analysis.js 中添加
export function getMyRanking(params) {
  return request({
    url: '/analysis/my-ranking/',
    method: 'get',
    params,
  })
}

export function getComparisonStats(params) {
  return request({
    url: '/analysis/comparison-stats/',
    method: 'get',
    params,
  })
}

// 在 Comparison.vue 中使用
async function loadRankingData() {
  const response = await getMyRanking({
    period: rankingType.value,
    type: 'room'
  })
  if (response.code === 0) {
    myRank.value = response.data.current_rank
    rankTrend.value = response.data.rank_trend
  }
}

async function loadComparisonStats() {
  const response = await getComparisonStats({
    period: activePeriod.value
  })
  if (response.code === 0) {
    // 更新 comparisonStats
  }
}
```

---

## 4. 节能知识 API

### 🎯 前端页面
- **页面路径**: `frontend/src/views/user/Notices.vue`
- **使用位置**: 节能小贴士模块（公告下方）
- **当前状态**: 使用硬编码静态数据，注释说明 "could come from API"

```javascript
// 当前代码位置：frontend/src/views/user/Notices.vue:216-257
const tips = ref([
  {
    title: '随手关灯，每月省电10度',
    content: '离开房间时记得关闭不必要的灯具...',
    category: 'electricity',
  },
  // ... 更多贴士
])
```

### 4.1 数据模型

需要创建节能知识模型：

```python
class EnergyTip(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    category = models.CharField(
        max_length=20,
        choices=[('electricity', '节电'), ('water', '节水'),
                 ('gas', '节气'), ('daily', '日常')],
        verbose_name="分类"
    )
    icon = models.CharField(max_length=50, blank=True, verbose_name="图标")
    priority = models.IntegerField(default=0, verbose_name="优先级")
    is_published = models.BooleanField(default=True, verbose_name="是否发布")
    view_count = models.IntegerField(default=0, verbose_name="浏览次数")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 4.2 API 端点

#### 获取节能知识列表
```
GET /api/tips/
```

**查询参数：**
- `category`: `electricity` | `water` | `gas` | `daily`（可选）
- `limit`: 返回数量（默认：10）
- `random`: 是否随机返回（默认：false）

**响应示例：**
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "title": "随手关灯，每月省电10度",
      "content": "离开房间时记得关闭不必要的灯具...",
      "category": "electricity",
      "icon": "⚡",
      "created_at": "2024-01-10T10:00:00Z"
    }
  ],
  "total": 25
}
```

#### 获取单条节能知识
```
GET /api/tips/{id}/
```

#### 创建节能知识（管理员）
```
POST /api/admin/tips/
```

#### 更新节能知识（管理员）
```
PUT /api/admin/tips/{id}/
```

#### 删除节能知识（管理员）
```
DELETE /api/admin/tips/{id}/
```

### 4.3 前端调用示例

```javascript
// 需要在 frontend/src/api/ 创建 tips.js
export function getTips(params) {
  return request({
    url: '/tips/',
    method: 'get',
    params,
  })
}

// 在 Notices.vue 中使用
import { getTips } from '@/api/tips'

async function loadTips() {
  const response = await getTips({
    limit: 10,
    random: true
  })
  if (response.code === 0) {
    tips.value = response.data
  }
}
```

---

## 5. 成就系统 API

### 🎯 前端页面
- **页面路径**: `frontend/src/views/user/Comparison.vue`
- **使用位置**: 成就徽章展示区域
- **当前状态**: 使用硬编码静态数据

```javascript
// 当前代码位置：frontend/src/views/user/Comparison.vue:266-273
const achievements = ref([
  { id: 1, name: '节能先锋', desc: '连续7天低于平均', icon: '🌟', unlocked: true },
  { id: 2, name: '节水达人', desc: '用水量低于平均30%', icon: '💧', unlocked: true },
  { id: 3, name: '低碳生活', desc: '碳排放减少50kg', icon: '🌿', unlocked: true },
  { id: 4, name: '月度冠军', desc: '月度排名前10', icon: '🏆', unlocked: false },
  { id: 5, name: '百日坚持', desc: '连续100天记录', icon: '🔥', unlocked: false },
  { id: 6, name: '能源管家', desc: '绑定3个房间', icon: '🏠', unlocked: true },
])
```

### 5.1 数据模型

需要创建成就系统模型：

```python
class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="成就代码")
    name = models.CharField(max_length=100, verbose_name="成就名称")
    description = models.TextField(verbose_name="成就描述")
    icon = models.CharField(max_length=50, verbose_name="图标")
    category = models.CharField(
        max_length=20,
        choices=[('saving', '节能'), ('streak', '坚持'),
                 ('ranking', '排名'), ('special', '特殊')],
        verbose_name="成就类别"
    )
    condition_type = models.CharField(
        max_length=20,
        choices=[('consumption', '用量'), ('days', '天数'),
                 ('rank', '排名'), ('rooms', '房间数')],
        verbose_name="条件类型"
    )
    condition_value = models.JSONField(verbose_name="条件值")
    points = models.IntegerField(default=0, verbose_name="积分奖励")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True)

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    progress = models.JSONField(default=dict, verbose_name="进度")

    class Meta:
        unique_together = ['user', 'achievement']
```

### 5.2 API 端点

#### 获取我的成就列表
```
GET /api/achievements/my/
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "unlocked": [
      {
        "id": 1,
        "code": "energy_pioneer",
        "name": "节能先锋",
        "description": "连续7天低于平均",
        "icon": "🌟",
        "category": "saving",
        "points": 50,
        "unlocked_at": "2024-01-10T15:30:00Z"
      }
    ],
    "locked": [
      {
        "id": 4,
        "code": "monthly_champion",
        "name": "月度冠军",
        "description": "月度排名前10",
        "icon": "🏆",
        "category": "ranking",
        "points": 100,
        "progress": {
          "current": 15,
          "target": 10,
          "percentage": 67
        }
      }
    ],
    "summary": {
      "total": 6,
      "unlocked_count": 3,
      "total_points": 150
    }
  }
}
```

#### 获取成就排行榜
```
GET /api/achievements/leaderboard/
```

**查询参数：**
- `limit`: 返回数量（默认：20）

**响应示例：**
```json
{
  "code": 0,
  "data": [
    {
      "user_id": 123,
      "username": "user001",
      "achievement_count": 5,
      "total_points": 280,
      "rank": 1
    }
  ]
}
```

#### 获取所有成就定义
```
GET /api/achievements/
```

#### 解锁成就进度检查
```
POST /api/achievements/check-progress/
```

### 5.3 前端调用示例

```javascript
// 需要在 frontend/src/api/ 创建 achievement.js
export function getMyAchievements() {
  return request({
    url: '/achievements/my/',
    method: 'get',
  })
}

export function getAchievementLeaderboard(params) {
  return request({
    url: '/achievements/leaderboard/',
    method: 'get',
    params,
  })
}

// 在 Comparison.vue 中使用
import { getMyAchievements } from '@/api/achievement'

async function loadAchievements() {
  const response = await getMyAchievements()
  if (response.code === 0) {
    achievements.value = [
      ...response.data.unlocked.map(a => ({ ...a, unlocked: true })),
      ...response.data.locked.map(a => ({ ...a, unlocked: false }))
    ]
  }
}
```

---

## 6. 建议的文件结构

```
backend/apps/
├── rates/                    # 新增：费率管理应用
│   ├── __init__.py
│   ├── models.py             # ElectricityRate, WaterRate, GasRate
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── achievements/             # 新增：成就系统应用
│   ├── __init__.py
│   ├── models.py             # Achievement, UserAchievement
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── tips/                     # 新增：节能知识应用
│   ├── __init__.py
│   ├── models.py             # EnergyTip
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── accounts/
    └── models.py             # 修改：UserProfile 添加 balance 等字段

frontend/src/api/
├── rate.js                   # 新增：费率管理 API
├── achievement.js            # 新增：成就系统 API
└── tips.js                   # 新增：节能知识 API
```

---

## 7. 前端页面与 API 对应关系总览

| API 模块 | 前端页面 | 文件路径 | 优先级 |
|---------|---------|----------|--------|
| 费率管理 | Configuration.vue | `frontend/src/views/admin/Configuration.vue` | 中 |
| 用户余额 | CostPayment.vue | `frontend/src/views/user/CostPayment.vue` | 高 |
| 排名与对比 | Comparison.vue | `frontend/src/views/user/Comparison.vue` | 高 |
| 节能知识 | Notices.vue | `frontend/src/views/user/Notices.vue` | 低 |
| 成就系统 | Comparison.vue | `frontend/src/views/user/Comparison.vue` | 低 |

---

## 8. 优先级建议

| 优先级 | API | 使用页面 | 说明 |
|--------|-----|---------|------|
| **高** | 用户余额 API | CostPayment.vue | 页面核心功能，硬编码余额 |
| **高** | 排名与对比 API | Comparison.vue | 页面核心功能，硬编码排名数据 |
| **中** | 费率管理 API | Configuration.vue | 管理功能，硬编码费率数据 |
| **低** | 节能知识 API | Notices.vue | 可先使用静态数据 |
| **低** | 成就系统 API | Comparison.vue | 增强用户互动功能 |

---

## 9. 注意事项

1. **响应格式统一**：所有 API 应遵循现有的响应格式 `{ code: 0, data: {...}, message: "" }`

2. **权限控制**：
   - 费率管理、节能知识管理需要 ADMIN 权限
   - 用户余额、成就数据需要用户本人或 ADMIN 权限

3. **数据验证**：
   - 余额变更需要记录操作日志
   - 充值接口需要幂等性处理

4. **数据库迁移**：
   - UserProfile 添加字段需要创建迁移文件
   - 新增应用需要运行 `makemigrations` 和 `migrate`

5. **前端兼容**：
   - 新增 API 需要在 `frontend/src/api/` 下创建对应的 API 文件
   - 前端需要处理 API 调用失败的情况，保留降级方案
