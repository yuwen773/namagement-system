/**
 * 日期时间格式化工具函数
 */

/**
 * 格式化日期时间为中文格式
 * @param {string|Date} dateTime - 日期时间字符串或 Date 对象
 * @param {string} format - 输出格式: 'datetime' (完整), 'date' (仅日期), 'time' (仅时间)
 * @returns {string} 格式化后的日期时间字符串
 */
export function formatDateTime(dateTime, format = 'datetime') {
  if (!dateTime) return '-'

  const date = new Date(dateTime)
  if (isNaN(date.getTime())) return '-'

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  switch (format) {
    case 'date':
      return `${year}-${month}-${day}`
    case 'time':
      return `${hours}:${minutes}:${seconds}`
    case 'datetime':
    default:
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  }
}

/**
 * 格式化日期为简短格式（用于列表展示）
 * @param {string|Date} dateTime - 日期时间字符串或 Date 对象
 * @returns {string} 格式化后的日期字符串
 */
export function formatDateShort(dateTime) {
  if (!dateTime) return '-'

  const date = new Date(dateTime)
  if (isNaN(date.getTime())) return '-'

  const now = new Date()
  const diff = now - date

  // 小于 1 分钟
  if (diff < 60 * 1000) {
    return '刚刚'
  }

  // 小于 1 小时
  if (diff < 60 * 60 * 1000) {
    const minutes = Math.floor(diff / (60 * 1000))
    return `${minutes} 分钟前`
  }

  // 小于 24 小时
  if (diff < 24 * 60 * 60 * 1000) {
    const hours = Math.floor(diff / (60 * 60 * 1000))
    return `${hours} 小时前`
  }

  // 小于 7 天
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days} 天前`
  }

  // 正常日期格式
  return formatDateTime(dateTime, 'date')
}

/**
 * 格式化金额
 * @param {number} amount - 金额
 * @param {boolean} showSymbol - 是否显示货币符号
 * @returns {string} 格式化后的金额字符串
 */
export function formatCurrency(amount, showSymbol = true) {
  if (amount === null || amount === undefined) return '-'

  const formatted = Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })

  return showSymbol ? `¥${formatted}` : formatted
}

/**
 * 格式化手机号（隐藏中间四位）
 * @param {string} phone - 手机号
 * @returns {string} 格式化后的手机号
 */
export function formatPhone(phone) {
  if (!phone || phone.length !== 11) return phone
  return `${phone.substring(0, 3)}****${phone.substring(7)}`
}

/**
 * 格式化员工姓名（隐藏中间字符）
 * @param {string} name - 姓名
 * @returns {string} 格式化后的姓名
 */
export function formatName(name) {
  if (!name || name.length < 2) return name
  if (name.length === 2) {
    return `${name.charAt(0)}*`
  }
  return `${name.charAt(0)}*${name.charAt(name.length - 1)}`
}

/**
 * 格式化百分比
 * @param {number} value - 值（0-1 之间的小数或 0-100 的数字）
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的百分比字符串
 */
export function formatPercent(value, decimals = 1) {
  if (value === null || value === undefined) return '-'

  // 如果值大于 1，假设是百分比值（如 50 表示 50%）
  const percent = value > 1 ? value : value * 100

  return `${percent.toFixed(decimals)}%`
}
