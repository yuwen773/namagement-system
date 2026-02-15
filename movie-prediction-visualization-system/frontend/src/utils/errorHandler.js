/**
 * 统一错误处理工具
 *
 * 功能：
 * - 解析后端错误响应，提取字段级错误信息
 * - 根据错误类型生成用户友好的提示信息
 * - 提供统一的错误展示方法
 */

import { ElMessage, ElMessageBox } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/stores/user'

/**
 * HTTP 状态码对应的用户友好提示
 */
const HTTP_ERROR_MESSAGES = {
  400: '请求参数错误，请检查输入信息',
  401: '登录已过期，请重新登录',
  403: '抱歉，您没有权限执行此操作',
  404: '请求的资源不存在',
  405: '请求方法不允许',
  429: '请求过于频繁，请稍后重试',
  500: '服务器遇到问题，请稍后重试',
  502: '网关错误，请稍后重试',
  503: '服务暂时不可用，请稍后重试',
  504: '请求超时，请稍后重试'
}

/**
 * 常见业务错误的友好提示映射
 * 用于将后端返回的 message 转换为更友好的提示
 */
const BUSINESS_ERROR_MESSAGES = {
  // 登录相关
  '登录失败': '用户名或密码不正确，请检查后重试',
  '用户名或密码错误': '用户名或密码不正确，请检查后重试',
  '用户已被禁用': '该账号已被禁用，请联系管理员',

  // 注册相关
  '注册失败': '注册失败，请检查输入信息',
  '用户名已存在': '该用户名已被占用，请更换用户名',
  '邮箱已存在': '该邮箱已被注册，请直接登录',

  // 通用操作
  '操作失败': '操作失败，请检查输入信息',
  '信息更新失败': '信息更新失败，请检查输入信息',
  '密码修改失败': '密码修改失败，请检查原密码是否正确',
  '原密码错误': '原密码不正确，请重新输入',

  // 影片相关
  '影片创建失败': '影片创建失败，请检查输入信息',
  '影片更新失败': '影片更新失败，请检查输入信息',
  '影片删除失败': '影片删除失败',
  '影片名称已存在': '影片名称已存在，请使用其他名称',
  '记录日期不能早于影片上映日期': '票房记录日期不能早于影片上映日期',
  '票房金额必须大于0': '票房金额必须大于0',
  '片长必须在1-1000分钟之间': '片长必须在1-1000分钟之间',
  '上映日期不能早于今天': '上映日期不能早于今天',
  '海报URL格式不正确': '海报链接格式不正确，请输入有效的URL',

  // 影院相关
  '影院创建失败': '影院创建失败，请检查输入信息',
  '影院更新失败': '影院更新失败，请检查输入信息',
  '影院删除失败': '影院删除失败',
  '屏幕数量必须大于0': '屏幕数量必须大于0',
  '座位数量必须大于0': '座位数量必须大于0',

  // 地域相关
  '地域创建失败': '地域创建失败，请检查输入信息',
  '地域更新失败': '地域更新失败，请检查输入信息',
  '地域删除失败': '地域删除失败',
  '省份不能有父级地域': '省份不能选择父级地域',
  '城市必须选择父级省份': '城市必须选择所属省份',
  '父级地域必须是省份': '父级地域必须是省份级别',
  '无法删除，该地域下存在子地域': '无法删除，该地域下存在子地域',
  '无法删除，该地域下存在关联的影院': '无法删除，该地域下存在关联的影院',

  // 票房相关
  '票房录入失败': '票房录入失败，请检查输入信息',
  '票房更新失败': '票房更新失败，请检查输入信息',
  '票房删除失败': '票房删除失败',

  // 用户管理
  '用户创建失败': '用户创建失败，请检查输入信息',
  '用户更新失败': '用户更新失败，请检查输入信息',
  '用户删除失败': '用户删除失败',
  '不能删除当前登录的管理员账户': '不能删除当前登录的管理员账户',
  '角色必须是 ADMIN 或 USER': '角色必须是 ADMIN 或 USER',

  // 删除限制
  '该类型下存在影片，无法删除': '该类型下存在影片，无法删除',
  '该影院存在关联的票房记录': '该影院存在关联的票房记录，无法删除',
  '影片《{title}》存在票房记录，无法删除': '该影片存在票房记录，无法删除',

  // 网络相关
  '网络请求失败，请检查网络连接': '网络连接失败，请检查您的网络',
  '请求超时': '请求超时，请稍后重试',
  '请求配置错误': '请求配置错误，请刷新页面重试'
}

/**
 * 解析后端错误响应，提取用户友好的错误信息
 *
 * @param {Error} error - 错误对象
 * @param {Object} error.response - Axios 响应对象
 * @param {Object} error.response.data - 响应数据
 * @param {number} error.response.status - HTTP 状态码
 * @param {string} error.response.data.message - 后端返回的错误消息
 * @param {Object} error.response.data.errors - 字段级错误对象
 * @returns {string} 用户友好的错误信息
 */
