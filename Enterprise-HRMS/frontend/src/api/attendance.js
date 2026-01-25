import axios from './axios'

/**
 * 考勤管理 API
 */

/**
 * 签到
 * @returns {Promise}
 */
export function checkIn() {
  return axios.post('/attendance/check-in/')
}

/**
 * 签退
 * @returns {Promise}
 */
export function checkOut() {
  return axios.post('/attendance/check-out/')
}

/**
 * 获取今日考勤
 * @returns {Promise}
 */
export function getTodayAttendance() {
  return axios.get('/attendance/today/')
}

/**
 * 获取考勤记录列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.date_start - 开始日期 (YYYY-MM-DD)
 * @param {string} params.date_end - 结束日期 (YYYY-MM-DD)
 * @param {string} params.date - 单日查询 (YYYY-MM-DD)
 * @param {string} params.status - 状态筛选 (normal/late/early/absent/leave)
 * @param {number} params.user_id - 筛选用户（HR/Admin可用）
 * @returns {Promise}
 */
export function getAttendanceRecords(params) {
  return axios.get('/attendance/', { params })
}

/**
 * 获取考勤统计
 * @param {string} month - 月份 (YYYY-MM)
 * @returns {Promise}
 */
export function getAttendanceStats(month) {
  return axios.get('/attendance/stats/', { params: { month } })
}

/**
 * 获取月度考勤统计（按部门汇总）
 * @param {string} month - 月份 (YYYY-MM)
 * @param {number} departmentId - 部门ID（可选）
 * @returns {Promise}
 */
export function getMonthlyAttendanceStats(month, departmentId = null) {
  const params = { month }
  if (departmentId) {
    params.department_id = departmentId
  }
  return axios.get('/attendance/monthly-stats/', { params })
}

export default {
  checkIn,
  checkOut,
  getTodayAttendance,
  getAttendanceRecords,
  getAttendanceStats,
  getMonthlyAttendanceStats
}
