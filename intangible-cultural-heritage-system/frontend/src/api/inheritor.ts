import request from '@/utils/request'
import type { ApiResponse, Inheritor, InheritorCreate, InheritorListParams } from '@/types'

// 获取传承人列表
export const getInheritorList = (params?: InheritorListParams) => {
  return request.get<ApiResponse<Inheritor[]>>('/inheritors/', { params })
}

// 获取传承人详情
export const getInheritorDetail = (id: number) => {
  return request.get<ApiResponse<Inheritor>>(`/inheritors/${id}/`)
}

// 创建传承人
export const createInheritor = (data: InheritorCreate) => {
  return request.post<ApiResponse<Inheritor>>('/inheritors/', data)
}

// 更新传承人
export const updateInheritor = (id: number, data: Partial<InheritorCreate>) => {
  return request.patch<ApiResponse<Inheritor>>(`/inheritors/${id}/`, data)
}

// 删除传承人
export const deleteInheritor = (id: number) => {
  return request.delete<ApiResponse<null>>(`/inheritors/${id}/`)
}
