/**
 * Axios 请求封装
 * 基于 Element Plus 的请求配置模式
 */

import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/stores/user'
import { showError, parseErrorMessage } from './errorHandler'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 从本地存储获取 token
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

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 根据状态码处理响应
    if (res.code === 0) {
      return res
    }

    // 业务错误码（code: -1 等）- 使用统一错误处理
    // 构造错误对象供 parseErrorMessage 使用
    const businessError = {
      response: {
        status: response.status || 400,
        data: res
      }
    }

    // 显示错误提示
    showError(businessError)

    // 返回拒绝的 Promise
    return Promise.reject(businessError)
  },
  (error) => {
    // HTTP 错误处理 - 使用统一错误处理
    showError(error)
    return Promise.reject(error)
  }
)

export default request
