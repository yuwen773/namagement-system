/**
 * 验证工具函数
 */

/**
 * 验证手机号
 * @param {string} phone - 手机号
 * @returns {boolean}
 */
export function isValidPhone(phone) {
  return /^1[3-9]\d{9}$/.test(phone)
}

/**
 * 验证邮箱
 * @param {string} email - 邮箱
 * @returns {boolean}
 */
export function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

/**
 * 验证密码强度（6-20位，包含字母和数字）
 * @param {string} password - 密码
 * @returns {boolean}
 */
export function isValidPassword(password) {
  return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,20}$/.test(password)
}

/**
 * 验证身份证号
 * @param {string} idCard - 身份证号
 * @returns {boolean}
 */
export function isValidIdCard(idCard) {
  return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(idCard)
}

/**
 * 验证URL
 * @param {string} url - URL
 * @returns {boolean}
 */
export function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * 验证金额
 * @param {number|string} amount - 金额
 * @returns {boolean}
 */
export function isValidAmount(amount) {
  return /^\d+(\.\d{1,2})?$/.test(String(amount))
}

/**
 * 验证正整数
 * @param {number|string} num - 数字
 * @returns {boolean}
 */
export function isPositiveInteger(num) {
  return /^\d+$/.test(String(num)) && Number(num) > 0
}
