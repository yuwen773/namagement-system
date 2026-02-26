import request from '@/utils/request'
import type {
  ApiResponse,
  LoginRequest,
  LoginResponse,
  User,
  UserProfile,
  RegisterRequest,
  CheckUsernameRequest,
  CheckEmailRequest,
  UpdateProfileRequest,
  ChangePasswordRequest
} from '@/types'

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
  return request.get<ApiResponse<UserProfile>>('/auth/me/')
}

// 更新个人资料
export const updateProfile = (data: UpdateProfileRequest) => {
  return request.patch<ApiResponse<UserProfile>>('/auth/me/', data)
}

// 修改密码
export const changePassword = (data: ChangePasswordRequest) => {
  return request.post<ApiResponse<{ message: string }>>('/auth/me/change-password/', data)
}

// 检查用户名是否可用
export const checkUsername = (data: CheckUsernameRequest) => {
  return request.post<ApiResponse<{ available: boolean }>>('/auth/check-username/', data)
}

// 检查邮箱是否可用
export const checkEmail = (data: CheckEmailRequest) => {
  return request.post<ApiResponse<{ available: boolean }>>('/auth/check-email/', data)
}

// 用户注册
export const register = (data: RegisterRequest) => {
  return request.post<ApiResponse<LoginResponse>>('/auth/register/', data)
}
