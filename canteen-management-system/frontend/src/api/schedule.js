/**
 * 排班管理 API
 * 包含班次定义、排班计划、调班申请相关接口
 */
import request from './request'

// ==================== 班次定义 ====================

/**
 * 获取班次列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getShiftList(params) {
  return request({
    url: '/schedules/shifts/',
    method: 'get',
    params
  })
}

/**
 * 获取班次详情
 * @param {number} id - 班次ID
 * @returns {Promise}
 */
export function getShiftDetail(id) {
  return request({
    url: `/schedules/shifts/${id}/`,
    method: 'get'
  })
}

/**
 * 创建班次
 * @param {Object} data - 班次数据
 * @returns {Promise}
 */
export function createShift(data) {
  return request({
    url: '/schedules/shifts/',
    method: 'post',
    data
  })
}

/**
 * 更新班次
 * @param {number} id - 班次ID
 * @param {Object} data - 班次数据
 * @returns {Promise}
 */
export function updateShift(id, data) {
  return request({
    url: `/schedules/shifts/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新班次
 * @param {number} id - 班次ID
 * @param {Object} data - 班次数据
 * @returns {Promise}
 */
export function patchShift(id, data) {
  return request({
    url: `/schedules/shifts/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除班次
 * @param {number} id - 班次ID
 * @returns {Promise}
 */
export function deleteShift(id) {
  return request({
    url: `/schedules/shifts/${id}/`,
    method: 'delete'
  })
}

// ==================== 排班计划 ====================

/**
 * 获取排班列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getScheduleList(params) {
  return request({
    url: '/schedules/schedules/',
    method: 'get',
    params
  })
}

/**
 * 获取排班详情
 * @param {number} id - 排班ID
 * @returns {Promise}
 */
export function getScheduleDetail(id) {
  return request({
    url: `/schedules/schedules/${id}/`,
    method: 'get'
  })
}

/**
 * 创建排班
 * @param {Object} data - 排班数据
 * @returns {Promise}
 */
export function createSchedule(data) {
  return request({
    url: '/schedules/schedules/',
    method: 'post',
    data
  })
}

/**
 * 更新排班
 * @param {number} id - 排班ID
 * @param {Object} data - 排班数据
 * @returns {Promise}
 */
export function updateSchedule(id, data) {
  return request({
    url: `/schedules/schedules/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新排班
 * @param {number} id - 排班ID
 * @param {Object} data - 排班数据
 * @returns {Promise}
 */
export function patchSchedule(id, data) {
  return request({
    url: `/schedules/schedules/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除排班
 * @param {number} id - 排班ID
 * @returns {Promise}
 */
export function deleteSchedule(id) {
  return request({
    url: `/schedules/schedules/${id}/`,
    method: 'delete'
  })
}

/**
 * 批量创建排班
 * @param {Object} data - 批量排班数据
 * @param {number[]} data.employee_ids - 员工ID列表
 * @param {number} data.shift_id - 班次ID
 * @param {string} data.start_date - 开始日期
 * @param {string} data.end_date - 结束日期
 * @returns {Promise}
 */
export function batchCreateSchedule(data) {
  return request({
    url: '/schedules/schedules/batch_create/',
    method: 'post',
    data
  })
}

/**
 * 获取日历视图数据
 * @param {Object} data - 日期范围数据
 * @param {string} data.start_date - 开始日期
 * @param {string} data.end_date - 结束日期
 * @param {number} data.employee_id - 员工ID（可选）
 * @returns {Promise}
 */
export function getCalendarView(data) {
  return request({
    url: '/schedules/schedules/calendar_view/',
    method: 'post',
    data
  })
}

// ==================== 调班申请 ====================

/**
 * 获取调班申请列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getShiftRequestList(params) {
  return request({
    url: '/schedules/shift-requests/',
    method: 'get',
    params
  })
}

/**
 * 获取调班申请详情
 * @param {number} id - 申请ID
 * @returns {Promise}
 */
export function getShiftRequestDetail(id) {
  return request({
    url: `/schedules/shift-requests/${id}/`,
    method: 'get'
  })
}

/**
 * 创建调班申请
 * @param {Object} data - 调班申请数据
 * @returns {Promise}
 */
export function createShiftRequest(data) {
  return request({
    url: '/schedules/shift-requests/',
    method: 'post',
    data
  })
}

/**
 * 更新调班申请
 * @param {number} id - 申请ID
 * @param {Object} data - 调班申请数据
 * @returns {Promise}
 */
export function updateShiftRequest(id, data) {
  return request({
    url: `/schedules/shift-requests/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新调班申请
 * @param {number} id - 申请ID
 * @param {Object} data - 调班申请数据
 * @returns {Promise}
 */
export function patchShiftRequest(id, data) {
  return request({
    url: `/schedules/shift-requests/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除调班申请
 * @param {number} id - 申请ID
 * @returns {Promise}
 */
export function deleteShiftRequest(id) {
  return request({
    url: `/schedules/shift-requests/${id}/`,
    method: 'delete'
  })
}

/**
 * 调班审批
 * @param {number} id - 申请ID
 * @param {Object} data - 审批数据
 * @param {boolean} data.approve - 是否批准
 * @param {string} data.approval_remark - 审批意见
 * @param {number} data.approver_id - 审批人ID
 * @returns {Promise}
 */
export function approveShiftRequest(id, data) {
  return request({
    url: `/schedules/shift-requests/${id}/approve/`,
    method: 'post',
    data
  })
}

/**
 * 获取我的调班申请
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getMyShiftRequests(params) {
  return request({
    url: '/schedules/shift-requests/my_requests/',
    method: 'get',
    params
  })
}

/**
 * 获取待审批调班申请列表
 * @returns {Promise}
 */
export function getPendingShiftRequests() {
  return request({
    url: '/schedules/shift-requests/pending/',
    method: 'get'
  })
}
