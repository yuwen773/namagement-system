import axios from './axios'

// 绩效评估 API 封装

/**
 * 获取绩效评估列表
 * @param {Object} params - 查询参数
 * @param {string} params.review_period - 评估周期筛选
 * @param {string} params.status - 状态筛选 (draft/published)
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 */
export function getPerformanceReviewList(params) {
  return axios.get('/performance/reviews/', { params })
}

/**
 * 获取绩效评估详情
 * @param {number} id - 评估ID
 */
export function getPerformanceReviewDetail(id) {
  return axios.get(`/performance/reviews/${id}/`)
}

/**
 * 创建绩效评估
 * @param {Object} data - 评估数据
 */
export function createPerformanceReview(data) {
  return axios.post('/performance/reviews/', data)
}

/**
 * 更新绩效评估
 * @param {number} id - 评估ID
 * @param {Object} data - 更新数据
 */
export function updatePerformanceReview(id, data) {
  return axios.put(`/performance/reviews/${id}/`, data)
}

/**
 * 删除绩效评估
 * @param {number} id - 评估ID
 */
export function deletePerformanceReview(id) {
  return axios.delete(`/performance/reviews/${id}/`)
}

/**
 * 获取我的绩效（所有认证用户）
 */
export function getMyPerformanceReviews(params) {
  return axios.get('/performance/reviews/my_reviews/', { params })
}

/**
 * 获取待发布草稿列表（HR/Admin）
 */
export function getPendingPerformanceReviews(params) {
  return axios.get('/performance/reviews/pending/', { params })
}

/**
 * 发布绩效评估（HR/Admin）
 * @param {number} id - 评估ID
 */
export function publishPerformanceReview(id) {
  return axios.post(`/performance/reviews/${id}/publish/`)
}

/**
 * 撤回绩效评估（HR/Admin）
 * @param {number} id - 评估ID
 */
export function unpublishPerformanceReview(id) {
  return axios.post(`/performance/reviews/${id}/unpublish/`)
}

/**
 * 获取员工列表（用于创建评估时选择）
 * 返回的是 EmployeeProfile 列表，包含 user_id 字段
 * @param {Object} params - 查询参数
 */
export function getEmployeeOptions(params) {
  return axios.get('/employee/', {
    params: {
      ...params,
      status: 'active',
      page_size: 100 // 获取全部在职员工
    }
  })
}

// 常量定义

/**
 * 评估周期选项
 */
export const REVIEW_PERIOD_OPTIONS = [
  { value: '2025-Q1', label: '2025年第一季度' },
  { value: '2025-Q2', label: '2025年第二季度' },
  { value: '2025-Q3', label: '2025年第三季度' },
  { value: '2025-Q4', label: '2025年第四季度' },
  { value: '2025-01', label: '2025年1月' },
  { value: '2025-02', label: '2025年2月' },
  { value: '2025-03', label: '2025年3月' },
  { value: '2025-04', label: '2025年4月' },
  { value: '2025-05', label: '2025年5月' },
  { value: '2025-06', label: '2025年6月' },
  { value: '2025-07', label: '2025年7月' },
  { value: '2025-08', label: '2025年8月' },
  { value: '2025-09', label: '2025年9月' },
  { value: '2025-10', label: '2025年10月' },
  { value: '2025-11', label: '2025年11月' },
  { value: '2025-12', label: '2025年12月' }
]

/**
 * 评分选项
 */
export const SCORE_OPTIONS = [
  { value: 5, label: '5分 - 优秀' },
  { value: 4, label: '4分 - 良好' },
  { value: 3, label: '3分 - 合格' },
  { value: 2, label: '2分 - 待改进' },
  { value: 1, label: '1分 - 不合格' }
]

/**
 * 状态映射
 */
export const STATUS = {
  DRAFT: 'draft',
  PUBLISHED: 'published'
}

/**
 * 状态文本映射
 */
export const STATUS_TEXT = {
  [STATUS.DRAFT]: '草稿',
  [STATUS.PUBLISHED]: '已发布'
}

/**
 * 状态类型映射（用于标签颜色）
 */
export const STATUS_TYPE = {
  [STATUS.DRAFT]: 'info',
  [STATUS.PUBLISHED]: 'success'
}
