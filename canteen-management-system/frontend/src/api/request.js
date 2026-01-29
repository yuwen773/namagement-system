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
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    // 显示全局 Loading
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
    // 隐藏全局 Loading
    hideLoading()
    const res = response.data
    // 后端返回格式：{ code, message, data }
    if (res.code === 200 || res.code === 201) {
      return res
    } else {
      // 业务错误处理
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5000
      })
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  (error) => {
    // 隐藏全局 Loading
    hideLoading()

    // 网络错误处理（无响应）
    if (!error.response) {
      ElMessage({
        message: '网络连接失败，请检查网络设置',
        type: 'error',
        duration: 5000
      })
      return Promise.reject(error)
    }

    // HTTP 错误状态处理
    const status = error.response.status
    switch (status) {
      case 400:
        ElMessage.error('请求参数错误')
        break
      case 401:
        // 使用确认对话框提示用户重新登录
        ElMessageBox.confirm(
          '登录状态已过期，请重新登录',
          '提示',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          // 清除 token 和用户信息
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          // 跳转到登录页
          window.location.href = '/login'
        }).catch(() => {
          // 用户取消操作
        })
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
      case 502:
        ElMessage.error('网关错误，请稍后重试')
        break
      case 503:
        ElMessage.error('服务不可用，请稍后重试')
        break
      case 504:
        ElMessage.error('网关超时，请稍后重试')
        break
      default:
        ElMessage.error(`请求失败 (${status})`)
    }

    return Promise.reject(error)
  }
)

export default request
