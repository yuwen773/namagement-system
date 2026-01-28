import axios from 'axios'

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
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 后端返回格式：{ code, message, data }
    if (res.code === 200 || res.code === 201) {
      return res
    } else {
      // 错误响应
      console.error('API 错误:', res.message)
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  (error) => {
    console.error('响应错误:', error)
    // 处理 HTTP 错误状态
    if (error.response) {
      switch (error.response.status) {
        case 401:
          error.message = '未授权，请重新登录'
          // 清除 token 并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          window.location.href = '/login'
          break
        case 403:
          error.message = '拒绝访问'
          break
        case 404:
          error.message = '请求错误，未找到该资源'
          break
        case 500:
          error.message = '服务器错误'
          break
        default:
          error.message = `连接错误 ${error.response.status}`
      }
    } else if (error.request) {
      error.message = '网络错误，请检查网络连接'
    }
    return Promise.reject(error)
  }
)

export default request
