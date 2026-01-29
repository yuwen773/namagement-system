import request from './request'

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 */
export function login(username, password) {
  return request({
    url: '/accounts/login/',
    method: 'post',
    data: { username, password }
  })
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 */
export function register(data) {
  return request({
    url: '/accounts/register/',
    method: 'post',
    data
  })
}

/**
 * 获取用户信息
 * @param {number} id - 用户ID
 */
export function getUserInfo(id) {
  return request({
    url: `/accounts/${id}/`,
    method: 'get'
  })
}

/**
 * 修改密码
 * @param {number} id - 用户ID
 * @param {Object} data - 密码数据
 * @param {string} data.old_password - 旧密码
 * @param {string} data.new_password - 新密码
 */
export function changePassword(id, data) {
  return request({
    url: `/accounts/${id}/change_password/`,
    method: 'post',
    data
  })
}
