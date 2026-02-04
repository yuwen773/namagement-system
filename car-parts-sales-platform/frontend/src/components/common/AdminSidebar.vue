<template>
  <aside class="admin-sidebar" :class="{ collapsed: collapsed }">
    <!-- Logo区域 -->
    <div class="sidebar-logo">
      <router-link to="/admin/dashboard" class="logo-link">
        <el-icon class="logo-icon"><Tools /></el-icon>
        <span v-show="!collapsed" class="logo-text">管理后台</span>
      </router-link>
      <el-button
        class="collapse-btn"
        :icon="collapsed ? Expand : Fold"
        @click="handleToggle"
        text
      />
    </div>

    <!-- 菜单区域 -->
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      :unique-opened="true"
      class="sidebar-menu"
      router
    >
      <!-- 仪表盘 -->
      <el-menu-item index="/admin/dashboard">
        <el-icon><DataAnalysis /></el-icon>
        <template #title>数据统计</template>
      </el-menu-item>

      <!-- 商品管理 -->
      <el-sub-menu index="products">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>商品管理</span>
        </template>
        <el-menu-item index="/admin/products">商品列表</el-menu-item>
        <el-menu-item index="/admin/categories">分类管理</el-menu-item>
        <el-menu-item index="/admin/attributes">属性管理</el-menu-item>
        <el-menu-item index="/admin/reviews">评价管理</el-menu-item>
      </el-sub-menu>

      <!-- 订单管理 -->
      <el-sub-menu index="orders">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>订单管理</span>
        </template>
        <el-menu-item index="/admin/orders">订单列表</el-menu-item>
        <el-menu-item index="/admin/returns">售后管理</el-menu-item>
        <el-menu-item index="/admin/shipping">发货管理</el-menu-item>
      </el-sub-menu>

      <!-- 用户管理 -->
      <el-sub-menu index="users">
        <template #title>
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </template>
        <el-menu-item index="/admin/users">用户列表</el-menu-item>
        <el-menu-item index="/admin/levels">用户等级</el-menu-item>
        <el-menu-item index="/admin/points">积分管理</el-menu-item>
      </el-sub-menu>

      <!-- 营销管理 -->
      <el-sub-menu index="marketing">
        <template #title>
          <el-icon><Ticket /></el-icon>
          <span>营销管理</span>
        </template>
        <el-menu-item index="/admin/marketing">优惠券</el-menu-item>
        <el-menu-item index="/admin/promotions">促销活动</el-menu-item>
        <el-menu-item index="/admin/banners">Banner管理</el-menu-item>
        <el-menu-item index="/admin/recommendations">推荐配置</el-menu-item>
      </el-sub-menu>

      <!-- 内容管理 -->
      <el-sub-menu index="content">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>内容管理</span>
        </template>
        <el-menu-item index="/admin/content">改装案例</el-menu-item>
        <el-menu-item index="/admin/faqs">FAQ管理</el-menu-item>
        <el-menu-item index="/admin/articles">文章管理</el-menu-item>
      </el-sub-menu>

      <!-- 系统管理 -->
      <el-sub-menu index="system">
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>系统管理</span>
        </template>
        <el-menu-item index="/admin/system">系统配置</el-menu-item>
        <el-menu-item index="/admin/system/messages">消息管理</el-menu-item>
        <el-menu-item index="/admin/system/logs">操作日志</el-menu-item>
        <el-menu-item index="/admin/admins">管理员管理</el-menu-item>
      </el-sub-menu>
    </el-menu>

    <!-- 底部按钮 -->
    <div class="sidebar-footer">
      <el-tooltip :content="collapsed ? '返回前台' : '返回前台'" placement="right">
        <el-button
          class="home-btn"
          :icon="HomeFilled"
          @click="goHome"
          circle
        />
      </el-tooltip>
      <el-tooltip :content="collapsed ? '退出登录' : '退出登录'" placement="right">
        <el-button
          class="logout-btn"
          :icon="SwitchButton"
          @click="handleLogout"
          circle
        />
      </el-tooltip>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Tools, Expand, Fold, DataAnalysis, Box, Document, User,
  Ticket, Setting, HomeFilled, SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 从本地存储读取折叠状态
const collapsed = computed({
  get: () => localStorage.getItem('sidebar-collapsed') === 'true',
  set: (value) => localStorage.setItem('sidebar-collapsed', value.toString())
})

// 当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 切换折叠
const handleToggle = () => {
  collapsed.value = !collapsed.value
}

// 返回前台
const goHome = () => {
  router.push('/')
}

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 取消退出
  }
}
</script>

<style scoped>
.admin-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  background: #304156;
  transition: width 0.3s;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.admin-sidebar.collapsed {
  width: 64px;
}

/* Logo区域 */
.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: #263445;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  font-size: 28px;
  color: #409eff;
  flex-shrink: 0;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.collapse-btn {
  color: #909399;
  flex-shrink: 0;
}

.collapse-btn:hover {
  color: #409eff;
}

/* 菜单区域 */
.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  border: none;
  background: transparent;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 240px;
}

/* 滚动条样式 */
.sidebar-menu::-webkit-scrollbar {
  width: 6px;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.sidebar-menu::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 菜单项样式 */
:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  color: #bfcbd9;
  height: 50px;
  line-height: 50px;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #409eff !important;
}

:deep(.el-menu-item.is-active) {
  background: #409eff !important;
  color: #fff !important;
}

:deep(.el-menu-item.is-active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #fff;
}

:deep(.el-sub-menu .el-menu-item) {
  background: #1f2d3d !important;
  min-width: 200px;
}

:deep(.el-sub-menu .el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.05) !important;
}

:deep(.el-icon) {
  font-size: 18px;
}

/* 底部按钮 */
.sidebar-footer {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 16px;
  background: #263445;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.home-btn,
.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #bfcbd9;
}

.home-btn:hover,
.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #409eff;
}

/* 折叠状态 */
.collapsed .sidebar-logo {
  padding: 0 18px;
}

.collapsed .collapse-btn {
  padding: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar:not(.collapsed) {
    transform: translateX(0);
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);
  }
}
</style>
