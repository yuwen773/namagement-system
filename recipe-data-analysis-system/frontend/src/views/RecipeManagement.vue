<template>
  <div class="recipe-management-page">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          菜谱管理
        </h1>
        <p class="page-subtitle">管理系统菜谱数据</p>
      </div>
      <div class="header-actions">
        <button @click="showImportDialog = true" class="action-btn import-btn">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          批量导入
        </button>
        <button @click="openCreateDialog" class="action-btn create-btn">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 6v6m0 0v6m0-6h6m-6 0H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          新增菜谱
        </button>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 搜索和筛选栏 -->
      <div class="toolbar">
        <div class="search-box">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索菜谱名称..."
            @keyup.enter="handleSearch"
          >
        </div>

        <div class="filter-group">
          <select v-model="filters.cuisine_type" @change="handleSearch" class="filter-select">
            <option value="">全部菜系</option>
            <option v-for="cuisine in cuisines" :key="cuisine.name" :value="cuisine.name">
              {{ cuisine.name }}
            </option>
          </select>
          <select v-model="filters.difficulty" @change="handleSearch" class="filter-select">
            <option value="">全部难度</option>
            <option value="easy">简单</option>
            <option value="medium">中等</option>
            <option value="hard">困难</option>
          </select>
          <select v-model="filters.scene_type" @change="handleSearch" class="filter-select">
            <option value="">全部场景</option>
            <option v-for="scene in scenes" :key="scene.name" :value="scene.name">
              {{ scene.name }}
            </option>
          </select>
          <select v-model="filters.target_audience" @change="handleSearch" class="filter-select">
            <option value="">全部人群</option>
            <option v-for="audience in audiences" :key="audience.name" :value="audience.name">
              {{ audience.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- 菜谱列表 -->
      <div v-loading="loading" class="recipe-list-container">
        <div v-if="recipeList.length === 0 && !loading" class="empty-state">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无菜谱数据</p>
        </div>

        <div v-else class="recipe-table-wrapper">
          <table class="recipe-table">
            <thead>
              <tr>
                <th>菜谱信息</th>
                <th>菜系</th>
                <th>难度</th>
                <th>场景</th>
                <th>时长</th>
                <th>数据</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="recipe in recipeList" :key="recipe.id">
                <td class="recipe-info-cell">
                  <div v-if="recipe.image_url" class="recipe-image">
                    <img :src="recipe.image_url" :alt="recipe.name">
                  </div>
                  <div v-else class="recipe-image-placeholder">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <div class="recipe-details">
                    <div class="recipe-name">{{ recipe.name }}</div>
                    <div class="recipe-meta">{{ recipe.flavor_tags || '无口味标签' }}</div>
                  </div>
                </td>
                <td class="tag-cell">
                  <span class="tag-badge cuisine">{{ recipe.cuisine_type || '-' }}</span>
                </td>
                <td class="tag-cell">
                  <span class="tag-badge" :class="recipe.difficulty">
                    {{ difficultyMap[recipe.difficulty] || recipe.difficulty }}
                  </span>
                </td>
                <td class="tag-cell">
                  <span class="tag-badge scene">{{ recipe.scene_type || '-' }}</span>
                </td>
                <td class="time-cell">
                  {{ recipe.cooking_time ? `${recipe.cooking_time} 分钟` : '-' }}
                </td>
                <td class="stats-cell">
                  <div class="stat-item">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5"/>
                      <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="1.5"/>
                    </svg>
                    {{ recipe.view_count || 0 }}
                  </div>
                  <div class="stat-item">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" stroke="currentColor" stroke-width="1.5"/>
                    </svg>
                    {{ recipe.favorite_count || 0 }}
                  </div>
                </td>
                <td class="action-cell">
                  <button @click="openEditDialog(recipe)" class="icon-btn edit-btn" title="编辑">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                  <button @click="handleDelete(recipe)" class="icon-btn delete-btn" title="删除">
                    <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalCount > 0" class="pagination">
        <button @click="handlePrevPage" :disabled="currentPage === 1" class="pagination-btn">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 15l-4-4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          上一页
        </button>
        <span class="pagination-info">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="handleNextPage" :disabled="currentPage >= totalPages" class="pagination-btn">
          下一页
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 15l4-4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="showEditDialog"
      :title="isEditMode ? '编辑菜谱' : '新增菜谱'"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="菜谱名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入菜谱名称" />
        </el-form-item>
        <el-form-item label="菜系分类" prop="cuisine_type">
          <el-select v-model="formData.cuisine_type" placeholder="请选择菜系">
            <el-option v-for="cuisine in cuisines" :key="cuisine.name" :label="cuisine.name" :value="cuisine.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度等级" prop="difficulty">
          <el-select v-model="formData.difficulty" placeholder="请选择难度">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="场景分类" prop="scene_type">
          <el-select v-model="formData.scene_type" placeholder="请选择场景">
            <el-option v-for="scene in scenes" :key="scene.name" :label="scene.name" :value="scene.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="适用人群" prop="target_audience">
          <el-select v-model="formData.target_audience" placeholder="请选择人群">
            <el-option v-for="audience in audiences" :key="audience.name" :label="audience.name" :value="audience.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="烹饪时长" prop="cooking_time">
          <el-input-number v-model="formData.cooking_time" :min="1" :max="999" controls-position="right" />
          <span class="unit-text">分钟</span>
        </el-form-item>
        <el-form-item label="成品图片" prop="image_url">
          <el-input v-model="formData.image_url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="口味标签" prop="flavor_tags">
          <el-input v-model="formData.flavor_tags" placeholder="多个标签用逗号分隔，如：辣,甜" />
        </el-form-item>
        <el-form-item label="制作步骤" prop="steps">
          <el-input v-model="formData.steps" type="textarea" :rows="6" placeholder="请输入制作步骤" />
        </el-form-item>
        <el-form-item label="食材列表">
          <div class="ingredients-editor">
            <div v-for="(ing, index) in formData.ingredients" :key="index" class="ingredient-row">
              <el-select v-model="ing.ingredient" placeholder="选择食材" class="ingredient-select" filterable>
                <el-option
                  v-for="item in ingredientsList"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
              <span class="ingredient-name-display">{{ ing.ingredient_name }}</span>
              <el-input v-model="ing.amount" placeholder="用量" class="ingredient-amount-input" />
              <el-input-number v-model="ing.sort_order" :min="1" placeholder="排序" controls-position="right" class="ingredient-order-input" />
              <el-button @click="removeIngredient(index)" type="danger" text>删除</el-button>
            </div>
            <el-button @click="addIngredient" type="primary" text>+ 添加食材</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog
      v-model="showImportDialog"
      title="批量导入菜谱"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="import-dialog-content">
        <el-alert
          title="支持 CSV 或 JSON 格式文件"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 1rem;"
        />
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          accept=".csv,.json"
          drag
        >
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="upload-icon">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              JSON 文件需为数组格式，CSV 文件第一行为表头
            </div>
          </template>
        </el-upload>
      </div>
      <template #footer>
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button type="primary" @click="handleImport" :loading="importing" :disabled="!importFile">开始导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminRecipeList, createRecipe, updateRecipe, deleteRecipe, importRecipes } from '@/api/recipes'
import { getCategories, getIngredients } from '@/api/recipes'

// 状态
const loading = ref(false)
const recipeList = ref([])
const searchQuery = ref('')
const filters = ref({
  cuisine_type: '',
  difficulty: '',
  scene_type: '',
  target_audience: ''
})
const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)

