import axios from "./axios";

/**
 * 用户信息修改 API 封装
 */

// 获取当前用户信息
export function getCurrentUser() {
  return axios.get("/auth/me/");
}

// 修改申请相关 API（路径前缀是 /api/auth/）
export function getEditRequestList(params) {
  return axios.get("/auth/edit-requests/", { params });
}

export function getEditRequestDetail(id) {
  return axios.get(`/auth/edit-requests/${id}/`);
}

export function createEditRequest(data) {
  return axios.post("/auth/edit-requests/", data);
}

export function getPendingEditRequests() {
  return axios.get("/auth/edit-requests/pending/");
}

export function approveEditRequest(id, data) {
  return axios.post(`/auth/edit-requests/${id}/approve/`, data);
}

export function rejectEditRequest(id, data) {
  return axios.post(`/auth/edit-requests/${id}/reject/`, data);
}

// 修改类型常量
export const EDIT_TYPE = {
  PHONE: "phone",
  EMAIL: "email",
  EMERGENCY_CONTACT: "emergency_contact",
  ADDRESS: "address",
  ID_CARD: "id_card",
};

// 修改类型显示文本
export const EDIT_TYPE_TEXT = {
  phone: "手机号",
  email: "邮箱",
  emergency_contact: "紧急联系人",
  address: "通讯地址",
  id_card: "身份证号",
};

// 状态常量
export const STATUS = {
  PENDING: "pending",
  APPROVED: "approved",
  REJECTED: "rejected",
};

// 状态显示文本
export const STATUS_TEXT = {
  pending: "待审批",
  approved: "已通过",
  rejected: "已驳回",
};

// 状态类型（用于 Element Plus 标签）
export const STATUS_TYPE = {
  pending: "warning",
  approved: "success",
  rejected: "danger",
};

// 获取当前用户的员工档案（包含部门和岗位信息）
export function getMyEmployeeProfile() {
  return axios.get("/employee/me/");
}

// 获取部门树形结构
export function getDepartmentTree() {
  return axios.get("/organization/departments/tree/");
}

// 获取组织架构树（完整树，包括停用部门）
export function getOrganizationTree() {
  return axios.get("/organization/departments/", {
    params: { include_inactive: true }
  });
}

// 修改密码
export function changePassword(data) {
  return axios.post("/auth/change-password/", data);
}
