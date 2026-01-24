import api from './axios'

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 状态筛选 (active/inactive)
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise}
 */
export function getUserList(params) {
  return api.get('/auth/users/', { params })
}

/**
 * 更新用户角色
 * @param {number} userId - 用户ID
 * @param {string} role - 新角色 (employee/hr/admin)
 * @returns {Promise}
 */
export function updateUserRole(userId, role) {
  return api.put(`/auth/users/${userId}/role/`, { role })
}

/**
 * 更新用户状态（启用/禁用）
 * @param {number} userId - 用户ID
 * @param {boolean} isActive - 是否启用
 * @returns {Promise}
 */
export function updateUserStatus(userId, isActive) {
  return api.put(`/auth/users/${userId}/status/`, { is_active: isActive })
}

/**
 * 重置用户密码
 * @param {number} userId - 用户ID
 * @param {string} newPassword - 新密码
 * @returns {Promise}
 */
export function resetUserPassword(userId, newPassword) {
  return api.post(`/auth/users/${userId}/reset-password/`, { new_password: newPassword })
}

// 角色选项
export const ROLE_OPTIONS = [
  { value: 'employee', label: '普通员工' },
  { value: 'hr', label: '人事专员' },
  { value: 'admin', label: '系统管理员' }
]

// 角色颜色映射
export const ROLE_COLORS = {
  employee: 'info',
  hr: 'warning',
  admin: 'danger'
}

// 状态选项
export const STATUS_OPTIONS = [
  { value: 'all', label: '全部' },
  { value: 'active', label: '已启用' },
  { value: 'inactive', label: '已禁用' }
]

export default {
  getUserList,
  updateUserRole,
  updateUserStatus,
  resetUserPassword,
  ROLE_OPTIONS,
  ROLE_COLORS,
  STATUS_OPTIONS
}
