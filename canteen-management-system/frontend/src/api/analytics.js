import request from './request'

/**
 * 统计分析 API
 */

/**
 * 获取人员统计数据
 * @returns {Promise} 岗位分布、持证率等统计数据
 */
export function getEmployeeStatistics() {
  return request({
    url: '/analytics/employees/',
    method: 'get'
  })
}

/**
 * 获取考勤统计数据
 * @param {Object} params - 查询参数
 * @param {number} params.days - 最近 N 天（可选）
 * @param {string} params.start_date - 开始日期（可选）
 * @param {string} params.end_date - 结束日期（可选）
 * @returns {Promise} 考勤统计数据
 */
export function getAttendanceStatistics(params = {}) {
  return request({
    url: '/analytics/attendance/',
    method: 'get',
    params
  })
}

/**
 * 获取薪资统计数据
 * @param {Object} params - 查询参数
 * @param {number} params.months - 最近 N 个月（可选）
 * @returns {Promise} 薪资统计数据
 */
export function getSalaryStatistics(params = {}) {
  return request({
    url: '/analytics/salaries/',
    method: 'get',
    params
  })
}

/**
 * 获取总览统计数据（Dashboard 首页）
 * @returns {Promise} 今日概览、待办事项等统计数据
 */
export function getOverviewStatistics() {
  return request({
    url: '/analytics/overview/',
    method: 'get'
  })
}
