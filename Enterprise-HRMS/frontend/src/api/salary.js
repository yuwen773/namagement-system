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

/**
 * 薪资异常处理 API
 */

/**
 * 获取异常列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 状态筛选
 * @param {string} params.exception_type - 类型筛选
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise}
 */
export function getExceptionList(params) {
  return axios.get('/salary/exceptions/', { params })
}

/**
 * 获取异常详情
 * @param {number} id - 异常ID
 * @returns {Promise}
 */
export function getExceptionDetail(id) {
  return axios.get(`/salary/exceptions/${id}/`)
}

/**
 * 上报异常
 * @param {Object} data - 异常数据
 * @param {number} data.salary_record - 薪资记录ID
 * @param {string} data.exception_type - 异常类型
 * @param {string} data.description - 异常描述
 * @returns {Promise}
 */
export function reportException(data) {
  return axios.post('/salary/exceptions/', data)
}

/**
 * 处理异常
 * @param {number} id - 异常ID
 * @param {Object} data - 处理数据
 * @param {string} data.resolution - 处理方案
 * @param {number} data.adjustment_amount - 调整金额
 * @param {string} data.status - 处理状态
 * @returns {Promise}
 */
export function resolveException(id, data) {
  return axios.post(`/salary/exceptions/${id}/resolve/`, data)
}

/**
 * 获取我上报的异常列表
 * @returns {Promise}
 */
export function getMyExceptions() {
  return axios.get('/salary/exceptions/my-exceptions/')
}

/**
 * 获取待处理异常列表（HR/Admin）
 * @returns {Promise}
 */
export function getPendingExceptions() {
  return axios.get('/salary/exceptions/pending/')
}

/**
 * 获取异常统计信息
 * @returns {Promise}
 */
export function getExceptionStatistics() {
  return axios.get('/salary/exceptions/statistics/')
}

/**
 * 获取薪资记录列表（用于上报异常时选择）
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getSalaryRecordsForException(params) {
  return axios.get('/salary/records/', { params })
}

export default {
  calculateSalary,
  getSalaryRecords,
  getSalaryRecordDetail,
  saveSalaryRecord,
  publishSalaryRecords,
  getExceptionList,
  getExceptionDetail,
  reportException,
  resolveException,
  getMyExceptions,
  getPendingExceptions,
  getExceptionStatistics,
  getSalaryRecordsForException
}
