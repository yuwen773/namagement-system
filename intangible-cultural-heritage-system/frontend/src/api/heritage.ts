import request from '@/utils/request'
import type { ApiResponse, HeritageItem, HeritageItemCreate, HeritageListParams } from '@/types'

// 获取非遗项目列表
export const getHeritageList = (params?: HeritageListParams) => {
  return request.get<ApiResponse<HeritageItem[]>>('/heritage/', { params })
}

// 获取非遗项目详情
export const getHeritageDetail = (id: number) => {
  return request.get<ApiResponse<HeritageItem>>(`/heritage/${id}/`)
}

// 创建非遗项目
export const createHeritage = (data: HeritageItemCreate) => {
  return request.post<ApiResponse<HeritageItem>>('/heritage/', data)
}

// 更新非遗项目
export const updateHeritage = (id: number, data: Partial<HeritageItemCreate>) => {
  return request.patch<ApiResponse<HeritageItem>>(`/heritage/${id}/`, data)
}

// 删除非遗项目
export const deleteHeritage = (id: number) => {
  return request.delete<ApiResponse<null>>(`/heritage/${id}/`)
}
