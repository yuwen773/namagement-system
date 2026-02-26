import request from '@/utils/request'
import type { ApiResponse, LoginRequest, LoginResponse, User } from '@/types'

// 登录
export const login = (data: LoginRequest) => {
  return request.post<ApiResponse<LoginResponse>>('/auth/login/', data)
}

// 刷新 token
export const refreshToken = (refresh: string) => {
  return request.post<ApiResponse<{ access: string }>>('/auth/refresh/', { refresh })
}

// 登出
export const logout = (refresh: string) => {
  return request.post<ApiResponse<null>>('/auth/logout/', { refresh })
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<ApiResponse<User>>('/auth/me/')
}
