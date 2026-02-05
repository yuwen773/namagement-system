<template>
  <el-dialog
    v-model="dialogVisible"
    title="商品分类管理"
    width="700px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="category-manage">
      <!-- 工具栏 -->
      <div class="toolbar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索分类"
          clearable
          style="width: 200px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新增分类</el-button>
        <el-button :icon="Refresh" @click="fetchCategoryTree">刷新</el-button>
      </div>

      <!-- 分类树 -->
      <el-tree
        ref="treeRef"
        v-loading="loading"
        :data="categoryTree"
        :props="treeProps"
        :filter-node-method="filterNode"
        :expand-on-click-node="false"
        node-key="id"
        default-expand-all
        class="category-tree"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <span class="node-label">
              <el-icon v-if="data.children && data.children.length > 0"><Folder /></el-icon>
              <el-icon v-else><Document /></el-icon>
              {{ node.label }}
            </span>
            <span class="node-actions">
              <el-tag v-if="!data.is_active" type="info" size="small">已禁用</el-tag>
              <el-tag v-else-if="data.product_count > 0" type="success" size="small">{{ data.product_count }}件</el-tag>
              <el-button link type="primary" size="small" :icon="Plus" @click="handleAddChild(data)">添加子类</el-button>
              <el-button link type="primary" size="small" :icon="Edit" @click="handleEdit(data)">编辑</el-button>
              <el-button link type="danger" size="small" :icon="Delete" @click="handleDelete(data)">删除</el-button>
            </span>
          </div>
        </template>
      </el-tree>
    </div>

    <!-- 分类编辑表单对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="editForm.id ? '编辑分类' : '新增分类'"
      width="500px"
      append-to-body
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="editForm.name" placeholder="请输入分类名称" maxlength="50" show-word-limit />
        </el-form-item>

        <el-form-item label="上级分类">
          <el-tree-select
            v-model="editForm.parent"
            :data="categoryTreeForSelect"
            :props="{ value: 'id', label: 'name', children: 'children' }"
            placeholder="请选择上级分类（不选则为顶级分类）"
            clearable
            check-strictly
            :render-after-expand="false"
          />
        </el-form-item>

        <el-form-item label="排序权重">
          <el-input-number v-model="editForm.sort_order" :min="0" controls-position="right" style="width: 150px" />
          <span class="unit-hint">数值越小越靠前</span>
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="editForm.is_active">
            <el-radio :value="true">启用</el-radio>
            <el-radio :value="false">禁用</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="图标">
          <el-input v-model="editForm.icon" placeholder="图标类名（可选）" clearable />
        </el-form-item>

        <el-form-item label="描述">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分类描述"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Edit, Delete, Search, Refresh, Folder, Document
} from '@element-plus/icons-vue'
import {
  getCategoryTreeApi,
  createCategoryApi,
  updateCategoryApi,
  deleteCategoryApi
} from '@/api/modules/product'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const treeRef = ref(null)
const loading = ref(false)
const searchKeyword = ref('')
const categoryTree = ref([])

// 树形配置
const treeProps = {
  children: 'children',
  label: 'name'
}

// 编辑对话框
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const submitLoading = ref(false)

// 编辑表单
const editForm = reactive({
  id: null,
  name: '',
  parent: null,
  sort_order: 0,
  is_active: true,
  icon: '',
  description: ''
})

// 表单验证规则
const editRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

// 用于选择的分类树（排除当前编辑的节点）
const categoryTreeForSelect = computed(() => {
  const excludeId = editForm.id
  const excludeNode = (nodes) => {
    return nodes
      .filter(node => node.id !== excludeId)
      .map(node => ({
        ...node,
        children: node.children ? excludeNode(node.children) : undefined
      }))
  }
  return excludeNode(JSON.parse(JSON.stringify(categoryTree.value)))
})

// 获取分类树
const fetchCategoryTree = async () => {
  loading.value = true
  try {
    const data = await getCategoryTreeApi()
    categoryTree.value = data || []
  } catch (error) {
    ElMessage.error('获取分类树失败')
  } finally {
    loading.value = false
  }
}

// 过滤节点
const filterNode = (value, data) => {
  if (!value) return true
  return data.name.includes(value)
}

// 监听搜索关键词
watch(searchKeyword, (val) => {
  treeRef.value?.filter(val)
})

// 新增分类
const handleAdd = () => {
  Object.assign(editForm, {
    id: null,
    name: '',
    parent: null,
    sort_order: 0,
    is_active: true,
    icon: '',
    description: ''
  })
  editDialogVisible.value = true
}

// 添加子分类
const handleAddChild = (data) => {
  Object.assign(editForm, {
    id: null,
    name: '',
    parent: data.id,
    sort_order: 0,
    is_active: true,
    icon: '',
    description: ''
  })
  editDialogVisible.value = true
}

// 编辑分类
const handleEdit = (data) => {
  Object.assign(editForm, {
    id: data.id,
    name: data.name,
    parent: data.parent || null,
    sort_order: data.sort_order || 0,
    is_active: data.is_active !== false,
    icon: data.icon || '',
    description: data.description || ''
  })
  editDialogVisible.value = true
}

// 删除分类
const handleDelete = async (data) => {
  // 检查是否有子分类
  if (data.children && data.children.length > 0) {
    ElMessage.warning('该分类下有子分类，无法删除')
    return
  }

  // 检查是否有商品
  if (data.product_count > 0) {
    ElMessage.warning('该分类下有商品，无法删除')
    return
  }

  try {
    await ElMessageBox.confirm(`确定要删除分类"${data.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteCategoryApi(data.id)
    ElMessage.success('删除成功')
    fetchCategoryTree()
    emit('success')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await editFormRef.value.validate()
  } catch {
    return
  }

  submitLoading.value = true
  try {
    const data = {
      name: editForm.name,
      parent: editForm.parent,
      sort_order: editForm.sort_order,
      is_active: editForm.is_active,
      icon: editForm.icon,
      description: editForm.description
    }

    if (editForm.id) {
      await updateCategoryApi(editForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createCategoryApi(data)
      ElMessage.success('创建成功')
    }

    editDialogVisible.value = false
    fetchCategoryTree()
    emit('success')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
}

// 监听对话框打开
watch(() => props.modelValue, (val) => {
  if (val) {
    fetchCategoryTree()
  }
})
</script>

<style scoped>
.category-manage {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-tree {
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 10px;
  min-height: 300px;
  max-height: 400px;
  overflow-y: auto;
}

.tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 8px;
}

.node-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.node-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.unit-hint {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}

/* 滚动条样式 */
.category-tree::-webkit-scrollbar {
  width: 6px;
}

.category-tree::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.category-tree::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}

/* Element Plus 树形样式调整 */
:deep(.el-tree-node__content) {
  height: 36px;
}

:deep(.el-tree-node__content:hover) {
  background: #f5f7fa;
}

:deep(.el-tree-node:focus > .el-tree-node__content) {
  background: #ecf5ff;
}
</style>