// 分类数据
const cuisines = ref([])
const scenes = ref([])
const audiences = ref([])
const ingredientsList = ref([])

// 对话框状态
const showEditDialog = ref(false)
const showImportDialog = ref(false)
const isEditMode = ref(false)
const submitting = ref(false)
const importing = ref(false)
const formRef = ref(null)
const uploadRef = ref(null)
const importFile = ref(null)

// 表单数据
const formData = ref({
  name: '',
  cuisine_type: '',
  difficulty: 'medium',
  scene_type: '',
  target_audience: '',
  cooking_time: 30,
  image_url: '',
  flavor_tags: '',
  steps: '',
  ingredients: []
})

const editingRecipeId = ref(null)

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入菜谱名称', trigger: 'blur' }]
}

// 难度映射
const difficultyMap = {
  easy: '简单',
  medium: '中等',
  hard: '困难'
}

// 总页数
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))

// 获取分类数据
const fetchCategories = async () => {
  try {
    const [cuisineRes, sceneRes, crowdRes] = await Promise.all([
      getCategories({ type: 'cuisine' }),
      getCategories({ type: 'scene' }),
      getCategories({ type: 'crowd' })
    ])
    cuisines.value = cuisineRes.data || []
    scenes.value = sceneRes.data || []
    audiences.value = crowdRes.data || []
  } catch (error) {
    console.error('获取分类数据失败:', error)
  }
}

