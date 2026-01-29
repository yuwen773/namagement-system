import request from './request'

/**
 * 获取薪资列表
 * @param {Object} params - 查询参数 { year_month, employee, status, page, page_size }
 */
export function getSalaryList(params) {
  return request({
    url: '/salaries/salaries/',
    method: 'get',
    params
  })
}

/**
 * 获取薪资详情
 * @param {number} id - 薪资记录 ID
 */
export function getSalaryDetail(id) {
  return request({
    url: `/salaries/salaries/${id}/`,
    method: 'get'
  })
}

/**
 * 创建薪资记录
 * @param {Object} data - 薪资数据
 */
export function createSalary(data) {
  return request({
    url: '/salaries/salaries/',
    method: 'post',
    data
  })
}

/**
 * 更新薪资记录
 * @param {number} id - 薪资记录 ID
 * @param {Object} data - 薪资数据
 */
export function updateSalary(id, data) {
  return request({
    url: `/salaries/salaries/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 生成薪资（自动计算）
 * @param {Object} data - { year_month, employee_ids }
 */
export function generateSalary(data) {
  return request({
    url: '/salaries/salaries/generate/',
    method: 'post',
    data
  })
}

/**
 * 调整薪资
 * @param {number} id - 薪资记录 ID
 * @param {Object} data - { base_salary, overtime_pay, reason }
 */
export function adjustSalary(id, data) {
  return request({
    url: `/salaries/salaries/${id}/adjust/`,
    method: 'post',
    data
  })
}

/**
 * 发布薪资
 * @param {number} id - 薪资记录 ID
 */
export function publishSalary(id) {
  return request({
    url: `/salaries/salaries/${id}/publish/`,
    method: 'post'
  })
}

/**
 * 删除薪资记录
 * @param {number} id - 薪资记录 ID
 */
export function deleteSalary(id) {
  return request({
    url: `/salaries/salaries/${id}/`,
    method: 'delete'
  })
}

// ==================== 申诉相关 ====================

/**
 * 获取申诉列表
 * @param {Object} params - 查询参数 { appeal_type, employee, status, search }
 */
export function getAppealList(params) {
  return request({
    url: '/salaries/appeals/',
    method: 'get',
    params
  })
}

/**
 * 获取申诉详情
 * @param {number} id - 申诉 ID
 */
export function getAppealDetail(id) {
  return request({
    url: `/salaries/appeals/${id}/`,
    method: 'get'
  })
}

/**
 * 创建申诉
 * @param {Object} data - 申诉数据
 */
export function createAppeal(data) {
  return request({
    url: '/salaries/appeals/',
    method: 'post',
    data
  })
}

/**
 * 审批申诉
 * @param {number} id - 申诉 ID
 * @param {Object} data - { approve, approval_remark, approver_id }
 */
export function approveAppeal(id, data) {
  return request({
    url: `/salaries/appeals/${id}/approve/`,
    method: 'post',
    data
  })
}

/**
 * 获取待审批申诉列表
 * @param {Object} params - 查询参数 { appeal_type }
 */
export function getPendingAppeals(params) {
  return request({
    url: '/salaries/appeals/pending/',
    method: 'get',
    params
  })
}

/**
 * 导出工资表（导出功能通常由后端生成文件，这里返回下载链接）
 * @param {Object} params - { year_month }
 */
export function exportSalarySheet(params) {
  return request({
    url: '/salaries/salaries/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 我的薪资记录（员工查询）
 * @param {Object} params - 查询参数
 * @param {number} params.employee_id - 员工ID
 * @param {string} params.year_month - 年月（可选）YYYY-MM
 * @returns {Promise}
 */
export function getMySalaries(params) {
  return request({
    url: '/salaries/salaries/my-salaries/',
    method: 'get',
    params
  })
}
