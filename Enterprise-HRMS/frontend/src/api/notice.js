import axios from './axios'

// 公告 API 封装

/**
 * 获取公告列表（所有认证用户可访问公开列表）
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 */
export function getPublicNoticeList(params) {
  return axios.get('/notice/public/', { params })
}

/**
 * 获取公告详情（所有认证用户可访问公开详情）
 * @param {number} id - 公告ID
 */
export function getPublicNoticeDetail(id) {
  return axios.get(`/notice/public/${id}/`)
}

/**
 * 获取公告管理列表（仅管理员）
 * @param {Object} params - 查询参数
 * @param {string} params.is_published - 筛选发布状态
 * @param {string} params.is_pinned - 筛选置顶状态
 */
export function getNoticeList(params) {
  return axios.get('/notice/notices/', { params })
}

/**
 * 获取公告详情（仅管理员）
 * @param {number} id - 公告ID
 */
export function getNoticeDetail(id) {
  return axios.get(`/notice/notices/${id}/`)
}

/**
 * 创建公告（仅管理员）
 * @param {Object} data - 公告数据
 * @param {string} data.title - 公告标题
 * @param {string} data.content - 公告内容
 * @param {boolean} data.is_pinned - 是否置顶
 * @param {boolean} data.is_published - 是否发布
 */
export function createNotice(data) {
  return axios.post('/notice/notices/', data)
}

/**
 * 更新公告（仅管理员）
 * @param {number} id - 公告ID
 * @param {Object} data - 更新数据
 */
export function updateNotice(id, data) {
  return axios.put(`/notice/notices/${id}/`, data)
}

/**
 * 删除公告（仅管理员）
 * @param {number} id - 公告ID
 */
export function deleteNotice(id) {
  return axios.delete(`/notice/notices/${id}/`)
}

/**
 * 发布公告（仅管理员）
 * @param {number} id - 公告ID
 */
export function publishNotice(id) {
  return axios.post(`/notice/notices/${id}/publish/`)
}

/**
 * 撤回公告（仅管理员）
 * @param {number} id - 公告ID
 */
export function unpublishNotice(id) {
  return axios.post(`/notice/notices/${id}/unpublish/`)
}

/**
 * 置顶/取消置顶公告（仅管理员）
 * @param {number} id - 公告ID
 * @param {boolean} is_pinned - 是否置顶
 */
export function togglePinned(id, is_pinned) {
  return axios.put(`/notice/notices/${id}/`, { is_pinned })
}

// 公告状态常量
export const NOTICE_STATUS = {
  DRAFT: 'draft',
  PUBLISHED: 'published'
}

// 公告置顶常量
export const NOTICE_PINNED = {
  NORMAL: false,
  PINNED: true
}

/**
 * 获取最新公告列表
 * @param {number} limit - 获取数量，默认5
 */
export function getLatestNotices(limit = 5) {
  return axios.get('/notice/public/latest/', { params: { limit } })
}
