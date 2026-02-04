/**
 * 本地存储工具函数
 */

/**
 * 设置 localStorage
 * @param {string} key - 键名
 * @param {any} value - 值
 */
export function setStorage(key, value) {
  try {
    const data = JSON.stringify(value)
    localStorage.setItem(key, data)
  } catch (error) {
    console.error('setStorage error:', error)
  }
}

/**
 * 获取 localStorage
 * @param {string} key - 键名
 * @param {any} defaultValue - 默认值
 * @returns {any}
 */
export function getStorage(key, defaultValue = null) {
  try {
    const data = localStorage.getItem(key)
    return data ? JSON.parse(data) : defaultValue
  } catch (error) {
    console.error('getStorage error:', error)
    return defaultValue
  }
}

/**
 * 删除 localStorage
 * @param {string} key - 键名
 */
export function removeStorage(key) {
  localStorage.removeItem(key)
}

/**
 * 清空 localStorage
 */
export function clearStorage() {
  localStorage.clear()
}

/**
 * 设置 sessionStorage
 * @param {string} key - 键名
 * @param {any} value - 值
 */
export function setSession(key, value) {
  try {
    const data = JSON.stringify(value)
    sessionStorage.setItem(key, data)
  } catch (error) {
    console.error('setSession error:', error)
  }
}

/**
 * 获取 sessionStorage
 * @param {string} key - 键名
 * @param {any} defaultValue - 默认值
 * @returns {any}
 */
export function getSession(key, defaultValue = null) {
  try {
    const data = sessionStorage.getItem(key)
    return data ? JSON.parse(data) : defaultValue
  } catch (error) {
    console.error('getSession error:', error)
    return defaultValue
  }
}

/**
 * 删除 sessionStorage
 * @param {string} key - 键名
 */
export function removeSession(key) {
  sessionStorage.removeItem(key)
}
