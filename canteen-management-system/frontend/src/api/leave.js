import request from './request'

/**
 * 获取请假申请列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.employee - 员工ID筛选
 * @param {string} params.leave_type - 请假类型筛选 (SICK/PERSONAL/COMPENSATORY)
 * @param {string} params.status - 状态筛选 (PENDING/APPROVED/REJECTED)
 * @param {string} params.search - 搜索关键词（姓名、电话、原因）
 * @param {string} params.ordering - 排序字段
 * @returns {Promise}
 */
export function getLeaveList(params) {
  return request({
    url: '/leaves/',
    method: 'get',
    params
  })
}

/**
 * 获取请假申请详情
 * @param {number} id - 请假申请ID
 * @returns {Promise}
 */
export function getLeaveDetail(id) {
  return request({
    url: `/leaves/${id}/`,
    method: 'get'
  })
}

/**
 * 创建请假申请
 * @param {Object} data - 请假数据
 * @returns {Promise}
 */
export function createLeave(data) {
  return request({
    url: '/leaves/',
    method: 'post',
    data
  })
}

/**
 * 更新请假申请
 * @param {number} id - 请假申请ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateLeave(id, data) {
  return request({
    url: `/leaves/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新请假申请
 * @param {number} id - 请假申请ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function patchLeave(id, data) {
  return request({
    url: `/leaves/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除请假申请
 * @param {number} id - 请假申请ID
 * @returns {Promise}
 */
export function deleteLeave(id) {
  return request({
    url: `/leaves/${id}/`,
    method: 'delete'
  })
}

/**
 * 查询我的请假申请
 * @param {Object} params - 查询参数
 * @param {number} params.employee_id - 员工ID
 * @param {string} params.status - 状态筛选
 * @returns {Promise}
 */
export function getMyLeaves(params) {
  return request({
    url: '/leaves/my-requests/',
    method: 'get',
    params
  })
}

/**
 * 获取待审批列表
 * @returns {Promise}
 */
export function getPendingLeaves() {
  return request({
    url: '/leaves/pending/',
    method: 'get'
  })
}

/**
 * 审批请假申请
 * @param {number} id - 请假申请ID
 * @param {Object} data - 审批数据
 * @param {string} data.approval_status - 审批状态 (APPROVED/REJECTED)
 * @param {string} data.approval_remark - 审批意见
 * @returns {Promise}
 */
export function approveLeave(id, data) {
  return request({
    url: `/leaves/${id}/approve/`,
    method: 'post',
    data
  })
}
