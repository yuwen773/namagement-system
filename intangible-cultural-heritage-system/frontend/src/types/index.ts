// API 响应统一格式
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  total?: number
}

// 用户相关类型
export type UserRole = 'admin' | 'user'

export interface User {
  id: number
  username: string
  role: UserRole
}

// 用户详细信息
export interface UserDetail {
  id: number
  username: string
  role: UserRole
  email: string
  is_active: boolean
  last_login_time: string | null
  date_joined: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

// 分类相关类型
export interface Category {
  id: number
  name: string
  code: string
  level: 'national' | 'provincial' | 'city_county'
  parent_id: number | null
  parent?: Category | null
  created_at: string
  updated_at: string
}

export interface CategoryTree extends Category {
  children: CategoryTree[]
}

// 地区相关类型
export interface Region {
  id: number
  country_code: string
  country_name: string
  continent?: string
  latitude: number
  longitude: number
}

// 非遗项目相关类型
export interface HeritageItem {
  id: number
  name: string
  category: Category
  level: 'national' | 'provincial' | 'city_county'
  region: Region
  area?: string
  protection_unit?: string
  description?: string
  created_at: string
  updated_at: string
}

export interface HeritageItemCreate {
  name: string
  category: number
  level: 'national' | 'provincial' | 'city_county'
  region: number
  area?: string
  protection_unit?: string
  description?: string
}

// 传承人相关类型
export interface Inheritor {
  id: number
  name: string
  heritage_item: {
    id: number
    name: string
    level: string
  }
  region: Region
  gender?: 'male' | 'female' | 'other'
  level?: 'national' | 'provincial' | 'city_county'
  area?: string
  description?: string
  created_at: string
  updated_at: string
}

export interface InheritorCreate {
  name: string
  heritage_item: number
  region: number
  gender?: 'male' | 'female' | 'other'
  level?: 'national' | 'provincial' | 'city_county'
  area?: string
  description?: string
}

// 驾驶舱相关类型
export interface DashboardOverview {
  heritage_count: number
  inheritor_count: number
  category_count: number
  country_count: number
}

export interface MapPoint {
  country_code: string
  country_name: string
  longitude: number
  latitude: number
  heritage_count: number
  inheritor_count: number
}

export interface CategoryDistribution {
  category_name: string
  heritage_count: number
  percentage: number
}

export interface CountryRanking {
  rank: number
  country_name: string
  heritage_count: number
}

// 分页参数
export interface PaginationParams {
  page?: number
  page_size?: number
}

// 列表查询参数
export interface HeritageListParams extends PaginationParams {
  category?: number
  level?: string
  region?: number
  name?: string
}

export interface InheritorListParams extends PaginationParams {
  heritage_item?: number
  level?: string
  region?: number
  name?: string
}

// 用户注册相关类型
export interface RegisterRequest {
  username: string
  password: string
  email: string
}

export interface CheckUsernameRequest {
  username: string
}

export interface CheckEmailRequest {
  email: string
}

export interface UserListParams extends PaginationParams {
  username?: string
  role?: UserRole
  is_active?: boolean
}

export interface CreateUserRequest {
  username: string
  password: string
  email: string
  role?: UserRole
}

export interface UpdateUserRequest {
  email?: string
  role?: UserRole
}

export interface UpdateUserStatusRequest {
  user_ids: number[]
  is_active: boolean
}

export interface UpdateUserRoleRequest {
  user_ids: number[]
  role: UserRole
}

export interface ResetUserPasswordRequest {
  user_id: number
  new_password: string
}
