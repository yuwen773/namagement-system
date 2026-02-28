import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 创建一个不带拦截器的 axios 实例用于刷新 token
const axiosWithoutInterceptor = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 标记是否正在刷新 token，防止多个请求同时触发
let isRefreshing = false
let failedRequestsQueue = []

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 刷新 token 的函数（使用不带拦截器的 axios）
const refreshToken = async () => {
  const refresh = localStorage.getItem('refresh_token')
  if (!refresh) {
    throw new Error('No refresh token')
  }

  try {
    const response = await axiosWithoutInterceptor.post('/api/users/token/refresh/', {
      refresh
    })
    const newAccessToken = response.data.access_token
    localStorage.setItem('access_token', newAccessToken)
    return newAccessToken
  } catch (error) {
    // 刷新失败，清除所有 token 并跳转到登录
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
    throw error
  }
}

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 如果是文件下载（blob类型），直接返回数据
    if (response.config.responseType === 'blob') {
      return response.data
    }

    // JSON响应处理
    const res = response.data
    if (res.code === 0) {
      return res
    } else {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  async error => {
    const originalRequest = error.config

    // 如果是 401 错误且不是重试请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // 如果没有 refresh_token，直接跳转登录
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        window.location.href = '/login'
        return Promise.reject(error)
      }

      // 如果已经在刷新，等待刷新完成
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedRequestsQueue.push({
            resolve: (token) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              resolve(request(originalRequest))
            },
            reject: (err) => {
              reject(err)
            }
          })
        })
      }

      // 开始刷新 token
      isRefreshing = true
      try {
        const newAccessToken = await refreshToken()

        // 更新所有等待的请求
        failedRequestsQueue.forEach(req => req.resolve(newAccessToken))
        failedRequestsQueue = []

        // 重试原请求
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return request(originalRequest)
      } catch (refreshError) {
        failedRequestsQueue.forEach(req => req.reject(refreshError))
        failedRequestsQueue = []
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    ElMessage.error(error.response?.data?.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request
