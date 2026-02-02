/**
 * API 错误处理工具
 *
 * 统一处理后端返回的错误信息，提供简洁明确的错误提示
 */

// 错误类型分类：用户错误 vs 系统错误
const USER_ERROR_TYPES = [
  'validation_error',      // 参数验证失败
  'parameter_error',       // 参数错误
  'not_found',             // 资源不存在
  'resource_exists',       // 资源已存在
  'permission_denied',     // 权限不足
  'unauthorized',          // 未登录
  'token_expired',         // 登录过期
  'token_invalid',         // 无效令牌
  'state_not_allowed',     // 状态不允许
  'account_disabled',      // 账户禁用
  'account_banned',        // 账户封禁
  'file_too_large',        // 文件过大
  'invalid_file_type'      // 不支持的文件类型
]

const SERVER_ERROR_TYPES = [
  'database_error',        // 数据库错误
  'internal_error',        // 内部错误
  'server_error'           // 服务器错误
]

/**
 * 判断是否为用户错误（用户输入或操作导致）
 */
export function isUserError(errorData) {
  if (!errorData) return false
  const type = errorData.type || errorData.data?.type
  if (type) {
    return USER_ERROR_TYPES.includes(type)
  }
  // 没有 type 时，根据状态码判断
  const code = errorData.code || errorData.status
  if (code >= 400 && code < 500) return true
  return false
}

/**
 * 获取简洁的错误提示
 * @param {Object} error - axios 错误对象
 * @returns {Object} { message: string, isUserError: boolean }
 */
export function getErrorTip(error) {
  // 无响应（网络问题）
  if (!error.response) {
    return {
      message: '网络异常，请检查网络连接',
      isUserError: false
    }
  }

  const data = error.response.data || {}
  const code = data.code || error.response.status

  // 服务器错误 (500+)
  if (code >= 500 || SERVER_ERROR_TYPES.includes(data.type)) {
    return {
      message: '服务异常，请稍后重试',
      isUserError: false
    }
  }

  // 401 未登录/登录过期
  if (code === 401 || data.type === 'token_expired' || data.type === 'token_invalid') {
    return {
      message: '登录已过期，请重新登录',
      isUserError: true
    }
  }

  // 403 权限不足
  if (code === 403) {
    return {
      message: data.message || '权限不足',
      isUserError: true
    }
  }

  // 400 参数验证错误
  if (code === 400 || code === 4001 || data.type === 'validation_error') {
    // 如果有字段错误，取字段错误信息
    if (data.errors && typeof data.errors === 'object') {
      const firstError = Object.values(data.errors)[0]
      if (firstError && Array.isArray(firstError) && firstError[0]) {
        return {
          message: firstError[0],
          isUserError: true
        }
      }
    }
    return {
      message: data.message || '参数错误',
      isUserError: true
    }
  }

  // 404 资源不存在
  if (code === 404) {
    return {
      message: data.message || '内容不存在',
      isUserError: true
    }
  }

  // 其他业务错误，直接显示 message
  return {
    message: data.message || '操作失败',
    isUserError: true
  }
}

/**
 * 解析 API 错误响应（用于获取字段级错误）
 */
export function parseApiError(error) {
  const data = error.data || error.response?.data

  if (!data) {
    return {
      message: error.message || '网络请求失败',
      code: 'NETWORK_ERROR',
      fieldErrors: {}
    }
  }

  // 提取字段级错误
  const fieldErrors = {}
  if (data.errors && typeof data.errors === 'object') {
    for (const [field, errors] of Object.entries(data.errors)) {
      if (Array.isArray(errors) && errors[0]) {
        fieldErrors[field] = errors[0]
      } else if (typeof errors === 'string') {
        fieldErrors[field] = errors
      }
    }
  }

  return {
    message: data.message || '操作失败',
    code: data.code || error.response?.status,
    fieldErrors,
    originalData: data
  }
}

/**
 * 获取字段错误消息
 */
export function getFieldError(fieldErrors, fieldName) {
  return fieldErrors[fieldName] || null
}

export default {
  isUserError,
  getErrorTip,
  parseApiError,
  getFieldError
}
