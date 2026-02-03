# 前端接口对接开发规范

> 前端与后端 API 对接开发规范文档
> 版本：v1.0
> 更新日期：2026-02-03

---

## 目录

1. [项目结构规范](#1-项目结构规范)
2. [API 请求封装规范](#2-api-请求封装规范)
3. [响应数据处理规范](#3-响应数据处理规范)
4. [错误处理规范](#4-错误处理规范)
5. [认证与授权规范](#5-认证与授权规范)
6. [分页处理规范](#6-分页处理规范)
7. [文件上传规范](#7-文件上传规范)
8. [数据转换规范](#8-数据转换规范)
9. [代码风格规范](#9-代码风格规范)
10. [测试规范](#10-测试规范)

---

## 1. 项目结构规范

### 1.1 目录结构

```
frontend/
├── src/
│   ├── api/                    # API 接口目录
│   │   ├── index.ts            # API 统一导出
│   │   ├── modules/            # 按模块拆分
│   │   │   ├── user.ts         # 用户相关接口
│   │   │   ├── product.ts      # 商品相关接口
│   │   │   └── order.ts        # 订单相关接口
│   │   ├── request.ts          # Axios 请求封装
│   │   └── types.ts            # TypeScript 类型定义
│   ├── components/             # 公共组件
│   ├── views/                  # 页面组件
│   ├── stores/                 # 状态管理
│   │   └── auth.ts             # 认证状态
│   ├── utils/                  # 工具函数
│   │   ├── index.ts
│   │   ├── format.ts           # 格式化工具
│   │   └── constants.ts        # 常量定义
│   └── styles/                 # 样式文件
├── types/                      # 全局类型定义
└── package.json
```

### 1.2 文件命名规范

| 文件类型 | 命名规范 | 示例 |
|---------|---------|------|
| API 模块 | 小写 + 连字符 | `user-api.ts` |
| 类型定义 | 大驼峰 + `.d.ts` | `User.d.ts` |
| 工具函数 | 小写下划线 | `format-date.ts` |
| 组件文件 | 大驼峰 | `UserCard.vue` |
| 视图文件 | 大驼峰 + View | `UserListView.vue` |

### 1.3 API 目录结构示例

```
api/
├── index.ts                    # 统一导出
├── request.ts                  # 请求封装
├── types.ts                    # 通用类型
└── modules/
    ├── auth.ts                 # 认证接口
    ├── user.ts                 # 用户接口
    ├── product.ts              # 商品接口
    ├── order.ts                # 订单接口
    └── common.ts               # 公共接口
```

---

## 2. API 请求封装规范

### 2.1 Axios 实例封装

**创建 `api/request.ts`：**

```typescript
import axios, { AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加 Token
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error: Error) => {
    console.error('请求配置错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { code, message, data } = response.data

    // 业务成功
    if (code === 200 || code === 201) {
      return data
    }

    // 业务错误
    ElMessage.error(message || '请求失败')
    return Promise.reject(new BusinessError(message, code))
  },
  (error: any) => {
    // HTTP 错误处理
    const status = error.response?.status

    switch (status) {
      case 401:
        // Token 过期或无效
        ElMessage.error('登录已过期，请重新登录')
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
        break
      case 403:
        ElMessage.error('没有权限访问')
        break
      case 404:
        ElMessage.error('请求的资源不存在')
        break
      case 500:
        ElMessage.error('服务器错误，请稍后重试')
        break
      default:
        ElMessage.error(error.message || '网络错误')
    }

    return Promise.reject(error)
  }
)

export default request

// 自定义业务错误类
export class BusinessError extends Error {
  code: number

  constructor(message: string, code: number = 400) {
    super(message)
    this.name = 'BusinessError'
    this.code = code
  }
}
```

### 2.2 请求方法封装

**创建 `api/index.ts`：**

```typescript
import request from './request'

/**
 * GET 请求
 */
export function get<T = any>(
  url: string,
  params?: object,
  config?: AxiosRequestConfig
): Promise<T> {
  return request.get(url, { params, ...config })
}

/**
 * POST 请求
 */
export function post<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig
): Promise<T> {
  return request.post(url, data, config)
}

/**
 * PUT 请求
 */
export function put<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig
): Promise<T> {
  return request.put(url, data, config)
}

/**
 * PATCH 请求
 */
export function patch<T = any>(
  url: string,
  data?: object,
  config?: AxiosRequestConfig
): Promise<T> {
  return request.patch(url, data, config)
}

/**
 * DELETE 请求
 */
export function del<T = any>(
  url: string,
  params?: object,
  config?: AxiosRequestConfig
): Promise<T> {
  return request.delete(url, { params, ...config })
}

/**
 * 上传文件
 */
export function upload<T = any>(
  url: string,
  formData: FormData,
  onProgress?: (event: any) => void
): Promise<T> {
  return request.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: onProgress
  })
}
```

### 2.3 请求方法类型定义

```typescript
// 通用响应结构
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应结构
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// 请求配置扩展
export interface RequestConfig extends AxiosRequestConfig {
  /** 是否显示错误提示 */
  showError?: boolean
  /** 是否显示成功提示 */
  showSuccess?: boolean
}

// API 错误结构
export interface ApiError {
  code: number
  message: string
  errors?: Record<string, string[]>
}
```

---

## 3. 响应数据处理规范

### 3.1 统一响应结构解析

后端返回的统一响应格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

前端处理方式：

```typescript
// request.ts 中的响应拦截器已自动解析 data
// 业务代码直接获取 data 数据

// 成功时返回 data
const user = await get<User>('/api/users/1')
// user 就是后端 data 中的数据

// 分页数据
interface UserListResponse {
  count: number
  next: string | null
  previous: string | null
  results: User[]
}
const userList = await get<UserListResponse>('/api/users/')
```

### 3.2 状态码对应处理

| 后端 code | HTTP Status | 处理方式 | 用户提示 |
|-----------|-------------|---------|---------|
| 200 | 200 | 成功 | "操作成功" |
| 201 | 201 | 创建成功 | "创建成功" |
| 400 | 400 | 参数错误 | 显示后端 message |
| 401 | 401 | 未登录/Token过期 | "登录已过期" |
| 403 | 403 | 无权限 | "没有权限访问" |
| 404 | 404 | 资源不存在 | "请求的资源不存在" |
| 500 | 500 | 服务器错误 | "服务器错误" |

### 3.3 响应数据处理示例

```typescript
// 用户详情接口
export function getUserDetail(id: number): Promise<UserDetail> {
  return get(`/api/users/${id}/`)
}

// 商品列表接口
export function getProductList(params: ProductListParams): Promise<PaginatedResponse<Product>> {
  return get('/api/products/products/', params)
}

// 创建订单接口
export function createOrder(data: CreateOrderData): Promise<Order> {
  return post('/api/orders/orders/', data)
}
```

---

## 4. 错误处理规范

### 4.1 错误类型定义

```typescript
// 错误类型
export enum ErrorType {
  NETWORK = 'NETWORK',
  TIMEOUT = 'TIMEOUT',
  BUSINESS = 'BUSINESS',
  AUTH = 'AUTH',
  VALIDATION = 'VALIDATION'
}

// 统一错误接口
export interface AppError {
  type: ErrorType
  message: string
  code?: number
  details?: Record<string, string[]>
}
```

### 4.2 全局错误处理

```typescript
// utils/error-handler.ts

import { ElMessage, ElNotification } from 'element-plus'

interface ErrorHandlerOptions {
  /** 是否显示错误消息 */
  showMessage?: boolean
  /** 是否记录日志 */
  logError?: boolean
}

/**
 * 处理业务错误
 */
export function handleBusinessError(
  error: any,
  options: ErrorHandlerOptions = {}
): void {
  const { showMessage = true, logError = true } = options

  if (logError) {
    console.error('业务错误:', error)
  }

  if (showMessage && error.message) {
    ElMessage.error(error.message)
  }
}

/**
 * 处理网络错误
 */
export function handleNetworkError(error: any): void {
  console.error('网络错误:', error)
  ElMessage.error('网络连接失败，请检查网络')
}

/**
 * 处理验证错误
 */
export function handleValidationError(details: Record<string, string[]>): void {
  const firstError = Object.values(details)[0]?.[0]
  if (firstError) {
    ElMessage.error(firstError)
  }
}
```

### 4.3 Try-Catch 最佳实践

```typescript
// 推荐写法
async function fetchUserList() {
  try {
    loading.value = true
    const data = await getUserList(params)
    tableData.value = data.results
    total.value = data.count
  } catch (error) {
    handleBusinessError(error)
  } finally {
    loading.value = false
  }
}

// 带确认的错误处理
async function deleteItem(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteItemApi(id)
    ElMessage.success('删除成功')
    await fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      handleBusinessError(error)
    }
  }
}
```

---

## 5. 认证与授权规范

### 5.1 Token 管理

```typescript
// stores/auth.ts
import { defineStore } from 'pinia'
import request from '@/api/request'

interface User {
  id: number
  nickname: string
  avatar: string
  phone: string
}

interface AuthState {
  token: string | null
  user: User | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userInfo: (state) => state.user
  },

  actions: {
    async login(username: string, password: string): Promise<void> {
      const data = await post<{ token: string; user: User }>('/api/auth/login/', {
        username,
        password
      })

      this.token = data.token
      this.user = data.user
      localStorage.setItem('token', data.token)
    },

    async getCurrentUser(): Promise<void> {
      if (!this.token) return

      try {
        const data = await get<User>('/api/auth/me/')
        this.user = data
      } catch {
        this.logout()
      }
    },

    logout(): void {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
```

### 5.2 路由守卫

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 导航守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 需要登录的路由
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // 检查本地是否有 Token
      const token = localStorage.getItem('token')
      if (token) {
        // 尝试获取用户信息
        authStore.token = token
        await authStore.getCurrentUser()

        if (authStore.isAuthenticated) {
          next()
          return
        }
      }

      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
  }

  // 已登录访问登录页
  if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
```

### 5.3 权限指令

```typescript
// directives/v-auth.ts
import type { Directive } from 'vue'
import { useAuthStore } from '@/stores/auth'

export const vAuth: Directive = {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const { value } = binding

    // 单个权限
    if (typeof value === 'string') {
      if (!authStore.permissions?.includes(value)) {
        el.parentNode?.removeChild(el)
      }
    }
    // 多个权限（满足任一即可）
    else if (Array.isArray(value)) {
      const hasPermission = value.some(p => authStore.permissions?.includes(p))
      if (!hasPermission) {
        el.parentNode?.removeChild(el)
      }
    }
  }
}

// 使用示例
// <el-button v-auth="'user:delete'">删除</el-button>
// <el-button v-auth="['user:edit', 'user:delete']">操作</el-button>
```

---

## 6. 分页处理规范

### 6.1 分页参数定义

```typescript
// 分页参数
export interface PaginationParams {
  page: number       // 当前页码，默认 1
  page_size: number  // 每页数量，默认 20
}

// 分页响应
export interface PaginatedData<T> {
  count: number      // 总数量
  next: string | null  // 下一页链接
  previous: string | null  // 上一页链接
  results: T[]       // 数据列表
}
```

### 6.2 分页 Hook

```typescript
// hooks/usePagination.ts
import { ref, reactive, watch } from 'vue'

export function usePagination<T>(
  fetchFn: (params: any) => Promise<PaginatedData<T>>,
  immediate = true
) {
  const loading = ref(false)
  const tableData = ref<T[]>([]) as { value: T[] }
  const total = ref(0)

  const pagination = reactive({
    page: 1,
    page_size: 20,
    total: 0
  })

  async function fetchData() {
    loading.value = true
    try {
      const data = await fetchFn({
        page: pagination.page,
        page_size: pagination.page_size
      })

      tableData.value = data.results
      pagination.total = data.count
    } catch (error) {
      console.error('获取数据失败:', error)
    } finally {
      loading.value = false
    }
  }

  function handlePageChange(page: number) {
    pagination.page = page
    fetchData()
  }

  function handleSizeChange(size: number) {
    pagination.page_size = size
    pagination.page = 1
    fetchData()
  }

  if (immediate) {
    fetchData()
  }

  return {
    loading,
    tableData,
    pagination,
    fetchData,
    handlePageChange,
    handleSizeChange
  }
}
```

### 6.3 分页组件使用

```vue
<template>
  <el-table v-loading="loading" :data="tableData">
    <el-table-column prop="name" label="名称" />
  </el-table>

  <el-pagination
    v-model:current-page="pagination.page"
    v-model:page-size="pagination.page_size"
    :total="pagination.total"
    :page-sizes="[10, 20, 50, 100]"
    layout="total, sizes, prev, pager, next, jumper"
    @size-change="handleSizeChange"
    @current-change="handlePageChange"
  />
</template>

<script setup lang="ts">
import { usePagination } from '@/hooks/usePagination'
import { getUserList } from '@/api/modules/user'

const {
  loading,
  tableData,
  pagination,
  handlePageChange,
  handleSizeChange
} = usePagination(getUserList)
</script>
```

---

## 7. 文件上传规范

### 7.1 上传接口封装

```typescript
// api/modules/upload.ts
import request from '../request'

interface UploadResponse {
  url: string
  filename: string
}

/**
 * 上传图片
 */
export function uploadImage(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('image', file)

  return request.post('/api/upload/image/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/**
 * 上传多个图片
 */
export function uploadImages(files: File[]): Promise<UploadResponse[]> {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('images', file)
  })

  return request.post('/api/upload/images/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
```

### 7.2 上传组件封装

```vue
<template>
  <el-upload
    :action="uploadUrl"
    :headers="uploadHeaders"
    :file-list="fileList"
    :on-success="handleSuccess"
    :on-error="handleError"
    :before-upload="beforeUpload"
    list-type="picture-card"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  modelValue: string[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
}>()

const authStore = useAuthStore()
const fileList = ref<{ name: string; url: string }[]>([])

const uploadUrl = `${import.meta.env.VITE_API_BASE_URL}/api/upload/image/`
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${authStore.token}`
}))

function handleSuccess(response: any) {
  const url = response.url
  const newList = [...props.modelValue, url]
  emit('update:modelValue', newList)
  ElMessage.success('上传成功')
}

function handleError() {
  ElMessage.error('上传失败')
}

function beforeUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }
  return true
}
</script>
```

---

## 8. 数据转换规范

### 8.1 日期格式处理

```typescript
// utils/date.ts
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.locale('zh-cn')
dayjs.extend(relativeTime)

/**
 * 格式化日期
 */
export function formatDate(date: string | number | Date, format = 'YYYY-MM-DD'): string {
  return dayjs(date).format(format)
}

/**
 * 格式化日期时间
 */
export function formatDateTime(date: string | number | Date): string {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

/**
 * 相对时间
 */
export function fromNow(date: string | number | Date): string {
  return dayjs(date).fromNow()
}
```

### 8.2 金额格式处理

```typescript
// utils/currency.ts

/**
 * 格式化金额
 */
export function formatCurrency(amount: number, decimals = 2): string {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(amount)
}

/**
 * 格式化数字（千分位）
 */
export function formatNumber(num: number): string {
  return new Intl.NumberFormat('zh-CN').format(num)
}

/**
 * 金额分转元
 */
export function centsToYuan(cents: number): number {
  return cents / 100
}

/**
 * 金额元转分
 */
export function yuanToCents(yuan: number): number {
  return Math.round(yuan * 100)
}
```

### 8.3 状态文本转换

```typescript
// utils/status.ts

/**
 * 订单状态映射
 */
export const ORDER_STATUS_MAP: Record<string, { label: string; type: string }> = {
  pending_payment: { label: '待付款', type: 'warning' },
  pending_shipment: { label: '待发货', type: 'info' },
  shipped: { label: '已发货', type: 'primary' },
  completed: { label: '已完成', type: 'success' },
  cancelled: { label: '已取消', type: 'danger' }
}

/**
 * 获取订单状态文本
 */
export function getOrderStatusLabel(status: string): string {
  return ORDER_STATUS_MAP[status]?.label || status
}

/**
 * 获取订单状态类型
 */
export function getOrderStatusType(status: string): string {
  return ORDER_STATUS_MAP[status]?.type || 'info'
}
```

---

## 9. 代码风格规范

### 9.1 API 模块定义规范

```typescript
// api/modules/user.ts
import { get, post, put, del } from '../index'

// 类型定义
export interface User {
  id: number
  nickname: string
  phone: string
  avatar: string
  created_at: string
}

export interface UserListParams {
  page?: number
  page_size?: number
  keyword?: string
  status?: string
}

// API 函数
export function getUserList(params: UserListParams): Promise<PaginatedResponse<User>> {
  return get('/api/users/', params)
}

export function getUserDetail(id: number): Promise<User> {
  return get(`/api/users/${id}/`)
}

export function createUser(data: Partial<User>): Promise<User> {
  return post('/api/users/', data)
}

export function updateUser(id: number, data: Partial<User>): Promise<User> {
  return put(`/api/users/${id}/`, data)
}

export function deleteUser(id: number): Promise<void> {
  return del(`/api/users/${id}/`)
}
```

### 9.2 统一导出

```typescript
// api/index.ts

// 认证相关
export * from './modules/auth'

// 用户相关
export * from './modules/user'

// 商品相关
export * from './modules/product'

// 订单相关
export * from './modules/order'

// 公共
export { get, post, put, patch, del, upload } from './index'
export type { ApiResponse, PaginatedResponse } from './types'
```

### 9.3 注释规范

```typescript
/**
 * 获取用户列表
 *
 * @param params - 查询参数
 * @param params.page - 页码，默认 1
 * @param params.page_size - 每页数量，默认 20
 * @param params.keyword - 搜索关键词
 * @param params.status - 状态筛选
 *
 * @returns 分页用户数据
 *
 * @example
 * ```ts
 * const data = await getUserList({ page: 1, page_size: 10, keyword: '张' })
 * ```
 */
export function getUserList(params: UserListParams): Promise<PaginatedResponse<User>> {
  return get('/api/users/', params)
}
```

---

## 10. 测试规范

### 10.1 API Mock

```typescript
// mocks/user.ts
import { MockMethod } from 'vite-plugin-mock'

export default [
  {
    url: '/api/users/',
    method: 'get',
    response: (params: any) => {
      return {
        code: 200,
        message: '获取成功',
        data: {
          count: 100,
          next: null,
          previous: null,
          results: [
            { id: 1, nickname: '用户1', phone: '13800138001' }
          ]
        }
      }
    }
  },
  {
    url: '/api/users/:id',
    method: 'get',
    response: {
      code: 200,
      message: '获取成功',
      data: {
        id: 1,
        nickname: '用户1',
        phone: '13800138001',
        created_at: '2026-01-01T00:00:00Z'
      }
    }
  }
] as MockMethod[]
```

### 10.2 接口测试用例

```typescript
// tests/user.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { getUserList } from '@/api/modules/user'

describe('用户接口', () => {
  it('应该正确返回用户列表', async () => {
    const data = await getUserList({ page: 1, page_size: 10 })

    expect(data).toHaveProperty('count')
    expect(data).toHaveProperty('results')
    expect(Array.isArray(data.results)).toBe(true)
  })

  it('应该正确处理空列表', async () => {
    const data = await getUserList({ page: 999 })

    expect(data.count).toBe(0)
    expect(data.results).toEqual([])
  })
})
```

---

## 附录

### A. 常用类型速查

```typescript
// 通用 ID
type ID = number | string

// 分页参数
interface PaginationParams {
  page?: number
  page_size?: number
}

// 排序参数
interface SortableParams {
  ordering?: string
}

// 筛选参数
interface FilterableParams {
  [key: string]: any
}

// 复合查询参数
type QueryParams = PaginationParams & SortableParams & FilterableParams
```

### B. 错误码速查

| Code | 说明 | 前端处理 |
|------|------|---------|
| 200 | 成功 | 返回 data |
| 201 | 创建成功 | 提示并跳转 |
| 400 | 参数错误 | 显示错误信息 |
| 401 | 未认证 | 跳转登录 |
| 403 | 无权限 | 显示无权限 |
| 404 | 不存在 | 显示不存在 |
| 500 | 服务器错误 | 提示重试 |

### C. 快速检查清单

- [ ] 所有 API 通过封装的方法调用
- [ ] Token 自动添加到请求头
- [ ] 错误信息友好提示
- [ ] 分页逻辑统一处理
- [ ] 加载状态正确显示
- [ ] 类型定义完整
- [ ] 代码注释清晰

---

**文档维护：** 本规范应随着项目发展持续更新。
**对应后端规范：** 参考 `backend-api-standards.md`
