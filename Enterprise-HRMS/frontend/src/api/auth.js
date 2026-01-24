import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 登录
export function login(username, password) {
  return api.post('/auth/login/', {
    username,
    password
  })
}

// 刷新 Token
export function refreshToken(refresh) {
  return api.post('/auth/refresh/', {
    refresh
  })
}

// 获取当前用户信息
export function getCurrentUser() {
  return api.get('/auth/me/')
}

export default {
  login,
  refreshToken,
  getCurrentUser
}