// 获取食材列表
const fetchIngredients = async () => {
  try {
    const response = await getIngredients({ page_size: 1000 })
    ingredientsList.value = response.data?.results || response.data || []
  } catch (error) {
    console.error('获取食材列表失败:', error)
  }
}

// 获取菜谱列表
const fetchRecipeList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (filters.value.cuisine_type) {
      params.cuisine_type = filters.value.cuisine_type
    }
    if (filters.value.difficulty) {
      params.difficulty = filters.value.difficulty
    }
    if (filters.value.scene_type) {
      params.scene_type = filters.value.scene_type
    }
    if (filters.value.target_audience) {
      params.target_audience = filters.value.target_audience
    }

    const response = await getAdminRecipeList(params)
    recipeList.value = response.data.results || []
    totalCount.value = response.data.count || 0
  } catch (error) {
    ElMessage.error(error.message || '获取菜谱列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchRecipeList()
}

// 上一页
const handlePrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchRecipeList()
  }
}

// 下一页
const handleNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchRecipeList()
  }
}

// 打开新增对话框
const openCreateDialog = () => {
  isEditMode.value = false
  resetFormData()
  showEditDialog.value = true
}

// 打开编辑对话框
const openEditDialog = async (recipe) => {
  isEditMode.value = true
  editingRecipeId.value = recipe.id

  // 确保食材列表已加载（用于新增时选择）
  if (ingredientsList.value.length === 0) {
    await fetchIngredients()
  }

  formData.value = {
    name: recipe.name || '',
    cuisine_type: recipe.cuisine_type || '',
    difficulty: recipe.difficulty || 'medium',
    scene_type: recipe.scene_type || '',
    target_audience: recipe.target_audience || '',
    cooking_time: recipe.cooking_time || 30,
    image_url: recipe.image_url || '',
    flavor_tags: recipe.flavor_tags || '',
    steps: recipe.steps || '',
    ingredients: recipe.ingredients || []
  }
  showEditDialog.value = true
}

// 重置表单数据
const resetFormData = () => {
  formData.value = {
    name: '',
    cuisine_type: '',
    difficulty: 'medium',
    scene_type: '',
    target_audience: '',
    cooking_time: 30,
    image_url: '',
    flavor_tags: '',
    steps: '',
    ingredients: []
  }
  editingRecipeId.value = null
}

// 添加食材
const addIngredient = () => {
  formData.value.ingredients.push({
    ingredient: null,
    ingredient_name: '',
    amount: '',
    sort_order: formData.value.ingredients.length + 1
  })
}

