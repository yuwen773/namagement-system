import request from '@/utils/request'

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
