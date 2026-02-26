import request from '@/utils/request'
import type { 
  ApiResponse, 
  DashboardOverview, 
  MapPoint, 
  CategoryDistribution, 
  CountryRanking 
} from '@/types'

// 获取总览统计
export const getOverview = () => {
  return request.get<ApiResponse<DashboardOverview>>('/dashboard/overview/')
}

// 获取地图分布数据
export const getMapDistribution = (params?: { category?: number }) => {
  return request.get<ApiResponse<MapPoint[]>>('/dashboard/map-distribution/', { params })
}

// 获取类别占比
export const getCategoryDistribution = () => {
  return request.get<ApiResponse<CategoryDistribution[]>>('/dashboard/category-distribution/')
}

// 获取国家排行
export const getCountryRanking = (params?: { limit?: number }) => {
  return request.get<ApiResponse<CountryRanking[]>>('/dashboard/country-ranking/', { params })
}
