import axios from '@/api/axios'

/**
 * 员工管理 API
 */

/**
 * 获取员工列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.status - 状态筛选 (active/pending/resigned)
 * @param {number} params.department_id - 按部门筛选
 * @param {number} params.post_id - 按岗位筛选
 * @param {string} params.keyword - 按姓名/工号模糊搜索
 * @returns {Promise}
 */
export function getEmployeeList(params) {
  return axios.get('/employee/', { params })
}

/**
 * 获取员工详情
 * @param {number} id - 员工ID
 * @returns {Promise}
 */
export function getEmployeeDetail(id) {
  return axios.get(`/employee/${id}/`)
}

/**
 * 获取待入职用户列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.keyword - 按姓名/用户名搜索
 * @returns {Promise}
 */
export function getPendingUsers(params) {
  return axios.get('/employee/pending/', { params })
}

/**
 * 创建员工档案（入职办理）
 * @param {Object} data - 员工数据
 * @param {number} data.user_id - 用户ID
 * @param {string} data.emp_no - 员工编号
 * @param {number} data.department_id - 部门ID
 * @param {number} data.post_id - 岗位ID
 * @param {string} data.hire_date - 入职日期 (YYYY-MM-DD)
 * @param {number} data.salary_base - 基本工资
 * @returns {Promise}
 */
export function createEmployee(data) {
  return axios.post('/employee/', data)
}

/**
 * 更新员工档案
 * @param {number} id - 员工ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateEmployee(id, data) {
  return axios.put(`/employee/${id}/`, data)
}

/**
 * 员工离职办理
 * @param {number} id - 员工ID
 * @param {Object} data - 离职数据
 * @param {string} data.resigned_date - 离职日期 (YYYY-MM-DD)
 * @param {string} [data.resigned_reason] - 离职原因
 * @returns {Promise}
 */
export function resignEmployee(id, data) {
  return axios.post(`/employee/${id}/resign/`, data)
}

/**
 * 获取员工列表（用于选择器）
 * @param {Object} params - 查询参数
 * @param {string} params.status - 状态筛选，默认 active
 * @param {number} params.page_size - 每页数量，默认 100
 * @returns {Promise}
 */
export function getEmployeeOptions(params) {
  return axios.get('/employee/', {
    params: {
      ...params,
      status: params.status || 'active',
      page_size: params.page_size || 100
    }
  })
}

/**
 * 获取当前用户的员工档案
 * @returns {Promise}
 */
export function getMyProfile() {
  return axios.get('/employee/me/')
}

export default {
  getEmployeeList,
  getEmployeeDetail,
  getPendingUsers,
  createEmployee,
  updateEmployee,
  resignEmployee,
  getEmployeeOptions,
  getMyProfile
}
