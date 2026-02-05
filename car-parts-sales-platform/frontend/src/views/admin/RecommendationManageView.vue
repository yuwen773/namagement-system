<template>
  <div class="recommendation-manage-view">
    <!-- 页面标题区 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">推荐管理</h1>
        <p class="page-subtitle">管理推荐规则和推荐商品配置</p>
      </div>
      <div class="header-actions">
        <el-button :icon="DataAnalysis" @click="showStatsDialog = true">
          效果监控
        </el-button>
        <el-button type="primary" :icon="Plus" @click="handleAddRule">
          新增规则
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);">
          <el-icon :size="24"><Trophy /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalRules }}</div>
          <div class="stat-label">推荐规则</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);">
          <el-icon :size="24"><CircleCheck /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.activeRules }}</div>
          <div class="stat-label">启用中</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
          <el-icon :size="24"><Goods /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalProducts }}</div>
          <div class="stat-label">推荐商品</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
          <el-icon :size="24"><Star /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.hotProducts }}</div>
          <div class="stat-label">热门推荐</div>
        </div>
      </div>
    </div>

    <!-- 选项卡 -->
    <el-tabs v-model="activeTab" class="content-tabs" @tab-change="handleTabChange">
      <!-- 推荐规则管理 -->
      <el-tab-pane label="推荐规则" name="rules">
        <!-- 筛选工具栏 -->
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-input
              v-model="ruleFilter.search"
              placeholder="搜索规则名称..."
              class="search-input"
              clearable
              @clear="handleRuleSearch"
              @keyup.enter="handleRuleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>

            <el-select v-model="ruleFilter.type" placeholder="规则类型" clearable class="filter-select">
              <el-option label="热门推荐" value="hot" />
              <el-option label="新品推荐" value="new" />
              <el-option label="个性化推荐" value="personalized" />
              <el-option label="分类推荐" value="category" />
            </el-select>

            <el-select v-model="ruleFilter.status" placeholder="状态" clearable class="filter-select">
              <el-option label="启用" :value="true" />
              <el-option label="禁用" :value="false" />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleRuleSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleRuleReset">重置</el-button>
          </div>
        </div>

        <!-- 规则列表 -->
        <div class="table-container">
          <el-table
            v-loading="ruleLoading"
            :data="ruleList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="规则信息" min-width="280">
              <template #default="{ row }">
                <div class="rule-info">
                  <div class="rule-badge" :class="`type-${row.rule_type}`">
                    {{ getRuleTypeLabel(row.rule_type) }}
                  </div>
                  <div class="rule-detail">
                    <div class="rule-name">{{ row.name }}</div>
                    <div class="rule-desc">{{ row.description || '暂无描述' }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="优先级" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)" size="small">
                  {{ row.priority }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="商品限制" width="120" align="center">
              <template #default="{ row }">
                <span class="limit-text">{{ row.limit || '-' }} 个</span>
              </template>
            </el-table-column>

            <el-table-column label="已配置商品" width="120" align="center">
              <template #default="{ row }">
                <el-button link type="primary" :icon="View" @click="handleViewProducts(row)">
                  {{ row.product_count || 0 }} 个
                </el-button>
              </template>
            </el-table-column>

            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-switch
                  v-model="row.is_active"
                  @change="handleStatusChange(row)"
                />
              </template>
            </el-table-column>

            <el-table-column label="创建时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.created_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="Edit" @click="handleEditRule(row)">
                  编辑
                </el-button>
                <el-button link type="primary" :icon="Plus" @click="handleAddProduct(row)">
                  添加商品
                </el-button>
                <el-button link type="danger" :icon="Delete" @click="handleDeleteRule(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="rulePagination.page"
              v-model:page-size="rulePagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="rulePagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleRuleSizeChange"
              @current-change="handleRulePageChange"
            />
          </div>
        </div>
      </el-tab-pane>

      <!-- 推荐商品管理 -->
      <el-tab-pane label="推荐商品" name="products">
        <!-- 筛选工具栏 -->
        <div class="filter-toolbar">
          <div class="filter-left">
            <el-select
              v-model="productFilter.ruleId"
              placeholder="选择推荐规则"
              clearable
              class="filter-select"
              @change="handleProductSearch"
            >
              <el-option
                v-for="rule in allRules"
                :key="rule.id"
                :label="rule.name"
                :value="rule.id"
              />
            </el-select>

            <el-button type="primary" :icon="Search" @click="handleProductSearch">搜索</el-button>
            <el-button :icon="Refresh" @click="handleProductReset">重置</el-button>
          </div>
        </div>

        <!-- 商品列表 -->
        <div class="table-container">
          <el-table
            v-loading="productLoading"
            :data="productList"
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: '600' }"
          >
            <el-table-column label="商品信息" min-width="300">
              <template #default="{ row }">
                <div class="product-info">
                  <el-image
                    v-if="row.product?.main_image"
                    :src="row.product.main_image"
                    fit="cover"
                    class="product-image"
                    :preview-src-list="[row.product.main_image]"
                  />
                  <div v-else class="product-image-placeholder">
                    <el-icon><Picture /></el-icon>
                  </div>
                  <div class="product-detail">
                    <div class="product-name">{{ row.product?.name || '-' }}</div>
                    <div class="product-category">{{ row.product?.category_name || '-' }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>

            <el-table-column label="价格" width="120">
              <template #default="{ row }">
                <span class="price-text">¥{{ row.product?.price || '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="所属规则" width="150">
              <template #default="{ row }">
                <span>{{ row.rule_name || '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="排序权重" width="120" align="center">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.sort_order"
                  :min="0"
                  :max="9999"
                  size="small"
                  controls-position="right"
                  @change="handleSortOrderChange(row)"
                />
              </template>
            </el-table-column>

            <el-table-column label="备注" width="200">
              <template #default="{ row }">
                <span class="remark-text">{{ row.remark || '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="添加时间" width="170">
              <template #default="{ row }">
                <span>{{ formatDateTime(row.created_at) }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button link type="danger" :icon="Delete" @click="handleDeleteProduct(row)">
                  移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="productPagination.page"
              v-model:page-size="productPagination.pageSize"
              :page-sizes="[10, 30, 50]"
              :total="productPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleProductSizeChange"
              @current-change="handleProductPageChange"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 规则编辑对话框 -->
    <el-dialog
      v-model="ruleDialogVisible"
      :title="isEditMode ? '编辑推荐规则' : '新增推荐规则'"
      width="600px"
      @close="handleRuleDialogClose"
    >
      <el-form
        ref="ruleFormRef"
        :model="ruleForm"
        :rules="ruleFormRules"
        label-width="120px"
      >
        <el-form-item label="规则名称" prop="name">
          <el-input
            v-model="ruleForm.name"
            placeholder="请输入规则名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="规则类型" prop="rule_type">
          <el-select
            v-model="ruleForm.rule_type"
            placeholder="请选择规则类型"
            :disabled="isEditMode"
          >
            <el-option label="热门推荐" value="hot">
              <div class="option-item">
                <span class="option-label">热门推荐</span>
                <span class="option-desc">根据销量和浏览量推荐</span>
              </div>
            </el-option>
            <el-option label="新品推荐" value="new">
              <div class="option-item">
                <span class="option-label">新品推荐</span>
                <span class="option-desc">根据上架时间推荐</span>
              </div>
            </el-option>
            <el-option label="个性化推荐" value="personalized">
              <div class="option-item">
                <span class="option-label">个性化推荐</span>
                <span class="option-desc">基于用户行为推荐</span>
              </div>
            </el-option>
            <el-option label="分类推荐" value="category">
              <div class="option-item">
                <span class="option-label">分类推荐</span>
                <span class="option-desc">按商品分类推荐</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="规则描述" prop="description">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            placeholder="请输入规则描述"
            :rows="3"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="优先级" prop="priority">
          <el-input-number
            v-model="ruleForm.priority"
            :min="0"
            :max="999"
            placeholder="数字越大优先级越高"
          />
          <span class="form-tip">数字越大优先级越高</span>
        </el-form-item>

        <el-form-item label="商品数量限制" prop="limit">
          <el-input-number
            v-model="ruleForm.limit"
            :min="1"
            :max="100"
            placeholder="最多返回商品数"
          />
          <span class="form-tip">最多返回的商品数量</span>
        </el-form-item>

        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="ruleForm.is_active" />
          <span class="form-tip">{{ ruleForm.is_active ? '启用' : '禁用' }}</span>
        </el-form-item>

        <!-- 规则配置（JSON） -->
        <el-form-item label="规则配置">
          <el-input
            v-model="configJsonText"
            type="textarea"
            placeholder='{"min_sales": 100, "min_views": 1000}'
            :rows="4"
          />
          <div class="form-tip" style="margin-top: 4px;">
            <div>配置示例：</div>
            <div>热门推荐：{"min_sales": 100, "min_views": 1000}</div>
            <div>新品推荐：{"days": 30}</div>
            <div>个性化：{"weight_view": 0.3, "weight_buy": 0.7}</div>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveRule" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 添加商品对话框 -->
    <el-dialog
      v-model="addProductDialogVisible"
      title="添加推荐商品"
      width="800px"
    >
      <div class="add-product-content">
        <el-input
          v-model="productSearch"
          placeholder="搜索商品名称..."
          class="product-search-input"
          clearable
          @clear="handleProductSelectSearch"
          @keyup.enter="handleProductSelectSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-table
          v-loading="availableProductsLoading"
          :data="availableProducts"
          style="width: 100%; margin-top: 16px"
          @selection-change="handleProductSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column label="商品信息" min-width="250">
            <template #default="{ row }">
              <div class="product-info">
                <el-image
                  v-if="row.main_image"
                  :src="row.main_image"
                  fit="cover"
                  class="product-image"
                />
                <div v-else class="product-image-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
                <div class="product-detail">
                  <div class="product-name">{{ row.name }}</div>
                  <div class="product-price">¥{{ row.price }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="分类" prop="category_name" width="120" />
          <el-table-column label="销量" prop="sales_count" width="80" align="center" />
          <el-table-column label="库存" prop="stock_quantity" width="80" align="center" />
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="availableProductPagination.page"
            v-model:page-size="availableProductPagination.pageSize"
            :total="availableProductPagination.total"
            layout="total, prev, pager, next"
            @current-change="loadAvailableProducts"
          />
        </div>
      </div>

      <template #footer>
        <el-button @click="addProductDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleConfirmAddProducts"
          :loading="addingProducts"
          :disabled="selectedProducts.length === 0"
        >
          添加选中商品 ({{ selectedProducts.length }})
        </el-button>
      </template>
    </el-dialog>

    <!-- 查看商品对话框 -->
    <el-dialog
      v-model="viewProductsDialogVisible"
      title="规则推荐商品"
      width="900px"
    >
      <div class="view-products-content">
        <div class="rule-info-summary">
          <span><strong>规则：</strong>{{ currentRule?.name }}</span>
          <span><strong>类型：</strong>{{ getRuleTypeLabel(currentRule?.rule_type) }}</span>
          <span><strong>限制：</strong>{{ currentRule?.limit }} 个</span>
        </div>

        <el-table
          v-loading="ruleProductsLoading"
          :data="ruleProducts"
          style="width: 100%; margin-top: 16px"
        >
          <el-table-column label="商品信息" min-width="250">
            <template #default="{ row }">
              <div class="product-info">
                <el-image
                  v-if="row.product?.main_image"
                  :src="row.product.main_image"
                  fit="cover"
                  class="product-image"
                />
                <div v-else class="product-image-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
                <div class="product-detail">
                  <div class="product-name">{{ row.product?.name }}</div>
                  <div class="product-price">¥{{ row.product?.price }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="排序权重" prop="sort_order" width="100" align="center" />
          <el-table-column label="备注" prop="remark" min-width="150" />
          <el-table-column label="操作" width="80" fixed="right">
            <template #default="{ row }">
              <el-button link type="danger" :icon="Delete" @click="handleDeleteProduct(row)">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="ruleProductsPagination.page"
            v-model:page-size="ruleProductsPagination.pageSize"
            :total="ruleProductsPagination.total"
            layout="total, prev, pager, next"
            @current-change="loadRuleProducts"
          />
        </div>
      </div>
    </el-dialog>

    <!-- 效果监控对话框 -->
    <el-dialog
      v-model="showStatsDialog"
      title="推荐效果监控"
      width="700px"
    >
      <div class="stats-dialog-content">
        <div class="stats-section">
          <h3>规则统计</h3>
          <div class="stats-list">
            <div class="stats-item">
              <span class="stats-label">总规则数：</span>
              <span class="stats-value">{{ stats.totalRules }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">启用规则：</span>
              <span class="stats-value">{{ stats.activeRules }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">禁用规则：</span>
              <span class="stats-value">{{ stats.inactiveRules }}</span>
            </div>
          </div>
        </div>

        <div class="stats-section">
          <h3>推荐商品统计</h3>
          <div class="stats-list">
            <div class="stats-item">
              <span class="stats-label">总推荐商品：</span>
              <span class="stats-value">{{ stats.totalProducts }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">热门推荐：</span>
              <span class="stats-value">{{ stats.hotProducts }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">新品推荐：</span>
              <span class="stats-value">{{ stats.newProducts }}</span>
            </div>
            <div class="stats-item">
              <span class="stats-label">个性化推荐：</span>
              <span class="stats-value">{{ stats.personalizedProducts }}</span>
            </div>
          </div>
        </div>

        <div class="stats-section">
          <h3>规则类型分布</h3>
          <div class="rule-type-distribution">
            <div
              v-for="item in ruleTypeDistribution"
              :key="item.type"
              class="distribution-item"
            >
              <div class="distribution-label">{{ item.label }}</div>
              <div class="distribution-bar">
                <div
                  class="distribution-fill"
                  :style="{ width: item.percent + '%' }"
                ></div>
              </div>
              <div class="distribution-value">{{ item.count }}</div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, Refresh, View, Edit, Delete, DataAnalysis,
  Trophy, CircleCheck, Goods, Star, Picture
} from '@element-plus/icons-vue'
import {
  getRecommendationRules,
  getActiveRecommendationRules,
  createRecommendationRule,
  updateRecommendationRule,
  patchRecommendationRule,
  deleteRecommendationRule,
  getRecommendedProducts,
  addRecommendedProduct,
  updateRecommendedProductSortOrder,
  deleteRecommendedProduct,
  getRuleTypeLabel
} from '@/api/modules/recommendation'
import { getProductListApi } from '@/api/modules/product'

// 当前选项卡
const activeTab = ref('rules')

// 统计数据
const stats = reactive({
  totalRules: 0,
  activeRules: 0,
  inactiveRules: 0,
  totalProducts: 0,
  hotProducts: 0,
  newProducts: 0,
  personalizedProducts: 0
})

const showStatsDialog = ref(false)

// 规则类型分布
const ruleTypeDistribution = ref([])

// 推荐规则列表
const ruleLoading = ref(false)
const ruleList = ref([])
const allRules = ref([])
const ruleFilter = reactive({
  search: '',
  type: null,
  status: null
})
const rulePagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 推荐商品列表
const productLoading = ref(false)
const productList = ref([])
const productFilter = reactive({
  ruleId: null
})
const productPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 规则编辑
const ruleDialogVisible = ref(false)
const isEditMode = ref(false)
const saving = ref(false)
const ruleFormRef = ref(null)
const ruleForm = reactive({
  name: '',
  rule_type: 'hot',
  description: '',
  priority: 0,
  limit: 10,
  is_active: true,
  config: {}
})
const configJsonText = ref('')
const currentRuleId = ref(null)

const ruleFormRules = {
  name: [
    { required: true, message: '请输入规则名称', trigger: 'blur' }
  ],
  rule_type: [
    { required: true, message: '请选择规则类型', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请输入优先级', trigger: 'blur' }
  ],
  limit: [
    { required: true, message: '请输入商品数量限制', trigger: 'blur' }
  ]
}

// 添加商品
const addProductDialogVisible = ref(false)
const addingProducts = ref(false)
const productSearch = ref('')
const availableProductsLoading = ref(false)
const availableProducts = ref([])
const selectedProducts = ref([])
const currentRuleForProduct = ref(null)
const availableProductPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 查看商品
const viewProductsDialogVisible = ref(false)
const ruleProductsLoading = ref(false)
const ruleProducts = ref([])
const currentRule = ref(null)
const ruleProductsPagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

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

// 获取优先级类型
const getPriorityType = (priority) => {
  if (priority >= 80) return 'danger'
  if (priority >= 50) return 'warning'
  return 'info'
}

// 获取规则列表
const fetchRuleList = async () => {
  ruleLoading.value = true
  try {
    const params = {
      page: rulePagination.page,
      page_size: rulePagination.pageSize
    }

    if (ruleFilter.search) params.search = ruleFilter.search
    if (ruleFilter.type) params.rule_type = ruleFilter.type
    if (ruleFilter.status !== null) params.is_active = ruleFilter.status

    const response = await getRecommendationRules(params)
    ruleList.value = response.results || []
    rulePagination.total = response.count || 0

    updateStats(ruleList.value)
  } catch (error) {
    ElMessage.error('获取推荐规则列表失败')
  } finally {
    ruleLoading.value = false
  }
}

// 获取所有规则（用于筛选）
const fetchAllRules = async () => {
  try {
    const response = await getRecommendationRules({ page: 1, page_size: 1000 })
    allRules.value = response.results || []
  } catch (error) {
    console.error('获取所有规则失败', error)
  }
}

// 更新统计数据
const updateStats = (rules) => {
  stats.totalRules = rules.length
  stats.activeRules = rules.filter(r => r.is_active).length
  stats.inactiveRules = rules.filter(r => !r.is_active).length

  // 计算规则类型分布
  const typeCount = {}
  rules.forEach(r => {
    typeCount[r.rule_type] = (typeCount[r.rule_type] || 0) + 1
  })

  ruleTypeDistribution.value = Object.entries(typeCount).map(([type, count]) => ({
    type,
    label: getRuleTypeLabel(type),
    count,
    percent: Math.round((count / rules.length) * 100)
  }))
}

// 获取推荐商品列表
const fetchProductList = async () => {
  productLoading.value = true
  try {
    const params = {
      page: productPagination.page,
      page_size: productPagination.pageSize
    }

    if (productFilter.ruleId) params.rule = productFilter.ruleId

    const response = await getRecommendedProducts(params)
    productList.value = response.results || []
    productPagination.total = response.count || 0

    // 更新商品统计
    updateProductStats(productList.value)
  } catch (error) {
    ElMessage.error('获取推荐商品列表失败')
  } finally {
    productLoading.value = false
  }
}

// 更新商品统计
const updateProductStats = (products) => {
  stats.totalProducts = products.length
  stats.hotProducts = products.filter(p => p.rule_name?.includes('热门')).length
  stats.newProducts = products.filter(p => p.rule_name?.includes('新品')).length
  stats.personalizedProducts = products.filter(p => p.rule_name?.includes('个性化')).length
}

// 规则搜索
const handleRuleSearch = () => {
  rulePagination.page = 1
  fetchRuleList()
}

const handleRuleReset = () => {
  Object.assign(ruleFilter, {
    search: '',
    type: null,
    status: null
  })
  rulePagination.page = 1
  fetchRuleList()
}

const handleRulePageChange = (page) => {
  rulePagination.page = page
  fetchRuleList()
}

const handleRuleSizeChange = (size) => {
  rulePagination.pageSize = size
  rulePagination.page = 1
  fetchRuleList()
}

// 商品搜索
const handleProductSearch = () => {
  productPagination.page = 1
  fetchProductList()
}

const handleProductReset = () => {
  productFilter.ruleId = null
  productPagination.page = 1
  fetchProductList()
}

const handleProductPageChange = (page) => {
  productPagination.page = page
  fetchProductList()
}

const handleProductSizeChange = (size) => {
  productPagination.pageSize = size
  productPagination.page = 1
  fetchProductList()
}

// 选项卡切换
const handleTabChange = (tab) => {
  if (tab === 'rules') {
    fetchRuleList()
  } else if (tab === 'products') {
    fetchProductList()
  }
}

// 新增规则
const handleAddRule = () => {
  isEditMode.value = false
  currentRuleId.value = null
  Object.assign(ruleForm, {
    name: '',
    rule_type: 'hot',
    description: '',
    priority: 0,
    limit: 10,
    is_active: true,
    config: {}
  })
  configJsonText.value = ''
  ruleDialogVisible.value = true
}

// 编辑规则
const handleEditRule = (row) => {
  isEditMode.value = true
  currentRuleId.value = row.id
  Object.assign(ruleForm, {
    name: row.name,
    rule_type: row.rule_type,
    description: row.description || '',
    priority: row.priority,
    limit: row.limit,
    is_active: row.is_active,
    config: row.config || {}
  })
  configJsonText.value = JSON.stringify(row.config || {}, null, 2)
  ruleDialogVisible.value = true
}

// 保存规则
const handleSaveRule = async () => {
  try {
    await ruleFormRef.value.validate()
    saving.value = true

    // 解析配置 JSON
    let config = {}
    if (configJsonText.value.trim()) {
      try {
        config = JSON.parse(configJsonText.value)
      } catch (e) {
        ElMessage.error('规则配置 JSON 格式不正确')
        return
      }
    }

    const data = {
      ...ruleForm,
      config
    }

    if (isEditMode.value) {
      await updateRecommendationRule(currentRuleId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createRecommendationRule(data)
      ElMessage.success('创建成功')
    }

    ruleDialogVisible.value = false
    fetchRuleList()
  } catch (error) {
    ElMessage.error(isEditMode.value ? '更新失败' : '创建失败')
  } finally {
    saving.value = false
  }
}

// 规则对话框关闭
const handleRuleDialogClose = () => {
  ruleFormRef.value?.resetFields()
}

// 删除规则
const handleDeleteRule = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除推荐规则"${row.name}"吗？此操作将同时移除该规则下的所有推荐商品！`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteRecommendationRule(row.id)
    ElMessage.success('删除成功')
    fetchRuleList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 状态切换
const handleStatusChange = async (row) => {
  try {
    await patchRecommendationRule(row.id, { is_active: row.is_active })
    ElMessage.success(row.is_active ? '已启用' : '已禁用')
    fetchRuleList()
  } catch (error) {
    row.is_active = !row.is_active // 回滚状态
    ElMessage.error('状态更新失败')
  }
}

// 添加商品
const handleAddProduct = (row) => {
  currentRuleForProduct.value = row
  productSearch.value = ''
  selectedProducts.value = []
  availableProductPagination.page = 1
  addProductDialogVisible.value = true
  loadAvailableProducts()
}

// 加载可选商品列表
const loadAvailableProducts = async () => {
  availableProductsLoading.value = true
  try {
    const params = {
      page: availableProductPagination.page,
      page_size: availableProductPagination.pageSize,
      status: 'published'
    }

    if (productSearch.value) params.search = productSearch.value

    const response = await getProductListApi(params)
    availableProducts.value = response.results || []
    availableProductPagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取商品列表失败')
  } finally {
    availableProductsLoading.value = false
  }
}

// 商品搜索
const handleProductSelectSearch = () => {
  availableProductPagination.page = 1
  loadAvailableProducts()
}

// 商品选择变化
const handleProductSelectionChange = (selection) => {
  selectedProducts.value = selection
}

// 确认添加商品
const handleConfirmAddProducts = async () => {
  if (selectedProducts.value.length === 0) {
    ElMessage.warning('请选择要添加的商品')
    return
  }

  addingProducts.value = true
  try {
    const promises = selectedProducts.value.map(product =>
      addRecommendedProduct({
        rule: currentRuleForProduct.value.id,
        product: product.id,
        sort_order: 0
      })
    )

    await Promise.all(promises)
    ElMessage.success(`成功添加 ${selectedProducts.value.length} 个商品`)
    addProductDialogVisible.value = false
    fetchRuleList()
    fetchProductList()
  } catch (error) {
    ElMessage.error('添加商品失败')
  } finally {
    addingProducts.value = false
  }
}

// 查看规则商品
const handleViewProducts = async (row) => {
  currentRule.value = row
  ruleProductsPagination.page = 1
  viewProductsDialogVisible.value = true
  await loadRuleProducts()
}

// 加载规则商品
const loadRuleProducts = async () => {
  ruleProductsLoading.value = true
  try {
    const params = {
      page: ruleProductsPagination.page,
      page_size: ruleProductsPagination.pageSize,
      rule: currentRule.value.id
    }

    const response = await getRecommendedProducts(params)
    ruleProducts.value = response.results || []
    ruleProductsPagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取规则商品失败')
  } finally {
    ruleProductsLoading.value = false
  }
}

// 排序权重变化
const handleSortOrderChange = async (row) => {
  try {
    await updateRecommendedProductSortOrder(row.id, row.sort_order)
    ElMessage.success('排序更新成功')
    fetchProductList()
  } catch (error) {
    ElMessage.error('排序更新失败')
  }
}

// 删除推荐商品
const handleDeleteProduct = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确定要移除该推荐商品吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteRecommendedProduct(row.id)
    ElMessage.success('移除成功')
    fetchProductList()
    if (viewProductsDialogVisible.value) {
      loadRuleProducts()
    }
    if (ruleDialogVisible.value) {
      fetchRuleList()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchRuleList()
  fetchAllRules()
  fetchProductList()
})
</script>

<style scoped>
.recommendation-manage-view {
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
   规则信息
   ======================================== */
.rule-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rule-badge {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
  min-width: 80px;
  text-align: center;
}

.rule-badge.type-hot {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #fff;
}

.rule-badge.type-new {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: #fff;
}

.rule-badge.type-personalized {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #fff;
}

.rule-badge.type-category {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: #fff;
}

.rule-detail {
  flex: 1;
  min-width: 0;
}

.rule-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.rule-desc {
  font-size: 12px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========================================
   商品信息
   ======================================== */
.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-image {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  flex-shrink: 0;
  object-fit: cover;
}

.product-image-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  flex-shrink: 0;
}

.product-detail {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-category {
  font-size: 12px;
  color: #64748b;
}

.product-price {
  font-size: 14px;
  color: #f97316;
  font-weight: 600;
}

.price-text {
  font-size: 16px;
  font-weight: 700;
  color: #f97316;
}

.limit-text {
  font-size: 13px;
  color: #64748b;
}

.remark-text {
  font-size: 13px;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
  max-width: 200px;
}

/* ========================================
   表单提示
   ======================================== */
.form-tip {
  margin-left: 12px;
  font-size: 12px;
  color: #94a3b8;
}

/* ========================================
   下拉选项
   ======================================== */
.option-item {
  display: flex;
  flex-direction: column;
}

.option-label {
  font-weight: 500;
}

.option-desc {
  font-size: 12px;
  color: #94a3b8;
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
   添加商品对话框
   ======================================== */
.add-product-content {
  padding: 8px 0;
}

.product-search-input {
  width: 100%;
}

/* ========================================
   查看商品对话框
   ======================================== */
.view-products-content {
  padding: 8px 0;
}

.rule-info-summary {
  display: flex;
  gap: 24px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 14px;
  color: #475569;
}

/* ========================================
   统计对话框
   ======================================== */
.stats-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-section h3 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #1e293b;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.stats-label {
  color: #64748b;
}

.stats-value {
  font-weight: 600;
  color: #1e293b;
}

/* ========================================
   规则类型分布
   ======================================== */
.rule-type-distribution {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.distribution-label {
  width: 80px;
  font-size: 13px;
  color: #64748b;
}

.distribution-bar {
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.distribution-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.distribution-value {
  width: 40px;
  text-align: right;
  font-weight: 600;
  color: #1e293b;
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

  .rule-info-summary {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
