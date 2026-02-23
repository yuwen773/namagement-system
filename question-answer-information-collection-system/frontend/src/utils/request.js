import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { clearAuth } from '@/utils/auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 防止重复跳转登录页的标志
let isRedirecting = false

// Request interceptor
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code === 0 || res.code === 200) {
      return res
    }
    ElMessage.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          // 防止重复跳转
          if (!isRedirecting) {
            isRedirecting = true
            ElMessage.warning({
              message: '登录已过期，请重新登录',
              duration: 2000,
              onClose: () => {
                isRedirecting = false
              }
            })
            clearAuth()
            // 立即跳转到登录页
            router.push('/login').catch(() => {
              isRedirecting = false
            })
          }
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error(data.message || '服务器错误')
          break
        default:
          ElMessage.error(data.message || '请求失败')
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请稍后重试')
    } else {
      ElMessage.error('网络连接失败，请检查网络')
    }
    return Promise.reject(error)
  }
)

export default request
