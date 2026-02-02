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
    // 保留完整的错误响应数据，便于前端解析
    const errorData = error.response?.data || {}
    const message = errorData.message || error.message || '请求失败'

    // 创建包含完整信息的错误对象
    const apiError = new Error(message)
    apiError.response = error.response
    apiError.data = errorData
    apiError.code = errorData.code
    apiError.errors = errorData.errors
    apiError.suggestions = errorData.data?.suggestions || []

    return Promise.reject(apiError)
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

/**
 * 获取用户列表（管理员）
 * @param {Object} params - 查询参数 { page, page_size, search, role }
 * @returns {Promise} 用户列表
 */
export function getUserList(params) {
  return request.get('/api/accounts/admin/users/', { params })
}

/**
 * 封禁用户（管理员）
 * @param {number} userId - 用户ID
 * @returns {Promise} 操作结果
 */
export function banUser(userId) {
  return request.put(`/api/accounts/admin/users/${userId}/ban/`)
}

/**
 * 解封用户（管理员）
 * @param {number} userId - 用户ID
 * @returns {Promise} 操作结果
 */
export function unbanUser(userId) {
  return request.put(`/api/accounts/admin/users/${userId}/unban/`)
}

export default request
