import { get, post, put } from '../request'

/**
 * 认证相关 API
 */

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 手机号
 * @param {string} data.password - 密码
 * @returns {Promise<{token: string, user: Object}>}
 */
export function loginApi(data) {
  return post('/auth/login/', data)
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 手机号
 * @param {string} data.password - 密码
 * @param {string} data.nickname - 昵称
 * @returns {Promise<{token: string, user: Object}>}
 */
export function registerApi(data) {
  return post('/auth/register/', data)
}

/**
 * 获取当前用户信息
 * @returns {Promise<Object>}
 */
export function getCurrentUserApi() {
  return get('/auth/me/')
}

/**
 * 重置密码
 * @param {Object} data - 重置密码数据
 * @param {string} data.username - 手机号
 * @param {string} data.new_password - 新密码
 * @param {string} data.code - 验证码
 * @returns {Promise<void>}
 */
export function resetPasswordApi(data) {
  return post('/auth/password/reset/', data)
}
