/**
 * 日期格式化工具函数
 */

/**
 * 格式化日期
 * @param {string|Date} date - 日期字符串或 Date 对象
 * @param {string} format - 格式化模板，默认为 'YYYY-MM-DD HH:mm'
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm') {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化日期为相对时间（如：刚刚、5分钟前、3小时前）
 * @param {string|Date} date - 日期字符串或 Date 对象
 * @returns {string} 相对时间字符串
 */
export function formatRelativeTime(date) {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const now = new Date()
  const diff = now - d
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return formatDate(date, 'YYYY-MM-DD')
}

/**
 * 格式化日期为简短格式（用于评论列表）
 * @param {string|Date} date - 日期字符串或 Date 对象
 * @returns {string} 短日期字符串
 */
export function formatShortDate(date) {
  return formatDate(date, 'YYYY-MM-DD')
}

export default {
  formatDate,
  formatRelativeTime,
  formatShortDate
}
