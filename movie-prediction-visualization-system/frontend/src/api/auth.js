/**
 * API 接口 - 用户认证
 */
import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/accounts/login/',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/accounts/register/',
    method: 'post',
    data
  })
}

// 获取当前用户信息
export function getCurrentUser() {
  return request({
    url: '/accounts/me/',
    method: 'get'
  })
}

// 刷新 Token
export function refreshToken(data) {
  return request({
    url: '/accounts/token/refresh/',
    method: 'post',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/accounts/password/change/',
    method: 'post',
    data
  })
}

// 登出
export function logout() {
  return request({
    url: '/accounts/logout/',
    method: 'post'
  })
}