export function parseErrorMessage(error) {
  // 网络错误
  if (!error.response) {
    if (error.request) {
      return { message: '网络连接失败，请检查您的网络', type: 'network' }
    }
    return { message: '请求配置错误，请刷新页面重试', type: 'config' }
  }

  const { status, data } = error.response

  // 后端返回的错误数据 - 优先检查，因为包含更详细的错误信息
  if (data) {
    // 优先检查字段级错误
    if (data.errors) {
      const fieldError = extractFieldError(data.errors)
      if (fieldError) {
        return { message: fieldError, type: 'field', field: Object.keys(data.errors)[0] }
      }
    }

    // 检查业务错误消息
    if (data.message) {
      // 使用映射表转换
      if (BUSINESS_ERROR_MESSAGES[data.message]) {
        return { message: BUSINESS_ERROR_MESSAGES[data.message], type: 'business' }
      }

      // 支持动态消息（如包含变量）
      const dynamicMessage = matchDynamicMessage(data.message)
      if (dynamicMessage) {
        return { message: dynamicMessage, type: 'business' }
      }
    }
  }

  // HTTP 状态码错误 - 没有详细错误信息时使用
  if (HTTP_ERROR_MESSAGES[status]) {
    return {
      message: HTTP_ERROR_MESSAGES[status],
      type: status === 401 ? 'auth' : 'http',
      code: status
    }
  }

  // 默认错误信息
  return { message: '操作失败，请稍后重试', type: 'unknown' }
}

/**
 * 从字段错误对象中提取第一个错误信息
 *
 * @param {Object} errors - 字段错误对象
 * @returns {string|null} 错误信息或 null
 *
 * @example
 * extractFieldError({ title: ['影片名称已存在'], release_date: ['不能早于今天'] })
 * // 返回: '影片名称已存在'
 */
export function extractFieldError(errors) {
  if (!errors || typeof errors !== 'object') {
    return null
  }

  // 获取第一个字段的错误
  for (const field in errors) {
    const fieldErrors = errors[field]
    if (Array.isArray(fieldErrors) && fieldErrors.length > 0) {
      // 检查是否需要映射
      const firstError = fieldErrors[0]
      if (BUSINESS_ERROR_MESSAGES[firstError]) {
        return BUSINESS_ERROR_MESSAGES[firstError]
      }
      return firstError
    }
    // 处理非数组格式的错误
    if (typeof fieldErrors === 'string') {
      if (BUSINESS_ERROR_MESSAGES[fieldErrors]) {
        return BUSINESS_ERROR_MESSAGES[fieldErrors]
      }
      return fieldErrors
    }
  }

  return null
}

/**
 * 匹配并转换动态错误消息（包含变量）
 *
 * @param {string} message - 原始错误消息
 * @returns {string|null} 转换后的消息或 null
 */
function matchDynamicMessage(message) {
  // 影片相关动态消息
  if (message.includes('存在票房记录，无法删除')) {
    return '该影片存在票房记录，无法删除'
  }

  // 用户相关动态消息
  if (message.includes('已禁用') || message.includes('已启用')) {
    return message // 保持原样
  }

  // 密码重置相关
  if (message.includes('密码已重置')) {
    return message // 保持原样
  }

  // 角色更新相关
  if (message.includes('角色已更新')) {
    return message // 保持原样
  }

  return null
}

/**
 * 显示错误提示
 *
 * @param {Error|string} error - 错误对象或错误消息
 * @param {Object} options - 选项
 * @param {number} options.duration - 显示时长（毫秒）
 * @param {boolean} options.showMessageBox - 是否使用确认框（默认 false）
 */
export function showError(error, options = {}) {
  const { duration = 3000, showMessageBox = false } = options

  let errorMessage = ''
  let errorType = 'unknown'

  if (typeof error === 'string') {
    errorMessage = error
    errorType = 'manual'
  } else if (error instanceof Error) {
    const parsed = parseErrorMessage(error)
    errorMessage = parsed.message
    errorType = parsed.type
  } else {
    errorMessage = '未知错误'
  }

  // 401 错误特殊处理：显示确认框并跳转登录
  if (errorType === 'auth' || errorType === 'http') {
    // 检查是否已在显示确认框（避免多个401同时弹出）
    if (!window.isShowing401Dialog) {
      window.isShowing401Dialog = true
      ElMessageBox.confirm(
        '登录已过期，请重新登录',
        '提示',
        {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        // 清除状态
        const userStore = useUserStore()
        userStore.token = ''
        userStore.user = null

        // 清除本地存储
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')

        // 跳转到登录页
        router.push('/login')
      }).catch(() => {
        // 用户取消
      }).finally(() => {
        window.isShowing401Dialog = false
      })
    }
    return
  }

  // 其他错误使用 Message 提示
  ElMessage.error({
    message: errorMessage,
    duration
  })
}

/**
 * 显示成功提示
 *
 * @param {string} message - 成功消息
 * @param {Object} options - 选项
 * @param {number} options.duration - 显示时长（毫秒）
 */
export function showSuccess(message, options = {}) {
  const { duration = 2000 } = options

  ElMessage.success({
    message,
    duration
  })
}

/**
 * 显示警告提示
 *
 * @param {string} message - 警告消息
 * @param {Object} options - 选项
 * @param {number} options.duration - 显示时长（毫秒）
 */
export function showWarning(message, options = {}) {
  const { duration = 3000 } = options

  ElMessage.warning({
    message,
    duration
  })
}

/**
 * 显示信息提示
 *
 * @param {string} message - 信息消息
 * @param {Object} options - 选项
 * @param {number} options.duration - 显示时长（毫秒）
 */
export function showInfo(message, options = {}) {
  const { duration = 3000 } = options

  ElMessage.info({
    message,
    duration
  })
}

export default {
  parseErrorMessage,
  extractFieldError,
  showError,
  showSuccess,
  showWarning,
  showInfo
}
