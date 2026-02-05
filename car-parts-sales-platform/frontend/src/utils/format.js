import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'
import duration from 'dayjs/plugin/duration'

dayjs.locale('zh-cn')
dayjs.extend(relativeTime)
dayjs.extend(duration)

/**
 * 格式化日期
 * @param {string|number|Date} date - 日期
 * @param {string} format - 格式，默认 'YYYY-MM-DD'
 * @returns {string}
 */
export function formatDate(date, format = 'YYYY-MM-DD') {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 格式化日期时间
 * @param {string|number|Date} date - 日期
 * @returns {string}
 */
export function formatDateTime(date) {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

/**
 * 格式化时间
 * @param {string|number|Date} date - 日期
 * @returns {string}
 */
export function formatTime(date) {
  if (!date) return '-'
  return dayjs(date).format('HH:mm:ss')
}

/**
 * 相对时间（多久之前）
 * @param {string|number|Date} date - 日期
 * @returns {string}
 */
export function fromNow(date) {
  if (!date) return '-'
  return dayjs(date).fromNow()
}

/**
 * 格式化相对时间（多久之前）- fromNow 的别名
 * @param {string|number|Date} date - 日期
 * @returns {string}
 */
export function formatRelativeTime(date) {
  return fromNow(date)
}

/**
 * 格式化金额
 * @param {number} amount - 金额
 * @param {number} decimals - 小数位数，默认 2
 * @returns {string}
 */
export function formatCurrency(amount, decimals = 2) {
  if (amount === null || amount === undefined) return '-'
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(amount)
}

/**
 * 格式化数字（千分位）
 * @param {number} num - 数字
 * @returns {string}
 */
export function formatNumber(num) {
  if (num === null || num === undefined) return '-'
  return new Intl.NumberFormat('zh-CN').format(num)
}

/**
 * 格式化百分比
 * @param {number} value - 数值
 * @param {number} total - 总数
 * @param {number} decimals - 小数位数
 * @returns {string}
 */
export function formatPercent(value, total, decimals = 1) {
  if (!total || total === 0) return '0%'
  const percent = (value / total) * 100
  return `${percent.toFixed(decimals)}%`
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

/**
 * 隐藏手机号中间四位
 * @param {string} phone - 手机号
 * @returns {string}
 */
export function maskPhone(phone) {
  if (!phone) return '-'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

/**
 * 获取订单状态标签
 * @param {string} status - 状态值
 * @returns {Object} { label, type }
 */
export function getOrderStatusInfo(status) {
  const { ORDER_STATUS_MAP } = require('./constants')
  return ORDER_STATUS_MAP[status] || { label: status, type: 'info' }
}

/**
 * 截断文本
 * @param {string} text - 文本
 * @param {number} length - 最大长度
 * @returns {string}
 */
export function truncateText(text, length = 50) {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}
