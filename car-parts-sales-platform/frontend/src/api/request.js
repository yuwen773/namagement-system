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

    // 业务错误（后端返回了错误信息）
    const errorMsg = message || '请求失败'
    ElMessage.error(errorMsg)
    return Promise.reject(new Error(errorMsg))
  },
  (error) => {
    // HTTP 错误处理
    const status = error.response?.status
    // 尝试从响应中获取后端返回的业务错误信息
    const responseData = error.response?.data
    const businessMessage = responseData?.message
    const businessErrors = responseData?.errors

    // 构建错误提示
    let errorMessage = ''

    // 优先使用业务错误信息
    if (businessMessage) {
      errorMessage = businessMessage
    } else if (businessErrors) {
      // 如果有字段错误，提取并显示
      const errorFields = Object.entries(businessErrors)
      if (errorFields.length > 0) {
        // 取第一个字段的错误信息
        const [field, errors] = errorFields[0]
        const fieldError = Array.isArray(errors) ? errors[0] : errors
        errorMessage = fieldError
      }
    }

    // 根据HTTP状态码显示错误
    switch (status) {
      case 400:
        ElMessage.error(errorMessage || '请求参数错误')
        break
      case 401:
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('token')
        window.location.href = '/login'
        break
      case 403:
        ElMessage.error(errorMessage || '没有权限访问')
        break
      case 404:
        ElMessage.error(errorMessage || '请求的资源不存在')
        break
      case 500:
        ElMessage.error(errorMessage || '服务器错误，请稍后重试')
        break
      default:
        ElMessage.error(errorMessage || error.message || '网络错误')
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
