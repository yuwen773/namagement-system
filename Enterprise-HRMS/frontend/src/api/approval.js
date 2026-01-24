import axios from './axios'

/**
 * 审批管理 API
 */

// 获取申请列表
export function getApplicationList(params) {
  return axios.get('/approval/', { params })
}

// 获取申请详情
export function getApplicationDetail(id) {
  return axios.get(`/approval/${id}/`)
}

// 提交申请
export function submitApplication(data) {
  return axios.post('/approval/', data)
}

// 更新申请
export function updateApplication(id, data) {
  return axios.patch(`/approval/${id}/`, data)
}

// 删除申请
export function deleteApplication(id) {
  return axios.delete(`/approval/${id}/`)
}

// 获取待审批列表（HR/Admin）
export function getPendingApprovals(params) {
  return axios.get('/approval/pending/', { params })
}

// 审批通过
export function approveApplication(id, data) {
  return axios.post(`/approval/${id}/approve/`, data)
}

// 审批驳回
export function rejectApplication(id, data) {
  return axios.post(`/approval/${id}/reject/`, data)
}

// 申请类型常量
export const REQUEST_TYPE = {
  LEAVE: 'leave',
  OVERTIME: 'overtime'
}

// 请假类型常量
export const LEAVE_TYPE = {
  SICK: 'sick',
  PERSONAL: 'personal',
  ANNUAL: 'annual'
}

// 申请状态常量
export const STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected'
}

// 状态文本映射
export const STATUS_TEXT = {
  [STATUS.PENDING]: '待审批',
  [STATUS.APPROVED]: '已通过',
  [STATUS.REJECTED]: '已驳回'
}

// 状态类型映射（用于 Element Plus Tag）
export const STATUS_TYPE = {
  [STATUS.PENDING]: 'warning',
  [STATUS.APPROVED]: 'success',
  [STATUS.REJECTED]: 'danger'
}

// 类型文本映射
export const REQUEST_TYPE_TEXT = {
  [REQUEST_TYPE.LEAVE]: '请假',
  [REQUEST_TYPE.OVERTIME]: '加班'
}

// 请假类型文本映射
export const LEAVE_TYPE_TEXT = {
  [LEAVE_TYPE.SICK]: '病假',
  [LEAVE_TYPE.PERSONAL]: '事假',
  [LEAVE_TYPE.ANNUAL]: '年假'
}
