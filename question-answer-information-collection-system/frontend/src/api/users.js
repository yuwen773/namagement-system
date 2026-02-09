import request from '@/utils/request'

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.search - 搜索关键词
 */
export function getUserList(params) {
  return request.get('/api/auth/users/', { params })
}

/**
 * 获取单个用户
 * @param {number} id - 用户ID
 */
export function getUser(id) {
  return request.get(`/api/auth/users/${id}/`)
}

/**
 * 创建用户
 * @param {Object} data - 用户数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @param {string} data.role - 角色 (admin/user)
 */
export function createUser(data) {
  return request.post('/api/auth/register/', data)
}

/**
 * 更新用户
 * @param {number} id - 用户ID
 * @param {Object} data - 用户数据
 */
export function updateUser(id, data) {
  return request.patch(`/api/auth/users/${id}/`, data)
}

/**
 * 删除用户
 * @param {number} id - 用户ID
 */
export function deleteUser(id) {
  return request.delete(`/api/auth/users/${id}/`)
}

/**
 * 修改密码
 * @param {Object} data - 密码修改数据
 * @param {string} data.old_password - 旧密码
 * @param {string} data.new_password - 新密码
 */
export function changePassword(data) {
  return request.post('/api/auth/change-password/', data)
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return request.get('/api/auth/me/')
}

/**
 * 更新用户信息
 * @param {Object} data - 用户数据
 */
export function updateUserInfo(data) {
  return request.patch('/api/auth/me/', data)
}