// 删除食材
const removeIngredient = (index) => {
  formData.value.ingredients.splice(index, 1)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitting.value = true
  try {
    if (isEditMode.value) {
      await updateRecipe(editingRecipeId.value, formData.value)
      ElMessage.success('菜谱更新成功')
    } else {
      await createRecipe(formData.value)
      ElMessage.success('菜谱创建成功')
    }
    showEditDialog.value = false
    fetchRecipeList()
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitting.value = false
  }
}

// 删除菜谱
const handleDelete = async (recipe) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除菜谱 "${recipe.name}" 吗？删除后相关的收藏记录也会被删除。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteRecipe(recipe.id)
    ElMessage.success(`菜谱 "${recipe.name}" 已删除`)
    fetchRecipeList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 文件变化
const handleFileChange = (file) => {
  importFile.value = file.raw
}

// 文件移除
const handleFileRemove = () => {
  importFile.value = null
}

// 导入
const handleImport = async () => {
  if (!importFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  importing.value = true
  try {
    const response = await importRecipes(importFile.value)
    const { success_count, failed_count, failed_records } = response.data

    if (failed_count > 0) {
      ElMessageBox.alert(
        `成功导入 ${success_count} 条，失败 ${failed_count} 条。${failed_records.length > 0 ? '失败原因：' + failed_records.map(r => r.error).join('; ') : ''}`,
        '导入完成',
        { type: 'warning' }
      )
    } else {
      ElMessage.success(`成功导入 ${success_count} 条菜谱`)
    }

    showImportDialog.value = false
    uploadRef.value?.clearFiles()
    importFile.value = null
    fetchRecipeList()
  } catch (error) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchCategories()
  fetchIngredients()
  fetchRecipeList()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.recipe-management-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%);
  padding-top: 80px;
  font-family: 'DM Sans', sans-serif;
}

/* 页面头部 */
.page-header {
  background: white;
  border-bottom: 1px solid #f0ebe3;
  padding: 2rem 2rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-family: 'Noto Serif SC', serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #3d2914;
  margin: 0 0 0.5rem 0;
}

.page-title svg {
  width: 32px;
  height: 32px;
  color: #c2622e;
}

.page-subtitle {
  font-size: 0.95rem;
  color: #8b7355;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* 内容区域 */
.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* 工具栏 */
.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
  background: white;
  border: 1.5px solid #e5ddd3;
  border-radius: 12px;
  padding: 0 1rem;
  transition: border-color 0.2s ease;
}

.search-box:focus-within {
  border-color: #c2622e;
}

.search-box svg {
  width: 18px;
  height: 18px;
  color: #a89078;
  flex-shrink: 0;
}

.search-box input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0.75rem;
  font-size: 0.95rem;
  font-family: inherit;
  color: #3d2914;
  background: transparent;
}

.search-box input::placeholder {
  color: #b8a99a;
}

.filter-group {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1.5px solid #e5ddd3;
  border-radius: 12px;
  font-size: 0.9rem;
  font-family: inherit;
  color: #3d2914;
  background: white;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s ease;
  min-width: 120px;
}

.filter-select:hover {
  border-color: #d4c4b0;
}

.filter-select:focus {
  border-color: #c2622e;
}

/* 菜谱列表容器 */
.recipe-list-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(61, 41, 20, 0.06);
  min-height: 400px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #a89078;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1rem;
  margin: 0;
}

/* 表格包装器 */
.recipe-table-wrapper {
  overflow-x: auto;
}

.recipe-table {
  width: 100%;
  border-collapse: collapse;
}

.recipe-table thead {
  background: #faf8f5;
}

.recipe-table th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b5c4d;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #f0ebe3;
  white-space: nowrap;
}

.recipe-table td {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f5f0e8;
}

.recipe-table tr:last-child td {
  border-bottom: none;
}

.recipe-table tbody tr {
  transition: background-color 0.15s ease;
}

.recipe-table tbody tr:hover {
  background: #faf8f5;
}

/* 菜谱信息单元格 */
.recipe-info-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 300px;
}

