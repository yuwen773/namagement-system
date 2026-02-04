import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 添加 Token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求配置错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const { code, message, data } = response.data

    // 业务成功
    if (code === 200 || code === 201) {
      return data
    }

    // 业务错误
    ElMessage.error(message || '请求失败')
    return Promise.reject(new Error(message))
  },
  (error) => {
    // HTTP 错误处理
    const status = error.response?.status

    switch (status) {
      case 401:
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('token')
        window.location.href = '/login'
        break
      case 403:
        ElMessage.error('没有权限访问')
        break
      case 404:
        ElMessage.error('请求的资源不存在')
        break
      case 500:
        ElMessage.error('服务器错误，请稍后重试')
        break
      default:
        ElMessage.error(error.message || '网络错误')
    }

    return Promise.reject(error)
  }
)

export default request

// 请求方法封装
export function get(url, params, config) {
  return request.get(url, { params, ...config })
}

export function post(url, data, config) {
  return request.post(url, data, config)
}

export function put(url, data, config) {
  return request.put(url, data, config)
}

export function patch(url, data, config) {
  return request.patch(url, data, config)
}

export function del(url, params, config) {
  return request.delete(url, { params, ...config })
}
