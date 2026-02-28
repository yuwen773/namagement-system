import request from '@/utils/request'

// 用户认证
export const authApi = {
  login(data) {
    return request.post('/users/login/', data)
  },
  register(data) {
    return request.post('/users/register/', data)
  },
  getProfile() {
    return request.get('/users/profile/')
  },
  changePassword(data) {
    return request.post('/users/change-password/', data)
  }
}

// 用户管理（管理员）
export const userApi = {
  getList(params) {
    return request.get('/users/', { params })
  },
  getDetail(id) {
    return request.get(`/users/${id}/`)
  },
  update(id, data) {
    return request.put(`/users/${id}/`, data)
  },
  delete(id) {
    return request.delete(`/users/${id}/`)
  },
  updateStatus(id, status) {
    return request.post(`/users/${id}/status/`, { status })
  },
  resetPassword(id, newPassword) {
    return request.post(`/users/${id}/reset-password/`, { new_password: newPassword })
  }
}

// 商品管理
export const productApi = {
  getList(params) {
    return request.get('/products/', { params })
  },
  getDetail(id) {
    return request.get(`/products/${id}/`)
  },
  create(data) {
    return request.post('/products/', data)
  },
  update(id, data) {
    return request.put(`/products/${id}/`, data)
  },
  delete(id) {
    return request.delete(`/products/${id}/`)
  },
  getPriceHistory(id, params) {
    return request.get(`/products/${id}/price-history/`, { params })
  },
  export(params) {
    return request.get('/products/export/', {
      params,
      responseType: 'blob'
    })
  }
}

// 数据导入
export const importApi = {
  start(data) {
    return request.post('/products/import/', data)
  },
  getTaskList() {
    return request.get('/products/import/')
  },
  getTaskDetail(taskId) {
    return request.get(`/products/import/${taskId}/`)
  }
}

// 爬虫控制
export const crawlerApi = {
  start(data) {
    return request.post('/crawler/start/', data)
  },
  getStatus(taskId) {
    return request.get(`/crawler/status/${taskId}/`)
  },
  stop(taskId) {
    return request.post(`/crawler/stop/${taskId}/`)
  },
  getLogs(params) {
    return request.get('/crawler/logs/', { params })
  },
  getLogDetail(id) {
    return request.get(`/crawler/logs/${id}/`)
  },
  getStats() {
    return request.get('/crawler/stats/')
  },
  getSystemHealth() {
    return request.get('/crawler/system-health/')
  }
}

// 采集日志
export const crawlLogApi = {
  getList(params) {
    return request.get('/crawl-logs/', { params })
  },
  getDetail(id) {
    return request.get(`/crawl-logs/${id}/`)
  }
}

// 数据统计
export const statisticsApi = {
  // 基础统计
  getOverview(params) {
    return request.get('/products/statistics/overview/', { params })
  },
  getPriceDistribution(params) {
    return request.get('/products/statistics/price-distribution/', { params })
  },
  getSalesDistribution(params) {
    return request.get('/products/statistics/sales-distribution/', { params })
  },

  // 品牌分析
  getBrandAnalysis(params) {
    return request.get('/products/statistics/brand-analysis/', { params })
  },

  // 地区分析
  getRegionAnalysis(params) {
    return request.get('/products/statistics/region-analysis/', { params })
  },

  // 店铺分析
  getShopAnalysis(params) {
    return request.get('/products/statistics/shop-analysis/', { params })
  },

  // 商品排行
  getTopProducts(params) {
    return request.get('/products/statistics/top-products/', { params })
  },

  // 关联分析
  getPriceSalesCorrelation(params) {
    return request.get('/products/statistics/price-sales-correlation/', { params })
  },

  // 属性分析
  getAttributeAnalysis(params) {
    return request.get('/products/statistics/attribute-analysis/', { params })
  },

  // 宠物分析
  getPetTypeDistribution() {
    return request.get('/products/statistics/pet-type/')
  },
  getPetUseDistribution() {
    return request.get('/products/statistics/pet-use/')
  },

  // 批次分析
  getBatchAnalysis(params) {
    return request.get('/products/statistics/batch-analysis/', { params })
  },

  // 关键词分析
  getKeywordAnalysis(params) {
    return request.get('/products/statistics/keyword-analysis/', { params })
  },

  // 市场洞察
  getMarketInsights(params) {
    return request.get('/products/statistics/market-insights/', { params })
  },

  // 仪表板（一次性获取所有数据）
  getDashboard(params) {
    return request.get('/products/statistics/dashboard/', { params })
  },

  // 兼容旧接口
  getTopSales() {
    return request.get('/products/statistics/top-sales/')
  },
  getShopRanking(params) {
    return request.get('/products/statistics/shop-ranking/', { params })
  }
}