.recipe-image {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.recipe-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recipe-image-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  background: linear-gradient(135deg, #f5f0e8 0%, #ebe4d8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.recipe-image-placeholder svg {
  width: 24px;
  height: 24px;
  color: #a89078;
}

.recipe-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.recipe-name {
  font-weight: 600;
  color: #3d2914;
  font-size: 0.95rem;
}

.recipe-meta {
  font-size: 0.8rem;
  color: #8b7355;
}

/* 标签单元格 */
.tag-cell {
  white-space: nowrap;
}

.tag-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
}

.tag-badge.cuisine {
  background: rgba(194, 98, 46, 0.1);
  color: #c2622e;
}

.tag-badge.scene {
  background: rgba(107, 92, 77, 0.1);
  color: #6b5c4d;
}

.tag-badge.easy {
  background: rgba(46, 125, 50, 0.1);
  color: #2e7d32;
}

.tag-badge.medium {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.tag-badge.hard {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

/* 时长单元格 */
.time-cell {
  color: #8b7355;
  font-size: 0.9rem;
  white-space: nowrap;
}

/* 统计单元格 */
.stats-cell {
  display: flex;
  gap: 1rem;
  white-space: nowrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  color: #6b5c4d;
}

.stat-item svg {
  width: 16px;
  height: 16px;
}

/* 操作单元格 */
.action-cell {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
}

.icon-btn svg {
  width: 18px;
  height: 18px;
}

.icon-btn.edit-btn:hover {
  background: rgba(194, 98, 46, 0.1);
  color: #c2622e;
}

.icon-btn.delete-btn:hover {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

/* 操作按钮 */
.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn.import-btn {
  background: white;
  border: 1.5px solid #e5ddd3;
  color: #6b5c4d;
}

.action-btn.import-btn:hover {
  border-color: #c2622e;
  color: #c2622e;
}

.action-btn.create-btn {
  background: linear-gradient(135deg, #c2622e 0%, #d4773a 100%);
  color: white;
}

.action-btn.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(194, 98, 46, 0.3);
}

/* 分页 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1rem;
  border: 1.5px solid #e5ddd3;
  border-radius: 10px;
  background: white;
  color: #6b5c4d;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  border-color: #c2622e;
  color: #c2622e;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination-btn svg {
  width: 16px;
  height: 16px;
}

.pagination-info {
  font-size: 0.9rem;
  color: #6b5c4d;
  font-weight: 500;
}

/* 对话框样式 */
.import-dialog-content {
  padding: 0.5rem 0;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #a89078;
  margin-bottom: 1rem;
}

/* 食材编辑器 */
.ingredients-editor {
  width: 100%;
}

.ingredient-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  align-items: center;
}

.ingredient-select {
  width: 180px;
}

.ingredient-amount-input {
  flex: 1;
}

.ingredient-order-input {
  width: 100px;
}

.ingredient-name-display {
  color: #3d2914;
  font-size: 0.9rem;
  font-weight: 500;
  min-width: 80px;
  white-space: nowrap;
  background: #f5f0e8;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.unit-text {
  margin-left: 0.5rem;
  color: #8b7355;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .recipe-management-page {
    padding-top: 72px;
  }

  .content-wrapper {
    padding: 1rem;
  }

  .page-header {
    padding: 1.5rem 1rem 1rem;
  }

  .page-title {
    font-size: 1.4rem;
  }

  .page-title svg {
    width: 28px;
    height: 28px;
  }

  .toolbar {
    flex-direction: column;
  }

  .search-box {
    min-width: 100%;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    flex: 1;
    min-width: calc(50% - 0.375rem);
  }

  .recipe-table th,
  .recipe-table td {
    padding: 0.85rem 1rem;
  }

  .recipe-info-cell {
    gap: 0.75rem;
    min-width: 250px;
  }

  .recipe-image,
  .recipe-image-placeholder {
    width: 48px;
    height: 48px;
  }

  .action-btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
