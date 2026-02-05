import { get, post, put, patch, del } from '../request'

/**
 * 系统管理相关 API
 * 包含系统配置 (SystemConfig)、消息通知 (Message)、操作日志 (OperationLog)
 */

// ==================== 系统配置相关接口 ====================

/**
 * 获取系统配置列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 分类筛选 (basic/seo/trade/other)
 * @param {boolean} params.is_editable - 是否可编辑筛选
 * @param {string} params.ordering - 排序字段
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getConfigsListApi(params) {
  return get('/system/configs/', params)
}

/**
 * 获取配置详情
 * @param {string|number} id - 配置ID
 * @returns {Promise<Object>}
 */
export function getConfigDetailApi(id) {
  return get(`/system/configs/${id}/`)
}

/**
 * 创建系统配置
 * @param {Object} data - 配置数据
 * @param {string} data.key - 配置键（唯一）
 * @param {string} data.value - 配置值
 * @param {string} data.description - 配置描述
 * @param {string} data.category - 分类 (basic/seo/trade/other)
 * @param {boolean} data.is_editable - 是否可编辑
 * @returns {Promise<Object>}
 */
export function createConfigApi(data) {
  return post('/system/configs/', data)
}

/**
 * 更新系统配置
 * @param {string|number} id - 配置ID
 * @param {Object} data - 配置数据
 * @returns {Promise<Object>}
 */
export function updateConfigApi(id, data) {
  return put(`/system/configs/${id}/`, data)
}

/**
 * 部分更新系统配置
 * @param {string|number} id - 配置ID
 * @param {Object} data - 配置数据
 * @returns {Promise<Object>}
 */
export function patchConfigApi(id, data) {
  return patch(`/system/configs/${id}/`, data)
}

/**
 * 删除系统配置
 * @param {string|number} id - 配置ID
 * @returns {Promise<void>}
 */
export function deleteConfigApi(id) {
  return del(`/system/configs/${id}/`)
}

// ==================== 消息通知相关接口 ====================

/**
 * 获取消息列表
 * @param {Object} params - 查询参数
 * @param {string} params.ordering - 排序字段
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getMessagesListApi(params) {
  return get('/system/messages/', params)
}

/**
 * 获取我的消息列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getMyMessagesApi(params) {
  return get('/system/messages/my-messages/', params)
}

/**
 * 获取消息详情
 * @param {string|number} id - 消息ID
 * @returns {Promise<Object>}
 */
export function getMessageDetailApi(id) {
  return get(`/system/messages/${id}/`)
}

/**
 * 发送消息
 * @param {Object} data - 消息数据
 * @param {number} data.recipient - 接收用户ID（为空表示全员消息）
 * @param {string} data.title - 消息标题
 * @param {string} data.content - 消息内容
 * @param {string} data.message_type - 消息类型 (announcement/notification/promotion/system)
 * @returns {Promise<Object>}
 */
export function createMessageApi(data) {
  return post('/system/messages/', data)
}

/**
 * 更新消息
 * @param {string|number} id - 消息ID
 * @param {Object} data - 消息数据
 * @returns {Promise<Object>}
 */
export function updateMessageApi(id, data) {
  return put(`/system/messages/${id}/`, data)
}

/**
 * 部分更新消息
 * @param {string|number} id - 消息ID
 * @param {Object} data - 消息数据
 * @returns {Promise<Object>}
 */
export function patchMessageApi(id, data) {
  return patch(`/system/messages/${id}/`, data)
}

/**
 * 删除消息
 * @param {string|number} id - 消息ID
 * @returns {Promise<void>}
 */
export function deleteMessageApi(id) {
  return del(`/system/messages/${id}/`)
}

/**
 * 标记消息已读
 * @param {string|number} id - 消息ID
 * @returns {Promise<Object>}
 */
export function markMessageReadApi(id) {
  return post(`/system/messages/${id}/mark-read/`)
}

// ==================== 操作日志相关接口 ====================

