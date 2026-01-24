import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @param {string} data.real_name - 真实姓名
 * @param {string} data.phone - 手机号
 * @param {string} data.email - 邮箱
 * @returns {Promise}
 */
export function register(data) {
  return api.post('/auth/register/', data)
}

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise}
 */
export function login(username, password) {
  return api.post('/auth/login/', { username, password })
}

/**
 * 刷新 Token
 * @param {string} refresh - 刷新令牌
 * @returns {Promise}
 */
export function refreshToken(refresh) {
  return api.post('/auth/token/refresh/', { refresh })
}

/**
 * 管理员重置用户密码
 * @param {number} userId - 用户ID
 * @param {string} newPassword - 新密码
 * @returns {Promise}
 */
export function resetPassword(userId, newPassword) {
  return api.post(`/auth/users/${userId}/reset-password/`, { new_password: newPassword })
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getCurrentUser() {
  return api.get('/auth/me/')
}

export default {
  register,
  login,
  refreshToken,
  resetPassword,
  getCurrentUser
}
