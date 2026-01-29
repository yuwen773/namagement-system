import { ElLoading } from 'element-plus'

/**
 * 全局 Loading 服务
 * 使用计数器管理多个并发请求，确保只有在所有请求完成后才关闭 Loading
 */

let loadingInstance = null
let loadingCount = 0

/**
 * 显示 Loading
 * @param {string} message - Loading 提示文字
 */
export const showLoading = (message = '加载中...') => {
  if (loadingCount === 0) {
    loadingInstance = ElLoading.service({
      lock: true,
      text: message,
      background: 'rgba(0, 0, 0, 0.7)',
      customClass: 'canteen-loading'
    })
  }
  loadingCount++
}

/**
 * 隐藏 Loading
 * 只有当计数器归零时才真正关闭 Loading
 */
export const hideLoading = () => {
  loadingCount--
  if (loadingCount === 0 && loadingInstance) {
    loadingInstance.close()
    loadingInstance = null
  }
}

/**
 * 重置 Loading 计数器
 * 用于处理异常情况，确保 Loading 能被正确关闭
 */
export const resetLoading = () => {
  loadingCount = 0
  if (loadingInstance) {
    loadingInstance.close()
    loadingInstance = null
  }
}

export default {
  showLoading,
  hideLoading,
  resetLoading
}
