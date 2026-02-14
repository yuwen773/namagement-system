import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.accessToken) {
      config.headers.Authorization = `Bearer ${userStore.accessToken}`
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
    const { code, data, message, ...rest } = response.data
    if (code === 0) {
      return { data, ...rest }
    } else {
      ElMessage.error(message || '请求失败')
      // 附加响应信息到错误对象，方便后续处理
      const err = new Error(message || '请求失败')
      err.response = response
      err.code = code
      return Promise.reject(err)
    }
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          const userStore = useUserStore()
          userStore.logout()
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 400:
          // 处理字段验证错误，提取友好的错误信息
          let errorMsg = ''
          if (typeof data === 'object' && data !== null) {
            const fieldErrors = []
            const fieldNameMap = {
              cover_image: '封面图片',
              rating_percentage: '好评率',
              opening_hours: '开放时间',
              region: '所属地区',
              name: '景点名称',
              category: '景点类别',
              address: '详细地址',
              description: '景点描述',
              level: '景区等级',
              ranking: '城市排名',
              latitude: '纬度',
              longitude: '经度',
              guide_count: '攻略数量',
              images: '展示图片'
            }
            for (const [key, value] of Object.entries(data)) {
              if (Array.isArray(value)) {
                const fieldName = fieldNameMap[key] || key
                fieldErrors.push(`${fieldName}: ${value.join('; ')}`)
              }
            }
            errorMsg = fieldErrors.join('; ')
          }
          ElMessage.error(errorMsg || data.detail || '请求参数错误')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(data.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

export default request
