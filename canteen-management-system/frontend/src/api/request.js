import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { showLoading, hideLoading } from '@/utils/loading'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    showLoading()
    return config
  },
  (error) => {
    hideLoading()
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    hideLoading()
    const res = response.data
    if (res.code === 200 || res.code === 201) {
      return res
    } else {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  (error) => {
    hideLoading()

    // 网络错误（无响应）
    if (!error.response) {
      ElMessage.error('网络连接失败，请检查网络设置')
      return Promise.reject(error)
    }

    const status = error.response.status
    const responseData = error.response.data
    const message = responseData?.message || '请求失败'

    switch (status) {
      case 401:
        ElMessageBox.confirm(
          '登录状态已过期，请重新登录',
          '提示',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          window.location.href = '/login'
        }).catch(() => {})
        break
      case 400:
      case 403:
      case 404:
      case 422:
        ElMessage.error(message)
        break
      case 500:
      case 502:
      case 503:
      case 504:
        ElMessage.error('服务器错误，请稍后重试')
        break
      default:
        ElMessage.error(message)
    }

    return Promise.reject(error)
  }
)

export default request
