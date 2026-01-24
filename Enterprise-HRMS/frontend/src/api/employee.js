import axios from '@/api/axios'

/**
 * 获取员工列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 状态筛选 (active/pending/resigned)
 * @returns {Promise} 员工列表
 */
export function getEmployeeList(params) {
  return axios.get('/employee/', { params })
}

/**
 * 获取员工详情
 * @param {number} id - 员工ID
 * @returns {Promise} 员工详情
 */
export function getEmployeeDetail(id) {
  return axios.get(`/employee/${id}/`)
}

/**
 * 获取待入职用户列表
 * @returns {Promise} 待入职用户列表
 */
export function getPendingUsers() {
  return axios.get('/employee/pending/')
}

/**
 * 创建员工档案（入职办理）
 * @param {Object} data - 员工数据
 * @returns {Promise} 创建结果
 */
export function createEmployee(data) {
  return axios.post('/employee/', data)
}