/**
 * 获取操作日志列表
 * @param {Object} params - 查询参数
 * @param {string} params.action_type - 操作类型筛选 (create/update/delete/login/logout/other)
 * @param {string} params.object_type - 对象类型筛选
 * @param {string} params.status - 状态筛选 (success/failed)
 * @param {string} params.ordering - 排序字段
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getLogsListApi(params) {
  return get('/system/logs/', params)
}

/**
 * 获取日志详情
 * @param {string|number} id - 日志ID
 * @returns {Promise<Object>}
 */
export function getLogDetailApi(id) {
  return get(`/system/logs/${id}/`)
}

/**
 * 创建操作日志（仅管理员）
 * @param {Object} data - 日志数据
 * @returns {Promise<Object>}
 */
export function createLogApi(data) {
  return post('/system/logs/', data)
}

/**
 * 更新操作日志（仅管理员）
 * @param {string|number} id - 日志ID
 * @param {Object} data - 日志数据
 * @returns {Promise<Object>}
 */
export function updateLogApi(id, data) {
  return put(`/system/logs/${id}/`, data)
}

/**
 * 部分更新操作日志（仅管理员）
 * @param {string|number} id - 日志ID
 * @param {Object} data - 日志数据
 * @returns {Promise<Object>}
 */
export function patchLogApi(id, data) {
  return patch(`/system/logs/${id}/`, data)
}

/**
 * 删除操作日志（仅管理员）
 * @param {string|number} id - 日志ID
 * @returns {Promise<void>}
 */
export function deleteLogApi(id) {
  return del(`/system/logs/${id}/`)
}

// ==================== 工具函数 ====================

/**
 * 获取系统配置分类标签
 * @param {string} category - 分类值
 * @returns {string}
 */
export function getConfigCategoryLabel(category) {
  const categoryMap = {
    basic: '基础配置',
    seo: 'SEO配置',
    trade: '交易配置',
    other: '其他配置'
  }
  return categoryMap[category] || category
}

/**
 * 获取系统配置分类类型
 * @param {string} category - 分类值
 * @returns {string}
 */
export function getConfigCategoryType(category) {
  const typeMap = {
    basic: 'primary',
    seo: 'success',
    trade: 'warning',
    other: 'info'
  }
  return typeMap[category] || ''
}

/**
 * 获取消息类型标签
 * @param {string} type - 类型值
 * @returns {string}
 */
export function getMessageTypeLabel(type) {
  const typeMap = {
    announcement: '系统公告',
    notification: '订单通知',
    promotion: '促销通知',
    system: '系统通知'
  }
  return typeMap[type] || type
}

/**
 * 获取消息类型颜色
 * @param {string} type - 类型值
 * @returns {string}
 */
export function getMessageTypeColor(type) {
  const colorMap = {
    announcement: 'danger',
    notification: 'primary',
    promotion: 'warning',
    system: 'info'
  }
  return colorMap[type] || ''
}

/**
 * 获取消息状态标签
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getMessageStatusLabel(status) {
  const statusMap = {
    draft: '草稿',
    sent: '已发送',
    read: '已读'
  }
  return statusMap[status] || status
}

/**
 * 获取消息状态类型
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getMessageStatusType(status) {
  const typeMap = {
    draft: 'info',
    sent: 'warning',
    read: 'success'
  }
  return typeMap[status] || 'info'
}

/**
 * 获取操作类型标签
 * @param {string} action - 操作类型值
 * @returns {string}
 */
export function getLogActionLabel(action) {
  const actionMap = {
    create: '创建',
    update: '更新',
    delete: '删除',
    login: '登录',
    logout: '登出',
    other: '其他'
  }
  return actionMap[action] || action
}

/**
 * 获取操作类型颜色
 * @param {string} action - 操作类型值
 * @returns {string}
 */
export function getLogActionColor(action) {
  const colorMap = {
    create: 'success',
    update: 'primary',
    delete: 'danger',
    login: 'info',
    logout: 'warning',
    other: ''
  }
  return colorMap[action] || ''
}

/**
 * 获取操作状态标签
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getLogStatusLabel(status) {
  const statusMap = {
    success: '成功',
    failed: '失败'
  }
  return statusMap[status] || status
}

/**
 * 获取操作状态类型
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getLogStatusType(status) {
  const typeMap = {
    success: 'success',
    failed: 'danger'
  }
  return typeMap[status] || 'info'
}
