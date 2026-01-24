import axios from './axios'

/**
 * 仪表盘统计 API
 */

/**
 * 获取仪表盘统计数据
 * 权限：仅 HR/Admin 可访问
 * @returns {Promise}
 */
export function getDashboardStats() {
  return axios.get('/dashboard/stats/')
}

export default {
  getDashboardStats
}
