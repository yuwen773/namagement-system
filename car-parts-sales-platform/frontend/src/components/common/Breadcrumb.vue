<template>
  <div class="breadcrumb-wrapper">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">
        <el-icon><HomeFilled /></el-icon>
        <span>首页</span>
      </el-breadcrumb-item>
      <el-breadcrumb-item
        v-for="(item, index) in breadcrumbList"
        :key="index"
        :to="index < breadcrumbList.length - 1 ? { path: item.path } : undefined"
      >
        <el-icon v-if="item.icon">
          <component :is="item.icon" />
        </el-icon>
        <span>{{ item.title }}</span>
      </el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 可选的右侧内容 -->
    <div v-if="$slots.extra" class="breadcrumb-extra">
      <slot name="extra" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()

// 路由映射表，用于将路由路径转换为面包屑标题
const routeMap = {
  // 用户端路由
  products: { title: '商品列表', icon: 'Goods' },
  search: { title: '搜索结果', icon: 'Search' },
  cart: { title: '购物车', icon: 'ShoppingCart' },
  orders: { title: '我的订单', icon: 'Document' },
  user: { title: '个人中心', icon: 'User' },
  login: { title: '登录', icon: 'Lock' },
  register: { title: '注册', icon: 'UserFilled' },

  // 用户中心子路由
  'user/profile': { title: '个人资料', icon: 'User' },
  'user/addresses': { title: '收货地址', icon: 'Location' },
  'user/orders': { title: '我的订单', icon: 'Document' },
  'user/coupons': { title: '我的优惠券', icon: 'Ticket' },
  'user/favorites': { title: '我的收藏', icon: 'Star' },
  'user/history': { title: '浏览历史', icon: 'Clock' },
  'user/messages': { title: '消息中心', icon: 'Bell' },
  'user/returns': { title: '售后服务', icon: 'Refresh' },
  'user/points': { title: '我的积分', icon: 'Medal' },

  // 管理端路由
  'admin/dashboard': { title: '数据统计', icon: 'DataAnalysis' },
  'admin/products': { title: '商品管理', icon: 'Box' },
  'admin/categories': { title: '分类管理', icon: 'FolderOpened' },
  'admin/orders': { title: '订单管理', icon: 'Document' },
  'admin/users': { title: '用户管理', icon: 'User' },
  'admin/coupons': { title: '优惠券管理', icon: 'Ticket' },
  'admin/cases': { title: '改装案例', icon: 'Document' },
  'admin/faqs': { title: 'FAQ管理', icon: 'QuestionFilled' },
  'admin/system': { title: '系统管理', icon: 'Setting' }
}

// 根据路由生成面包屑列表
const breadcrumbList = computed(() => {
  const path = route.path
  const segments = path.split('/').filter(Boolean)
  const breadcrumbs = []

  // 处理管理端路由
  if (segments[0] === 'admin') {
    // 添加"管理后台"
    breadcrumbs.push({ title: '管理后台', path: '/admin/dashboard' })

    // 处理子路由
    if (segments.length > 1) {
      const subPath = segments.slice(0, 2).join('/')
      const routeInfo = routeMap[subPath]
      if (routeInfo) {
        breadcrumbs.push({ title: routeInfo.title, path: `/${subPath}` })
      }
    }

    // 处理详情页（如 /admin/products/123）
    if (segments.length > 2) {
      const parentPath = segments.slice(0, 2).join('/')
      const detailInfo = routeMap[parentPath]
      if (detailInfo) {
        breadcrumbs.push({
          title: detailInfo.title.replace('管理', '') + '详情',
          path: path
        })
      }
    }
  }
  // 处理用户端路由
  else {
    // 处理商品详情页
    if (segments[0] === 'products' && segments.length === 2) {
      breadcrumbs.push({ title: '商品列表', path: '/products' })
      breadcrumbs.push({ title: '商品详情', path: path })
    }
    // 处理订单详情页
    else if (segments[0] === 'orders' && segments.length === 2) {
      breadcrumbs.push({ title: '我的订单', path: '/orders' })
      breadcrumbs.push({ title: '订单详情', path: path })
    }
    // 处理其他路由
    else if (segments.length > 0) {
      const routeKey = segments.join('/')
      const routeInfo = routeMap[routeKey]
      if (routeInfo) {
        breadcrumbs.push({ title: routeInfo.title, path: path })
      } else {
        // 尝试从父路由获取信息
        const parentPath = segments[0]
        const parentInfo = routeMap[parentPath]
        if (parentInfo) {
          breadcrumbs.push({ title: parentInfo.title, path: `/${parentPath}` })
          // 添加子页面标题
          if (segments.length > 1) {
            const subRouteKey = segments.slice(0, -1).join('/')
            const subRouteInfo = routeMap[subRouteKey]
            if (subRouteInfo) {
              breadcrumbs.push({ title: subRouteInfo.title, path: path })
            }
          }
        }
      }
    }
  }

  return breadcrumbs
})
</script>

<style scoped>
.breadcrumb-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
}

.breadcrumb-wrapper :deep(.el-breadcrumb) {
  font-size: 14px;
}

.breadcrumb-wrapper :deep(.el-breadcrumb__item) {
  display: flex;
  align-items: center;
}

.breadcrumb-wrapper :deep(.el-breadcrumb__inner) {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-weight: normal;
}

.breadcrumb-wrapper :deep(.el-breadcrumb__inner:hover) {
  color: #409eff;
}

.breadcrumb-wrapper :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #909399;
  cursor: default;
}

.breadcrumb-wrapper :deep(.el-icon) {
  font-size: 14px;
}

.breadcrumb-extra {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .breadcrumb-wrapper {
    padding: 12px 16px;
  }

  .breadcrumb-wrapper :deep(.el-breadcrumb) {
    font-size: 12px;
  }
}
</style>
