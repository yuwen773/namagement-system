# 通知公告功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为非遗数据平台新增通知公告功能，包括后端 API 和前端页面。

**Architecture:**
- 后端: 新建 Django app `announcements`，使用 ModelViewSet 实现 CRUD
- 前端: Vue 3 页面，公告列表、详情、管理页面，复用现有风格

**Tech Stack:** Django 5.2 + DRF, Vue 3 + Element Plus

---

## Task 1: 创建后端 Announcements App

**Files:**
- Create: `backend/apps/announcements/__init__.py`
- Create: `backend/apps/announcements/apps.py`
- Create: `backend/apps/announcements/models.py`
- Create: `backend/apps/announcements/serializers.py`
- Create: `backend/apps/announcements/views.py`
- Create: `backend/apps/announcements/urls.py`
- Modify: `backend/heritage_system/settings.py`
- Modify: `backend/heritage_system/urls.py`

**Step 1: 创建目录和 __init__.py**

```bash
mkdir -p backend/apps/announcements/migrations
touch backend/apps/announcements/__init__.py
touch backend/apps/announcements/migrations/__init__.py
```

**Step 2: 创建 apps.py**

```python
from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.announcements'
    verbose_name = '通知公告'
```

**Step 3: 创建 models.py**

```python
from django.conf import settings
from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_published = models.BooleanField(default=False, verbose_name='发布状态')
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements',
        verbose_name='发布人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'announcements'
        ordering = ['-is_top', '-created_at']
        verbose_name = '通知公告'
        verbose_name_plural = '通知公告'

    def __str__(self):
        return self.title
```

**Step 4: 创建 serializers.py**

```python
from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'is_published', 'is_top', 'author', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'is_published', 'is_top', 'created_at', 'updated_at']
```

**Step 5: 创建 views.py**

```python
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.pagination import StandardPageNumberPagination
from utils.response import success_response
from apps.users.permissions import IsAdmin

from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('author')
    serializer_class = AnnouncementSerializer
    pagination_class = StandardPageNumberPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return AnnouncementCreateSerializer
        return AnnouncementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # 普通用户只能看到已发布的公告
        if not self.request.user.is_superuser:
            from apps.users.models import get_user_role
            if get_user_role(self.request.user) != 'admin':
                queryset = queryset.filter(is_published=True)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total = self.paginator.page.paginator.count
            return success_response(
                data=serializer.data,
                message='Fetched successfully',
                total=total,
            )
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Fetched successfully',
            total=len(serializer.data),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message='Fetched successfully')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return success_response(
            data=serializer.data,
            message='Created successfully',
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Updated successfully')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message='Deleted successfully')
```

**Step 6: 创建 urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
```

**Step 7: 注册 App 和 URL**

修改 `backend/heritage_system/settings.py`，在 INSTALLED_APPS 添加:
```python
'app.apps.AnnouncementsConfig',
```

修改 `backend/heritage_system/urls.py`，在 urlpatterns 添加:
```python
path('api/v1/', include('apps.announcements.urls')),
```

**Step 8: 生成迁移文件并执行**

```bash
cd backend
python manage.py makemigrations announcements
python manage.py migrate
```

---

## Task 2: 添加前端类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

**添加公告相关类型:**

```typescript
// 通知公告相关类型
export interface Announcement {
  id: number
  title: string
  content: string
  is_published: boolean
  is_top: boolean
  author: number
  author_name: string
  created_at: string
  updated_at: string
}

export interface AnnouncementCreate {
  title: string
  content: string
  is_published?: boolean
  is_top?: boolean
}

export interface AnnouncementListParams extends PaginationParams {
  is_published?: boolean
  is_top?: boolean
}
```

---

## Task 3: 创建前端 API 模块

**Files:**
- Create: `frontend/src/api/announcement.ts`

```typescript
import request from '@/utils/request'
import type { ApiResponse, Announcement, AnnouncementCreate, AnnouncementListParams } from '@/types'

// 获取公告列表
export const getAnnouncementList = (params?: AnnouncementListParams) => {
  return request.get<ApiResponse<Announcement[]>>('/announcements/', { params })
}

// 获取公告详情
export const getAnnouncementDetail = (id: number) => {
  return request.get<ApiResponse<Announcement>>(`/announcements/${id}/`)
}

// 创建公告
export const createAnnouncement = (data: AnnouncementCreate) => {
  return request.post<ApiResponse<Announcement>>('/announcements/', data)
}

