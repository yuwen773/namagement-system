import axios from './axios'

/**
 * 薪资管理 API
 */

/**
 * 计算薪资
 * @param {Object} data - 计算参数
 * @param {number} data.user_id - 用户ID
 * @param {string} data.month - 月份 (YYYY-MM)
 * @returns {Promise}
 */
export function calculateSalary(data) {
  return axios.post('/salary/calculate/', data)
}

/**
 * 获取薪资记录列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.month - 单月查询 (YYYY-MM)
 * @param {string} params.month_start - 月份范围开始 (YYYY-MM)
 * @param {string} params.month_end - 月份范围结束 (YYYY-MM)
 * @returns {Promise}
 */
export function getSalaryRecords(params) {
  return axios.get('/salary/records/', { params })
}

/**
 * 获取薪资记录详情
 * @param {number} id - 记录ID
 * @returns {Promise}
 */
export function getSalaryRecordDetail(id) {
  return axios.get(`/salary/records/${id}/`)
}

/**
 * 保存薪资记录
 * @param {Object} data - 保存参数
 * @param {number} data.user_id - 用户ID
 * @param {string} data.month - 月份 (YYYY-MM)
 * @returns {Promise}
 */
export function saveSalaryRecord(data) {
  return axios.post('/salary/records/save/', data)
}

/**
 * 发布薪资记录
 * @param {number[]} ids - 薪资记录ID数组
 * @returns {Promise}
 */
export function publishSalaryRecords(ids) {
  return axios.post('/salary/records/publish/', { ids })
}

export default {
  calculateSalary,
  getSalaryRecords,
  getSalaryRecordDetail,
  saveSalaryRecord,
  publishSalaryRecords
}
