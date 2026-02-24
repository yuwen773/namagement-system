import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/stores/user'

/**
 * Create axios instance with base configuration
 */
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor
 * - Add authorization token to headers
 * - Add timestamp to prevent caching
 */
service.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    const token = userStore.token

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }

    // Add timestamp for GET requests to prevent caching
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      }
    }

    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

/**
 * Response interceptor
 * - Handle common response codes
 * - Handle token expiration
 * - Show error messages
 */
service.interceptors.response.use(
  (response) => {
    const res = response.data

    // API returns { code: 0, data: {...}, message: '...' }
    // If code is 0, return the data directly
    if (res.code === 0) {
      return res
    }

    // Handle business logic errors
    if (res.code !== 0) {
      ElMessage({
        message: res.message || 'Request failed',
        type: 'error',
        duration: 5000,
      })

      // Specific error handling
      if (res.code === 401) {
        // Token expired or invalid
        handleUnauthorized()
      }

      return Promise.reject(new Error(res.message || 'Error'))
    }

    return res
  },
  (error) => {
    console.error('Response error:', error)

    // Handle HTTP status codes
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          handleUnauthorized()
          break
        case 403:
          ElMessage({
            message: 'Permission denied',
            type: 'error',
            duration: 5000,
          })
          break
        case 404:
          ElMessage({
            message: 'Resource not found',
            type: 'error',
            duration: 5000,
          })
          break
        case 500:
          ElMessage({
            message: data?.message || 'Server error',
            type: 'error',
            duration: 5000,
          })
          break
        default:
          ElMessage({
            message: data?.message || error.message || 'Request failed',
            type: 'error',
            duration: 5000,
          })
      }
    } else if (error.request) {
      // Request was made but no response received
      ElMessage({
        message: 'Network error, please check your connection',
        type: 'error',
        duration: 5000,
      })
    } else {
      // Something happened in setting up the request
      ElMessage({
        message: error.message || 'Request configuration error',
        type: 'error',
        duration: 5000,
      })
    }

    return Promise.reject(error)
  }
)

/**
 * Handle unauthorized access (401)
 * - Clear user token and info
 * - Redirect to login page
 */
function handleUnauthorized() {
  const userStore = useUserStore()

  ElMessageBox.confirm(
    'Your session has expired. Please log in again.',
    'Session Expired',
    {
      confirmButtonText: 'Re-login',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
      userStore.logout()
      router.push({
        path: '/login',
        query: {
          redirect: router.currentRoute.value.fullPath,
        },
      })
    })
    .catch(() => {
      userStore.logout()
      router.push('/login')
    })
}

/**
 * Download file helper
 * @param {string} url - Download URL
 * @param {object} params - Request parameters
 * @param {string} filename - Download filename
 */
export function downloadFile(url, params, filename) {
  return service
    .get(url, {
      params,
      responseType: 'blob',
    })
    .then((response) => {
      const blob = new Blob([response.data])
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = filename
      link.click()
      window.URL.revokeObjectURL(link.href)
      return response
    })
}

export default service
