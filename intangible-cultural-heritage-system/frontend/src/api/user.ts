import request from '@/utils/request'
import type {
  ApiResponse,
  CheckUsernameRequest,
  CheckEmailRequest,
  RegisterRequest,
  UserDetail,
  UserListParams,
  CreateUserRequest,
  UpdateUserRequest,
  UpdateUserStatusRequest,
  UpdateUserRoleRequest,
  ResetUserPasswordRequest
} from '@/types'

// 检查用户名是否可用
export const checkUsername = (username: string) => {
  return request.post<ApiResponse<{ exists: boolean }>>('/auth/check-username/', { username })
}

// 检查邮箱是否可用
export const checkEmail = (email: string) => {
  return request.post<ApiResponse<{ exists: boolean }>>('/auth/check-email/', { email })
}

// 用户注册
export const register = (data: RegisterRequest) => {
  return request.post<ApiResponse<UserDetail>>('/auth/register/', data)
}

// 获取用户列表
export const getUserList = (params?: UserListParams) => {
  return request.get<ApiResponse<UserDetail[]>>('/users/', { params })
}

// 创建用户
export const createUser = (data: CreateUserRequest) => {
  return request.post<ApiResponse<UserDetail>>('/users/', data)
}

// 更新用户信息
export const updateUser = (id: number, data: UpdateUserRequest) => {
  return request.patch<ApiResponse<UserDetail>>(`/users/${id}/`, data)
}

// 批量更新用户状态
export const updateUserStatus = (data: UpdateUserStatusRequest) => {
  return request.patch<ApiResponse<{ updated_count: number }>>('/users/update-status/', data)
}

// 批量更新用户角色
export const updateUserRole = (data: UpdateUserRoleRequest) => {
  return request.patch<ApiResponse<{ updated_count: number }>>('/users/update-role/', data)
}

// 重置用户密码
export const resetUserPassword = (data: ResetUserPasswordRequest) => {
  return request.patch<ApiResponse<{ user_id: number; username: string }>>('/users/reset-password/', data)
}

// 删除用户
export const deleteUser = (id: number) => {
  return request.delete<ApiResponse<null>>(`/users/${id}/`)
}
