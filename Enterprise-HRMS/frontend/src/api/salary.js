import axios from './axios'

/**
 * 薪资管理 API
 */

/**
 * 计算薪资
 * @param {object} data - { user_id, month }
 * @returns {Promise}
 */
export function calculateSalary(data) {
  return axios.post('/salary/calculate/', data)
}

/**
 * 获取薪资记录列表
 * @param {object} params - { month }
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
 * @param {object} data - { user_id, month }
 * @returns {Promise}
 */
export function saveSalaryRecord(data) {
  return axios.post('/salary/records/save/', data)
}
