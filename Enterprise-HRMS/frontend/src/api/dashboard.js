import axios from './axios'

/**
 * 获取仪表盘统计数据
 * @returns {Promise<axios.AxiosResponse>}
 */
export function getDashboardStats() {
  return axios.get('/dashboard/stats/')
}
