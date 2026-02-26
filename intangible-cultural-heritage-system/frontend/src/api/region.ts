import request from '@/utils/request'
import type { ApiResponse, Region } from '@/types'

// 获取地区列表
export const getRegionList = (params?: { 
  page?: number
  search?: string
}) => {
  return request.get<ApiResponse<Region[]>>('/regions/', { params })
}

// 获取地区详情
export const getRegionDetail = (id: number) => {
  return request.get<ApiResponse<Region>>(`/regions/${id}/`)
}

// 创建地区
export const createRegion = (data: {
  country_code: string
  country_name: string
  latitude: number
  longitude: number
  continent?: string
}) => {
  return request.post<ApiResponse<Region>>('/regions/', data)
}

// 更新地区
export const updateRegion = (id: number, data: Partial<{
  country_code: string
  country_name: string
  latitude: number
  longitude: number
  continent?: string
}>) => {
  return request.patch<ApiResponse<Region>>(`/regions/${id}/`, data)
}

// 删除地区
export const deleteRegion = (id: number) => {
  return request.delete<ApiResponse<null>>(`/regions/${id}/`)
}
