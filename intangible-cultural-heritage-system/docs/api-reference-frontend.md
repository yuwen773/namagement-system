# 前端 API 使用指南

本文档说明前端如何使用封装好的 API 接口。

## 基础配置

所有 API 请求已通过 `src/utils/request.ts` 封装，自动处理：
- 添加 `Authorization: Bearer <token>` header
- 统一响应格式处理
- 错误处理和提示
- 401 自动跳转登录页

## 认证相关 API

### 登录

```typescript
import { login } from '@/api/auth'

const handleLogin = async () => {
  const response = await login({
    username: 'admin',
    password: 'password123'
  })
  
  // response.data.data 包含：
  // - access: JWT access token
  // - refresh: JWT refresh token
  // - user: { id, username, role }
}
```

### 刷新 Token

```typescript
import { refreshToken } from '@/api/auth'

const refresh = async () => {
  const response = await refreshToken('your-refresh-token')
  // response.data.data.access 是新的 access token
}
```

### 登出

```typescript
import { logout } from '@/api/auth'

const handleLogout = async () => {
  await logout('your-refresh-token')
}
```

### 获取当前用户信息

```typescript
import { getCurrentUser } from '@/api/auth'

const fetchUser = async () => {
  const response = await getCurrentUser()
  // response.data.data 包含用户信息
}
```

## 驾驶舱 API

### 获取总览统计

```typescript
import { getOverview } from '@/api/dashboard'

const fetchOverview = async () => {
  const response = await getOverview()
  const data = response.data.data
  // data 包含：
  // - heritage_count: 项目总数
  // - inheritor_count: 传承人总数
  // - category_count: 分类总数
  // - country_count: 国家数
}
```

### 获取地图分布数据

```typescript
import { getMapDistribution } from '@/api/dashboard'

const fetchMapData = async () => {
  // 可选：按类别筛选
  const response = await getMapDistribution({ category: 1 })
  const data = response.data.data
  // data 是数组，每项包含：
  // - country_code, country_name
  // - longitude, latitude
  // - heritage_count, inheritor_count
}
```

### 获取类别占比

```typescript
import { getCategoryDistribution } from '@/api/dashboard'

const fetchCategoryData = async () => {
  const response = await getCategoryDistribution()
  const data = response.data.data
  // data 是数组，每项包含：
  // - category_name
  // - heritage_count
  // - percentage (百分比)
}
```

### 获取国家排行

```typescript
import { getCountryRanking } from '@/api/dashboard'

const fetchRanking = async () => {
  // 可选：指定返回数量（默认 20）
  const response = await getCountryRanking({ limit: 10 })
  const data = response.data.data
  // data 是数组，每项包含：
  // - rank (排名)
  // - country_name
  // - heritage_count
}
```

## 非遗项目 API

### 获取项目列表

```typescript
import { getHeritageList } from '@/api/heritage'

const fetchList = async () => {
  const response = await getHeritageList({
    page: 1,
    category: 1,  // 可选
    level: 'national',  // 可选
    region: 1,  // 可选
    name: '京剧'  // 可选：模糊搜索
  })
  
  const items = response.data.data
  const total = response.data.total
}
```

### 获取项目详情

```typescript
import { getHeritageDetail } from '@/api/heritage'

const fetchDetail = async (id: number) => {
  const response = await getHeritageDetail(id)
  const item = response.data.data
}
```

### 创建项目（需要 admin 权限）

```typescript
import { createHeritage } from '@/api/heritage'

const create = async () => {
  const response = await createHeritage({
    name: '项目名称',
    category: 1,
    level: 'national',
    region: 1,
    area: '地区',  // 可选
    protection_unit: '保护单位',  // 可选
    description: '简介'  // 可选
  })
}
```

### 更新项目（需要 admin 权限）

```typescript
import { updateHeritage } from '@/api/heritage'

const update = async (id: number) => {
  const response = await updateHeritage(id, {
    name: '新名称'
    // 其他字段...
  })
}
```

### 删除项目（需要 admin 权限）

```typescript
import { deleteHeritage } from '@/api/heritage'

const remove = async (id: number) => {
  await deleteHeritage(id)
}
```

## 传承人 API

用法与非遗项目 API 类似，导入自 `@/api/inheritor`：

```typescript
import {
  getInheritorList,
  getInheritorDetail,
  createInheritor,
  updateInheritor,
  deleteInheritor
} from '@/api/inheritor'
```

## 分类 API

```typescript
import {
  getCategoryList,
  getCategoryTree,  // 获取树形结构
  getCategoryDetail,
  createCategory,
  updateCategory,
  deleteCategory
} from '@/api/category'
```

## 地区 API

```typescript
import {
  getRegionList,
  getRegionDetail,
  createRegion,
  updateRegion,
  deleteRegion
} from '@/api/region'
```

## 错误处理

所有 API 调用都应该使用 try-catch 处理错误：

```typescript
try {
  const response = await getHeritageList()
  // 处理成功响应
} catch (error) {
  // 错误已经在拦截器中处理（显示 ElMessage）
  // 这里可以做额外的错误处理
  console.error('Failed to fetch heritage list:', error)
}
```

## 类型定义

所有类型定义在 `src/types/index.ts` 中，使用时导入：

```typescript
import type {
  User,
  HeritageItem,
  Inheritor,
  Category,
  Region,
  DashboardOverview,
  MapPoint,
  CategoryDistribution,
  CountryRanking
} from '@/types'
```

## 状态管理

使用 Pinia 的 user store 管理用户状态：

```typescript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 登录
await userStore.login({ username, password })

// 登出
await userStore.logout()

// 获取用户信息
console.log(userStore.userInfo)
console.log(userStore.isAdmin)
console.log(userStore.isLoggedIn)
```

## 路由守卫

路由守卫已自动配置，无需手动处理：
- 未登录访问受保护路由 → 跳转登录页
- 非管理员访问管理页面 → 跳转首页
- 已登录访问登录页 → 跳转首页
