import request from './request'

/**
 * 考勤管理 API
 */

/**
 * 获取考勤记录列表
 * @param {Object} params - 查询参数
 * @param {number} params.employee - 员工ID（可选）
 * @param {string} params.status - 考勤状态（可选）
 * @param {string} params.search - 搜索关键字（可选）
 * @param {string} params.ordering - 排序字段（可选）
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise}
 */
export function getAttendanceList(params) {
  return request({
    url: '/attendance/',
    method: 'get',
    params
  })
}

/**
 * 获取考勤记录详情
 * @param {number} id - 考勤记录ID
 * @returns {Promise}
 */
export function getAttendanceDetail(id) {
  return request({
    url: `/attendance/${id}/`,
    method: 'get'
  })
}

/**
 * 创建考勤记录（管理员手动创建）
 * @param {Object} data - 考勤记录数据
 * @returns {Promise}
 */
export function createAttendance(data) {
  return request({
    url: '/attendance/',
    method: 'post',
    data
  })
}

/**
 * 更新考勤记录
 * @param {number} id - 考勤记录ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateAttendance(id, data) {
  return request({
    url: `/attendance/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新考勤记录
 * @param {number} id - 考勤记录ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function patchAttendance(id, data) {
  return request({
    url: `/attendance/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除考勤记录
 * @param {number} id - 考勤记录ID
 * @returns {Promise}
 */
export function deleteAttendance(id) {
  return request({
    url: `/attendance/${id}/`,
    method: 'delete'
  })
}

/**
 * 员工签到
 * @param {Object} data - 签到数据
 * @param {number} data.employee_id - 员工ID
 * @param {number} data.schedule_id - 排班ID（可选）
 * @param {string} data.clock_in_location - 签到地点
 * @returns {Promise}
 */
export function clockIn(data) {
  return request({
    url: '/attendance/clock_in/',
    method: 'post',
    data
  })
}

/**
 * 员工签退
 * @param {Object} data - 签退数据
 * @param {number} data.employee_id - 员工ID
 * @param {string} data.clock_out_location - 签退地点
 * @returns {Promise}
 */
export function clockOut(data) {
  return request({
    url: '/attendance/clock_out/',
    method: 'post',
    data
  })
}

/**
 * 考勤统计
 * @param {Object} data - 统计参数
 * @param {string} data.start_date - 开始日期
 * @param {string} data.end_date - 结束日期
 * @param {number} data.employee_id - 员工ID（可选）
 * @returns {Promise}
 */
export function getAttendanceStatistics(data) {
  return request({
    url: '/attendance/statistics/',
    method: 'post',
    data
  })
}

/**
 * 异常处理（修改考勤状态）
 * @param {number} id - 考勤记录ID
 * @param {Object} data - 修改数据
 * @param {string} data.status - 新状态
 * @param {string} data.correction_remark - 修改备注（必填）
 * @returns {Promise}
 */
export function correctAttendance(id, data) {
  return request({
    url: `/attendance/${id}/correct/`,
    method: 'post',
    data
  })
}

/**
 * 我的考勤记录（员工查询）
 * @param {Object} params - 查询参数
 * @param {number} params.employee_id - 员工ID
 * @param {string} params.start_date - 开始日期（可选）
 * @param {string} params.end_date - 结束日期（可选）
 * @returns {Promise}
 */
export function getMyAttendance(params) {
  return request({
    url: '/attendance/my_attendance/',
    method: 'get',
    params
  })
}
