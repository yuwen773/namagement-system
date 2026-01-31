import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

/**
 * 用户登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise} 登录结果
 */
export function login(username, password) {
  return request.post('/api/accounts/login/', { username, password })
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @returns {Promise} 注册结果
 */
export function register(data) {
  return request.post('/api/accounts/register/', data)
}

/**
 * 获取当前用户信息
 * @returns {Promise} 用户信息
 */
export function getCurrentUser() {
  return request.get('/api/accounts/me/')
}

/**
 * 更新用户资料
 * @param {Object} data - 更新数据
 * @returns {Promise} 更新结果
 */
export function updateProfile(data) {
  return request.put('/api/accounts/me/', data)
}

/**
 * 修改密码
 * @param {Object} data - { old_password, new_password, new_password_confirm }
 * @returns {Promise} 修改结果
 */
export function changePassword(data) {
  return request.put('/api/accounts/password/', data)
}

/**
 * 角色检查
 * @returns {Promise} 角色信息
 */
export function checkRole() {
  return request.get('/api/accounts/role-check/')
}

export default request
