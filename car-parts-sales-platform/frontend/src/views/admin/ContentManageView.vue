<template>
  <div class="content-manage-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">内容管理</h1>
        <p class="page-subtitle">管理改装案例和常见问题</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" :icon="Plus" @click="handleAdd">
          新增内容
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
          <el-icon :size="24"><Document /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalCases }}</div>
          <div class="stat-label">改装案例</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);">
          <el-icon :size="24"><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.publishedCases }}</div>
          <div class="stat-label">已发布案例</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);">
          <el-icon :size="24"><QuestionFilled /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalFAQs }}</div>
          <div class="stat-label">常见问题</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
          <el-icon :size="24"><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.activeFAQs }}</div>
          <div class="stat-label">启用中 FAQ</div>
        </div>
      </div>
    </div>

    <!-- 选项卡 -->
    <el-tabs v-model="activeTab" class="content-tabs" @tab-change="handleTabChange">
      <!-- 改装案例管理 -->
      <el-tab-pane label="改装案例" name="cases">
        <!-- 筛选工具栏 -->
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-input
              v-model="caseFilter.search"
              placeholder="搜索案例标题..."
              class="search-input"
              clearable
              @clear="handleCaseSearch"
              @keyup.enter="handleCaseSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>

            <el-select v-model="caseFilter.status" placeholder="状态" clearable class="filter-select">
              <el-option label="已发布" value="published" />
              <el-option label="草稿" value="draft" />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleCaseSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleCaseReset">重置</el-button>
          </div>
        </div>

        <!-- 案例列表 -->
        <div class="table-container">
          <el-table
            v-loading="caseLoading"
            :data="caseList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="封面" width="100">
              <template #default="{ row }">
                <el-image
                  v-if="row.cover_image"
                  :src="row.cover_image"
                  fit="cover"
                  class="cover-image"
                  :preview-src-list="[row.cover_image]"
                />
                <div v-else class="cover-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="案例信息" min-width="300">
              <template #default="{ row }">
                <div class="case-info">
                  <div class="case-title">{{ row.title }}</div>
                  <div class="case-summary">{{ row.summary || '暂无摘要' }}</div>
                  <div class="case-meta">
                    <span class="meta-item">
                      <el-icon><User /></el-icon>
                      {{ row.author || '-' }}
                    </span>
                    <span class="meta-item">
                      <el-icon><View /></el-icon>
                      {{ row.view_count || 0 }}
                    </span>
                  </div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getCaseStatusType(row.status)" size="small">
                  {{ getCaseStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="排序" width="90" align="center">
              <template #default="{ row }">
                <span class="sort-text">{{ row.sort_order || 0 }}</span>
              </template>
            </el-table-column>

            <el-table-column label="发布时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.published_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="创建时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.created_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="View" @click="handleViewCase(row)">
                  查看
                </el-button>
                <el-button link type="primary" :icon="Edit" @click="handleEditCase(row)">
                  编辑
                </el-button>
                <el-button link type="danger" :icon="Delete" @click="handleDeleteCase(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="casePagination.page"
              v-model:page-size="casePagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="casePagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleCaseSizeChange"
              @current-change="handleCasePageChange"
            />
          </div>
        </div>
      </el-tab-pane>

      <!-- FAQ 管理 -->
      <el-tab-pane label="常见问题" name="faqs">
        <!-- 筛选工具栏 -->
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-input
              v-model="faqFilter.search"
              placeholder="搜索问题或答案..."
              class="search-input"
              clearable
              @clear="handleFAQSearch"
              @keyup.enter="handleFAQSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>

            <el-select v-model="faqFilter.category" placeholder="问题分类" clearable class="filter-select">
              <el-option label="订单相关" value="order" />
              <el-option label="支付相关" value="payment" />
              <el-option label="物流相关" value="shipping" />
              <el-option label="商品相关" value="product" />
              <el-option label="退换货" value="return" />
              <el-option label="其他问题" value="other" />
            </el-select>

            <el-select v-model="faqFilter.isActive" placeholder="状态" clearable class="filter-select">
              <el-option label="启用" :value="true" />
              <el-option label="禁用" :value="false" />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleFAQSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleFAQReset">重置</el-button>
          </div>
        </div>

        <!-- FAQ 列表 -->
        <div class="table-container">
          <el-table
            v-loading="faqLoading"
            :data="faqList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="问题" min-width="250">
              <template #default="{ row }">
                <div class="question-text">{{ row.question }}</div>
              </template>
            </el-table-column>

            <el-table-column label="答案" min-width="300">
              <template #default="{ row }">
                <div class="answer-text">{{ row.answer || '-' }}</div>
              </template>
            </el-table-column>

            <el-table-column label="分类" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="getFAQCategoryType(row.category)" size="small">
                  {{ getFAQCategoryLabel(row.category) }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="排序" width="90" align="center">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.sort_order"
                  :min="0"
                  :max="9999"
                  size="small"
                  controls-position="right"
                  @change="handleFAQSortOrderChange(row)"
                />
              </template>
            </el-table-column>

            <el-table-column label="状态" width="90" align="center">
              <template #default="{ row }">
                <el-switch
                  v-model="row.is_active"
                  @change="handleFAQStatusChange(row)"
                />
              </template>
            </el-table-column>

            <el-table-column label="创建时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.created_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="Edit" @click="handleEditFAQ(row)">
                  编辑
                </el-button>
                <el-button link type="danger" :icon="Delete" @click="handleDeleteFAQ(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="faqPagination.page"
              v-model:page-size="faqPagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="faqPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleFAQSizeChange"
              @current-change="handleFAQPageChange"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 案例编辑对话框 -->
    <el-dialog
      v-model="caseDialogVisible"
      :title="isEditMode ? '编辑改装案例' : '新增改装案例'"
      width="700px"
      @close="handleCaseDialogClose"
    >
      <el-form
        ref="caseFormRef"
        :model="caseForm"
        :rules="caseFormRules"
        label-width="100px"
      >
        <el-form-item label="案例标题" prop="title">
          <el-input
            v-model="caseForm.title"
            placeholder="请输入案例标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="案例摘要" prop="summary">
          <el-input
            v-model="caseForm.summary"
            type="textarea"
            placeholder="请输入案例摘要"
            :rows="3"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="封面图片" prop="cover_image">
          <el-input
            v-model="caseForm.cover_image"
            placeholder="请输入封面图片URL"
          />
          <div v-if="caseForm.cover_image" class="image-preview">
            <el-image
              :src="caseForm.cover_image"
              fit="cover"
              style="width: 200px; height: 150px; border-radius: 8px;"
              :preview-src-list="[caseForm.cover_image]"
            />
          </div>
        </el-form-item>

        <el-form-item label="作者" prop="author">
          <el-input
            v-model="caseForm.author"
            placeholder="请输入作者名称"
            maxlength="50"
          />
        </el-form-item>

        <el-form-item label="详细内容" prop="content">
          <el-input
            v-model="caseForm.content"
            type="textarea"
            placeholder="请输入详细内容（支持Markdown格式）"
            :rows="8"
            maxlength="10000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="排序值" prop="sort_order">
          <el-input-number
            v-model="caseForm.sort_order"
            :min="0"
            :max="9999"
            placeholder="数字越大越靠前"
          />
          <span class="form-tip">数字越大越靠前</span>
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="caseForm.status">
            <el-radio value="draft">草稿</el-radio>
            <el-radio value="published">发布</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="发布时间" prop="published_at">
          <el-date-picker
            v-model="caseForm.published_at"
            type="datetime"
            placeholder="选择发布时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="caseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveCase" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 案例查看对话框 -->
    <el-dialog
      v-model="caseViewDialogVisible"
      title="案例详情"
      width="800px"
    >
      <div v-if="currentCase" class="case-detail-content">
        <div class="detail-cover">
          <el-image
            v-if="currentCase.cover_image"
            :src="currentCase.cover_image"
            fit="cover"
            class="cover-large"
            :preview-src-list="[currentCase.cover_image]"
          />
          <div v-else class="cover-placeholder-large">
            <el-icon><Picture /></el-icon>
          </div>
        </div>

        <div class="detail-info">
          <h2 class="detail-title">{{ currentCase.title }}</h2>

          <div class="detail-meta">
            <span class="meta-item">
              <el-icon><User /></el-icon>
              {{ currentCase.author || '-' }}
            </span>
            <span class="meta-item">
              <el-icon><View /></el-icon>
              {{ currentCase.view_count || 0 }} 次浏览
            </span>
            <span class="meta-item">
              <el-tag :type="getCaseStatusType(currentCase.status)" size="small">
                {{ getCaseStatusLabel(currentCase.status) }}
              </el-tag>
            </span>
          </div>

          <div class="detail-summary">
            <strong>摘要：</strong>{{ currentCase.summary || '暂无摘要' }}
          </div>

          <div class="detail-content">
            <strong>详细内容：</strong>
            <div class="content-text">{{ currentCase.content || '暂无内容' }}</div>
          </div>

          <div class="detail-footer">
            <span>创建时间：{{ formatDateTime(currentCase.created_at) }}</span>
            <span>发布时间：{{ formatDateTime(currentCase.published_at) }}</span>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- FAQ 编辑对话框 -->
    <el-dialog
      v-model="faqDialogVisible"
      :title="isEditMode ? '编辑常见问题' : '新增常见问题'"
      width="600px"
      @close="handleFAQDialogClose"
    >
      <el-form
        ref="faqFormRef"
        :model="faqForm"
        :rules="faqFormRules"
        label-width="100px"
      >
        <el-form-item label="问题" prop="question">
          <el-input
            v-model="faqForm.question"
            type="textarea"
            placeholder="请输入问题"
            :rows="2"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="答案" prop="answer">
          <el-input
            v-model="faqForm.answer"
            type="textarea"
            placeholder="请输入答案"
            :rows="5"
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="问题分类" prop="category">
          <el-select v-model="faqForm.category" placeholder="请选择分类">
            <el-option label="订单相关" value="order" />
            <el-option label="支付相关" value="payment" />
            <el-option label="物流相关" value="shipping" />
            <el-option label="商品相关" value="product" />
            <el-option label="退换货" value="return" />
            <el-option label="其他问题" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序值" prop="sort_order">
          <el-input-number
            v-model="faqForm.sort_order"
            :min="0"
            :max="9999"
            placeholder="数字越大越靠前"
          />
          <span class="form-tip">数字越大越靠前</span>
        </el-form-item>

        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="faqForm.is_active" />
          <span class="form-tip">{{ faqForm.is_active ? '启用' : '禁用' }}</span>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="faqDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveFAQ" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, View, Edit, Delete,
  Document, CircleCheck, QuestionFilled, Picture, User
} from '@element-plus/icons-vue'
import {
  getCasesListApi,
  getCaseDetailApi,
  createCaseApi,
  updateCaseApi,
  deleteCaseApi,
  getFAQListApi,
  createFAQApi,
  updateFAQApi,
  patchFAQApi,
  deleteFAQApi,
  getCaseStatusLabel,
  getCaseStatusType,
  getFAQCategoryLabel,
  getFAQCategoryType
} from '@/api/modules/content'

// 当前选项卡
const activeTab = ref('cases')

// 统计数据
const stats = reactive({
  totalCases: 0,
  publishedCases: 0,
  totalFAQs: 0,
  activeFAQs: 0
})

// 案例列表
const caseLoading = ref(false)
const caseList = ref([])
const caseFilter = reactive({
  search: '',
  status: null
})
const casePagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// FAQ 列表
const faqLoading = ref(false)
const faqList = ref([])
const faqFilter = reactive({
  search: '',
  category: null,
  isActive: null
})
const faqPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 案例编辑
const caseDialogVisible = ref(false)
const caseViewDialogVisible = ref(false)
const isEditMode = ref(false)
const saving = ref(false)
const caseFormRef = ref(null)
const currentCase = ref(null)
const caseForm = reactive({
  title: '',
  summary: '',
  content: '',
  cover_image: '',
  author: '',
  status: 'draft',
  sort_order: 0,
  published_at: null
})

const caseFormRules = {
  title: [
    { required: true, message: '请输入案例标题', trigger: 'blur' }
  ],
  summary: [
    { required: true, message: '请输入案例摘要', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入详细内容', trigger: 'blur' }
  ]
}

// FAQ 编辑
const faqDialogVisible = ref(false)
const faqFormRef = ref(null)
const currentFAQId = ref(null)
const faqForm = reactive({
  question: '',
  answer: '',
  category: 'order',
  sort_order: 0,
  is_active: true
})

const faqFormRules = {
  question: [
    { required: true, message: '请输入问题', trigger: 'blur' }
  ],
  answer: [
    { required: true, message: '请输入答案', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择问题分类', trigger: 'change' }
  ]
}

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取案例列表
const fetchCaseList = async () => {
  caseLoading.value = true
  try {
    const params = {
      page: casePagination.page,
      page_size: casePagination.pageSize
    }

    if (caseFilter.search) params.search = caseFilter.search
    if (caseFilter.status) params.status = caseFilter.status

    const response = await getCasesListApi(params)
    caseList.value = response.results || []
    casePagination.total = response.count || 0

    // 更新统计
    stats.totalCases = response.count || 0
    stats.publishedCases = caseList.value.filter(c => c.status === 'published').length
  } catch (error) {
    ElMessage.error('获取案例列表失败')
  } finally {
    caseLoading.value = false
  }
}

// 获取 FAQ 列表
const fetchFAQList = async () => {
  faqLoading.value = true
  try {
    const params = {
      page: faqPagination.page,
      page_size: faqPagination.pageSize
    }

    if (faqFilter.search) params.search = faqFilter.search
    if (faqFilter.category) params.category = faqFilter.category
    if (faqFilter.isActive !== null) params.is_active = faqFilter.isActive

    const response = await getFAQListApi(params)
    faqList.value = response.results || []
    faqPagination.total = response.count || 0

    // 更新统计
    stats.totalFAQs = response.count || 0
    stats.activeFAQs = faqList.value.filter(f => f.is_active).length
  } catch (error) {
    ElMessage.error('获取 FAQ 列表失败')
  } finally {
    faqLoading.value = false
  }
}

// 案例搜索
const handleCaseSearch = () => {
  casePagination.page = 1
  fetchCaseList()
}

const handleCaseReset = () => {
  Object.assign(caseFilter, {
    search: '',
    status: null
  })
  casePagination.page = 1
  fetchCaseList()
}

const handleCasePageChange = (page) => {
  casePagination.page = page
  fetchCaseList()
}

const handleCaseSizeChange = (size) => {
  casePagination.pageSize = size
  casePagination.page = 1
  fetchCaseList()
}

// FAQ 搜索
const handleFAQSearch = () => {
  faqPagination.page = 1
  fetchFAQList()
}

const handleFAQReset = () => {
  Object.assign(faqFilter, {
    search: '',
    category: null,
    isActive: null
  })
  faqPagination.page = 1
  fetchFAQList()
}

const handleFAQPageChange = (page) => {
  faqPagination.page = page
  fetchFAQList()
}

const handleFAQSizeChange = (size) => {
  faqPagination.pageSize = size
  faqPagination.page = 1
  fetchFAQList()
}

// 选项卡切换
const handleTabChange = (tab) => {
  if (tab === 'cases') {
    fetchCaseList()
  } else if (tab === 'faqs') {
    fetchFAQList()
  }
}

// 新增按钮
const handleAdd = () => {
  if (activeTab.value === 'cases') {
    handleAddCase()
  } else {
    handleAddFAQ()
  }
}

// 新增案例
const handleAddCase = () => {
  isEditMode.value = false
  Object.assign(caseForm, {
    title: '',
    summary: '',
    content: '',
    cover_image: '',
    author: '',
    status: 'draft',
    sort_order: 0,
    published_at: null
  })
  caseDialogVisible.value = true
}

// 编辑案例
const handleEditCase = (row) => {
  isEditMode.value = true
  currentCase.value = row
  Object.assign(caseForm, {
    title: row.title,
    summary: row.summary,
    content: row.content,
    cover_image: row.cover_image,
    author: row.author,
    status: row.status,
    sort_order: row.sort_order,
    published_at: row.published_at
  })
  caseDialogVisible.value = true
}

// 保存案例
const handleSaveCase = async () => {
  try {
    await caseFormRef.value.validate()
    saving.value = true

    if (isEditMode.value) {
      await updateCaseApi(currentCase.value?.id, caseForm)
      ElMessage.success('更新成功')
    } else {
      await createCaseApi(caseForm)
      ElMessage.success('创建成功')
    }

    caseDialogVisible.value = false
    fetchCaseList()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    saving.value = false
  }
}

// 案例对话框关闭
const handleCaseDialogClose = () => {
  caseFormRef.value?.resetFields()
  currentCase.value = null
}

// 查看案例
const handleViewCase = async (row) => {
  try {
    const data = await getCaseDetailApi(row.id)
    currentCase.value = data
    caseViewDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取案例详情失败')
  }
}

// 删除案例
const handleDeleteCase = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除案例"${row.title}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteCaseApi(row.id)
    ElMessage.success('删除成功')
    fetchCaseList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 新增 FAQ
const handleAddFAQ = () => {
  isEditMode.value = false
  currentFAQId.value = null
  Object.assign(faqForm, {
    question: '',
    answer: '',
    category: 'order',
    sort_order: 0,
    is_active: true
  })
  faqDialogVisible.value = true
}

// 编辑 FAQ
const handleEditFAQ = (row) => {
  isEditMode.value = true
  currentFAQId.value = row.id
  Object.assign(faqForm, {
    question: row.question,
    answer: row.answer,
    category: row.category,
    sort_order: row.sort_order,
    is_active: row.is_active
  })
  faqDialogVisible.value = true
}

// 保存 FAQ
const handleSaveFAQ = async () => {
  try {
    await faqFormRef.value.validate()
    saving.value = true

    if (isEditMode.value) {
      await updateFAQApi(currentFAQId.value, faqForm)
      ElMessage.success('更新成功')
    } else {
      await createFAQApi(faqForm)
      ElMessage.success('创建成功')
    }

    faqDialogVisible.value = false
    fetchFAQList()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    saving.value = false
  }
}

// FAQ 对话框关闭
const handleFAQDialogClose = () => {
  faqFormRef.value?.resetFields()
  currentFAQId.value = null
}

// FAQ 排序权重变化
const handleFAQSortOrderChange = async (row) => {
  try {
    await patchFAQApi(row.id, { sort_order: row.sort_order })
    ElMessage.success('排序更新成功')
    fetchFAQList()
  } catch (error) {
    ElMessage.error('排序更新失败')
  }
}

// FAQ 状态切换
const handleFAQStatusChange = async (row) => {
  try {
    await patchFAQApi(row.id, { is_active: row.is_active })
    ElMessage.success(row.is_active ? '已启用' : '已禁用')
    fetchFAQList()
  } catch (error) {
    row.is_active = !row.is_active // 回滚状态
    ElMessage.error('状态更新失败')
  }
}

// 删除 FAQ
const handleDeleteFAQ = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除该问题吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteFAQApi(row.id)
    ElMessage.success('删除成功')
    fetchFAQList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchCaseList()
  fetchFAQList()
})
</script>

<style scoped>
.content-manage-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   页面标题区
   ======================================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.page-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* ========================================
   统计卡片
   ======================================== */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

/* ========================================
   选项卡
   ======================================== */
.content-tabs {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.content-tabs :deep(.el-tabs__header) {
  margin-bottom: 20px;
}

/* ========================================
   筛选工具栏
   ======================================== */
.filter-toolbar {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  flex-wrap: wrap;
}

.search-input {
  width: 280px;
}

.filter-select {
  width: 160px;
}

/* ========================================
   表格容器
   ======================================== */
.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

/* ========================================
   案例相关
   ======================================== */
.cover-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.cover-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.case-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.case-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.case-summary {
  font-size: 12px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.case-meta {
  display: flex;
  gap: 16px;
}

.meta-item {
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}

.sort-text {
  font-size: 13px;
  color: #64748b;
}

/* ========================================
   FAQ 相关
   ======================================== */
.question-text {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.answer-text {
  font-size: 13px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* ========================================
   表单
   ======================================== */
.form-tip {
  margin-left: 12px;
  font-size: 12px;
  color: #94a3b8;
}

.image-preview {
  margin-top: 12px;
}

/* ========================================
   案例详情
   ======================================== */
.case-detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-cover {
  width: 100%;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  background: #f1f5f9;
}

.cover-large {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder-large {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 48px;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.detail-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.detail-summary,
.detail-content {
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 14px;
  color: #475569;
}

.content-text {
  margin-top: 8px;
  white-space: pre-wrap;
  line-height: 1.6;
}

.detail-footer {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: #94a3b8;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

/* ========================================
   分页
   ======================================== */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px;
}

/* ========================================
   响应式设计
   ======================================== */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    width: 100%;
    justify-content: stretch;
  }

  .header-actions .el-button {
    flex: 1;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .filter-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-left {
    flex-direction: column;
    width: 100%;
  }

  .search-input,
  .filter-select {
    width: 100%;
  }

  .detail-meta {
    flex-direction: column;
    gap: 8px;
  }

  .detail-footer {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