// 更新公告
export const updateAnnouncement = (id: number, data: Partial<AnnouncementCreate>) => {
  return request.patch<ApiResponse<Announcement>>(`/announcements/${id}/`, data)
}

// 删除公告
export const deleteAnnouncement = (id: number) => {
  return request.delete<ApiResponse<null>>(`/announcements/${id}/`)
}
```

---

## Task 4: 创建用户端公告列表页面

**Files:**
- Create: `frontend/src/views/AnnouncementList.vue`

**代码结构:**
- 页面头部 (卷轴风格)
- 卡片式列表展示
- 分页组件
- 点击进入详情页

```vue
<template>
  <div class="announcement-list-page">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-seal">
        <span class="seal-text">公告</span>
      </div>
      <h1 class="page-title">通知公告</h1>
    </header>

    <!-- 公告列表 -->
    <div class="announcement-grid">
      <div
        v-for="item in list"
        :key="item.id"
        class="announcement-card"
        @click="goDetail(item.id)"
      >
        <div v-if="item.is_top" class="top-badge">置顶</div>
        <h3 class="card-title">{{ item.title }}</h3>
        <div class="card-meta">
          <span>{{ item.author_name }}</span>
          <span>{{ formatDate(item.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      @current-change="fetchList"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAnnouncementList } from '@/api/announcement'
import type { Announcement } from '@/types'

const router = useRouter()
const list = ref<Announcement[]>([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchList = async () => {
  const res = await getAnnouncementList({ page: page.value, page_size: pageSize.value })
  list.value = res.data.data
  total.value = res.data.total || 0
}

const goDetail = (id: number) => {
  router.push(`/announcements/${id}`)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(fetchList)
</script>

<style scoped>
/* 复用现有页面样式 */
</style>
```

---

## Task 5: 创建用户端公告详情页面

**Files:**
- Create: `frontend/src/views/AnnouncementDetail.vue`

```vue
<template>
  <div class="announcement-detail-page">
    <div class="detail-header">
      <el-button @click="goBack">返回</el-button>
      <h1>{{ announcement.title }}</h1>
      <div class="meta">
        <span>发布人: {{ announcement.author_name }}</span>
        <span>发布时间: {{ formatDate(announcement.created_at) }}</span>
      </div>
    </div>
    <div class="content" v-html="announcement.content"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAnnouncementDetail } from '@/api/announcement'
import type { Announcement } from '@/types'

const route = useRoute()
const router = useRouter()
const announcement = ref<Announcement>({} as Announcement)

const fetchDetail = async () => {
  const id = Number(route.params.id)
  const res = await getAnnouncementDetail(id)
  announcement.value = res.data.data
}

const goBack = () => router.back()
const formatDate = (date: string) => new Date(date).toLocaleDateString('zh-CN')

onMounted(fetchDetail)
</script>

<style scoped>
.content {
  padding: 20px;
  line-height: 1.8;
}
</style>
```

---

## Task 6: 创建管理端公告管理页面

**Files:**
- Create: `frontend/src/views/admin/AnnouncementManage.vue`

**功能:**
- 表格展示所有公告
- 搜索筛选
- 操作: 新建、编辑、删除、置顶、发布/下架
- 富文本编辑 (textarea + 预览)

```vue
<template>
  <div class="announcement-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <h1>公告管理</h1>
      <button class="add-btn" @click="handleAdd">新增公告</button>
    </header>

    <!-- 筛选 -->
    <div class="filter-section">
      <el-input v-model="filters.title" placeholder="搜索标题" @clear="fetchList" />
      <el-select v-model="filters.is_published" placeholder="状态" clearable @change="fetchList">
        <el-option label="已发布" :value="true" />
        <el-option label="草稿" :value="false" />
      </el-select>
      <button class="action-btn" @click="fetchList">搜索</button>
    </div>

    <!-- 表格 -->
    <el-table :data="tableData" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_published ? 'success' : 'info'">
            {{ row.is_published ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="置顶" width="80">
        <template #default="{ row }">
          <el-tag v-if="row.is_top" type="warning">置顶</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <button class="table-action-btn" @click="handleEdit(row)">编辑</button>
          <button class="table-action-btn" @click="handleTogglePublish(row)">
            {{ row.is_published ? '下架' : '发布' }}
          </button>
          <button class="table-action-btn" @click="handleToggleTop(row)">
            {{ row.is_top ? '取消置顶' : '置顶' }}
          </button>
          <button class="table-action-btn delete-btn" @click="handleDelete(row)">删除</button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="fetchList"
    />

    <!-- 编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑公告' : '新增公告'" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="form.content" type="textarea" :rows="10" />
        </el-form-item>
        <el-form-item label="发布">
          <el-switch v-model="form.is_published" />
        </el-form-item>
        <el-form-item label="置顶">
          <el-switch v-model="form.is_top" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAnnouncementList, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api/announcement'
import type { Announcement, AnnouncementCreate } from '@/types'

const tableData = ref<Announcement[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const filters = reactive({ title: '', is_published: undefined as boolean | undefined })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(0)
const form = reactive<AnnouncementCreate>({ title: '', content: '', is_published: false, is_top: false })

const fetchList = async () => {
  loading.value = true
  const res = await getAnnouncementList({ page: page.value, page_size: pageSize.value, ...filters })
  tableData.value = res.data.data
  total.value = res.data.total || 0
  loading.value = false
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, { title: '', content: '', is_published: false, is_top: false })
  dialogVisible.value = true
}

const handleEdit = (row: Announcement) => {
  isEdit.value = true
  editingId.value = row.id
  Object.assign(form, { title: row.title, content: row.content, is_published: row.is_published, is_top: row.is_top })
  dialogVisible.value = true
}

const handleSave = async () => {
  if (isEdit.value) {
    await updateAnnouncement(editingId.value, form)
    ElMessage.success('更新成功')
  } else {
    await createAnnouncement(form)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  fetchList()
}

const handleDelete = async (row: Announcement) => {
  await ElMessageBox.confirm('确定删除该公告?', '提示', { type: 'warning' })
  await deleteAnnouncement(row.id)
  ElMessage.success('删除成功')
  fetchList()
}

const handleTogglePublish = async (row: Announcement) => {
  await updateAnnouncement(row.id, { is_published: !row.is_published })
  ElMessage.success(row.is_published ? '已下架' : '已发布')
  fetchList()
}

const handleToggleTop = async (row: Announcement) => {
  await updateAnnouncement(row.id, { is_top: !row.is_top })
  ElMessage.success(row.is_top ? '已取消置顶' : '已置顶')
  fetchList()
}

const formatDate = (date: string) => new Date(date).toLocaleDateString('zh-CN')

onMounted(fetchList)
</script>

<style scoped>
/* 复用现有管理页面样式 */
</style>
```

---

## Task 7: 添加路由配置

**Files:**
- Modify: `frontend/src/router/index.ts`

**添加路由:**

```typescript
// 用户端
{
  path: 'announcements',
  name: 'AnnouncementList',
  component: () => import('@/views/AnnouncementList.vue'),
  meta: { requiresAuth: true }
},
{
  path: 'announcements/:id',
  name: 'AnnouncementDetail',
  component: () => import('@/views/AnnouncementDetail.vue'),
  meta: { requiresAuth: true }
},
// 管理端
{
  path: 'admin/announcements',
  name: 'AdminAnnouncements',
  component: () => import('@/views/admin/AnnouncementManage.vue'),
  meta: { requiresAuth: true, requiresAdmin: true }
}
```

---

## Task 8: 添加侧边栏菜单

**Files:**
- Modify: `frontend/src/layouts/MainLayout.vue`

**添加菜单项:**

```typescript
// viewMenus 添加
{ path: '/announcements', title: '通知公告', icon: Bell, seal: '告' }

// adminMenus 添加
{ path: '/admin/announcements', title: '公告管理', icon: Bell, seal: '告' }

// 导入 Bell 图标
import { Bell } from '@element-plus/icons-vue'
```

---

## Task 9: 测试验证

**测试步骤:**

1. 后端 API 测试:
   - `GET /api/v1/announcements/` - 获取公告列表 (需登录)
   - `GET /api/v1/announcements/1/` - 获取公告详情
   - `POST /api/v1/announcements/` - 创建公告 (需管理员)
   - `PATCH /api/v1/announcements/1/` - 更新公告
   - `DELETE /api/v1/announcements/1/` - 删除公告

2. 前端页面测试:
   - 访问 `/announcements` 查看公告列表
   - 点击公告查看详情
   - 管理员访问 `/admin/announcements` 进行 CRUD 操作

---

**Plan complete and saved to `docs/plans/2026-02-26-announcement-implementation.md`. Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
