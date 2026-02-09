import request from '@/utils/request'

/**
 * 获取问答列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.search - 搜索关键词
 */
export function getQuestions(params) {
  return request.get('/api/questions/', { params })
}

/**
 * 获取问答详情
 * @param {number} id - 问答ID
 */
export function getQuestionDetail(id) {
  return request.get(`/api/questions/${id}/`)
}

/**
 * 删除问答
 * @param {number} id - 问答ID
 */
export function deleteQuestion(id) {
  return request.delete(`/api/questions/${id}/`)
}
