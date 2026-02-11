/**
 * API 接口 - 用户认证
 */
import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

// 获取当前用户信息
export function getCurrentUser() {
  return request({
    url: '/auth/profile/',
    method: 'get'
  })
}

// 刷新 Token
export function refreshToken(data) {
  return request({
    url: '/auth/token/refresh/',
    method: 'post',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/auth/password/change/',
    method: 'post',
    data
  })
}

// 更新用户个人信息
export function updateProfile(data) {
  return request({
    url: '/auth/profile/',
    method: 'put',
    data
  })
}

// 登出
export function logout() {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}
