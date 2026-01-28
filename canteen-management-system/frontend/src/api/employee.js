/**
 * 员工档案管理 API
 */
import request from './request'

/**
 * 获取员工列表
 * @param {Object} params - 查询参数
 * @param {string} params.position - 岗位筛选
 * @param {string} params.status - 状态筛选
 * @param {string} params.search - 搜索关键字
 * @param {string} params.ordering - 排序字段
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise}
 */
export function getEmployeeList(params = {}) {
  return request({
    url: '/employees/',
    method: 'get',
    params
  })
}

/**
 * 获取员工详情
 * @param {number} id - 员工ID
 * @returns {Promise}
 */
export function getEmployeeDetail(id) {
  return request({
    url: `/employees/${id}/`,
    method: 'get'
  })
}

/**
 * 创建员工档案
 * @param {Object} data - 员工数据
 * @returns {Promise}
 */
export function createEmployee(data) {
  return request({
    url: '/employees/',
    method: 'post',
    data
  })
}

/**
 * 更新员工档案
 * @param {number} id - 员工ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateEmployee(id, data) {
  return request({
    url: `/employees/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新员工档案
 * @param {number} id - 员工ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function patchEmployee(id, data) {
  return request({
    url: `/employees/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除员工档案
 * @param {number} id - 员工ID
 * @returns {Promise}
 */
export function deleteEmployee(id) {
  return request({
    url: `/employees/${id}/`,
    method: 'delete'
  })
}
