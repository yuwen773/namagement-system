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
