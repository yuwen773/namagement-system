/**
 * 常量定义
 */

// 用户角色
export const USER_ROLES = {
  ADMIN: 'ADMIN',
  EMPLOYEE: 'EMPLOYEE',
  USER: 'USER'
}

// 性别
export const GENDER = {
  MALE: 'M',
  FEMALE: 'F',
  OTHER: 'O'
}

// 票房记录状态
export const BOXOFFICE_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  CANCELLED: 'cancelled'
}

// 预测算法
export const PREDICTION_ALGORITHMS = {
  LINEAR_REGRESSION: 'linear_regression',
  MOVING_AVERAGE: 'moving_average'
}

// 日期格式
export const DATE_FORMAT = {
  DISPLAY: 'YYYY-MM-DD',
  DISPLAY_TIME: 'YYYY-MM-DD HH:mm:ss',
  API: 'YYYY-MM-DD'
}

// 分页默认值
export const PAGE_DEFAULT = {
  PAGE: 1,
  PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
}

// 路由名称
export const ROUTE_NAMES = {
  // Auth
  LOGIN: 'Login',
  REGISTER: 'Register',

  // Admin
  ADMIN_DASHBOARD: 'AdminDashboard',
  ADMIN_MOVIES: 'AdminMovies',
  ADMIN_MOVIE_TYPES: 'AdminMovieTypes',
  ADMIN_CINEMAS: 'AdminCinemas',
  ADMIN_REGIONS: 'AdminRegions',
  ADMIN_BOXOFFICE: 'AdminBoxOffice',
  ADMIN_PREDICTION: 'AdminPrediction',
  ADMIN_USERS: 'AdminUsers',

  // User
  USER_DASHBOARD: 'UserDashboard',
  USER_BOXOFFICE: 'UserBoxOffice',
  USER_VISUALIZATION: 'UserVisualization',
  USER_PREDICTION: 'UserPrediction',
  USER_PROFILE: 'UserProfile'
}
