/**
 * 账号相关 API
 * 对应后端: backend/accounts/
 *
 * 包含: 注册、登录、Token刷新、个人信息、修改密码、注销账号
 */

import request from './request'

export default {
  /**
   * 用户注册
   * @param {Object} data - 注册数据
   * @param {string} data.username - 用户名 (必填, 最大50字符, 唯一)
   * @param {string} data.password - 密码 (必填)
   * @param {string} data.password_confirm - 确认密码 (必填, 需与password一致)
   * @param {string} data.real_name - 真实姓名 (可选, 最大50字符)
   * @param {string} data.phone - 手机号 (可选, 最大20字符)
   * @param {string} data.email - 邮箱 (可选, 邮箱格式, 最大100字符)
   * @returns {Promise} { code: 0, message: "注册成功", data: { id, username, real_name, phone, email, role } }
   */
  register(data) {
    return request({
      url: '/accounts/register/',
      method: 'post',
      data
    })
  },

  /**
   * 用户登录
   * @param {Object} data - 登录数据
   * @param {string} data.username - 用户名 (必填)
   * @param {string} data.password - 密码 (必填)
   * @returns {Promise} { code: 0, message: "登录成功", data: { access_token, refresh_token, user } }
   */
  login(data) {
    return request({
      url: '/accounts/login/',
      method: 'post',
      data
    })
  },

  /**
   * 刷新 Token
   * @param {string} refresh - refresh_token
   * @returns {Promise} { access: "新的access_token", refresh: "新的refresh_token" }
   */
  refreshToken(refresh) {
    return request({
      url: '/accounts/token/refresh/',
      method: 'post',
      data: { refresh }
    })
  },

  /**
   * 获取当前用户信息
   * @returns {Promise} { code: 0, data: { id, username, real_name, phone, email, role, is_active, created_at, updated_at } }
   */
  getProfile() {
    return request({
      url: '/accounts/profile/',
      method: 'get'
    })
  },

  /**
   * 更新当前用户信息
   * @param {Object} data - 更新数据 (所有字段可选)
   * @param {string} data.real_name - 真实姓名 (最大50字符)
   * @param {string} data.phone - 手机号 (最大20字符)
   * @param {string} data.email - 邮箱 (邮箱格式, 最大100字符)
   * @returns {Promise} { code: 0, message: "更新成功", data: {...} }
   */
  updateProfile(data) {
    return request({
      url: '/accounts/profile/',
      method: 'put',
      data
    })
  },

  /**
   * 修改密码
   * @param {Object} data - 密码数据
   * @param {string} data.old_password - 旧密码 (必填)
   * @param {string} data.new_password - 新密码 (必填, 最少6位)
   * @param {string} data.new_password_confirm - 确认新密码 (必填, 需与new_password一致)
   * @returns {Promise} { code: 0, message: "密码修改成功" }
   */
  changePassword(data) {
    return request({
      url: '/accounts/change-password/',
      method: 'post',
      data
    })
  },

  /**
   * 注销账号 (逻辑删除)
   * @returns {Promise} { code: 0, message: "账号注销成功" }
   */
  deleteAccount() {
    return request({
      url: '/accounts/delete-account/',
      method: 'delete'
    })
  }
}
