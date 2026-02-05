<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑商品' : '新增商品'"
    width="80%"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      class="product-form"
    >
      <el-tabs v-model="activeTab" class="form-tabs">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-row :gutter="20">
            <el-col :span="16">
              <el-form-item label="商品名称" prop="name">
                <el-input v-model="formData.name" placeholder="请输入商品名称" maxlength="200" show-word-limit />
              </el-form-item>

              <el-form-item label="商品分类" prop="category">
                <el-cascader
                  v-model="formData.category"
                  :options="categoryTree"
                  :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true, emitPath: false }"
                  placeholder="请选择分类"
                  style="width: 100%"
                />
              </el-form-item>

              <el-form-item label="商品价格" prop="price">
                <el-input-number v-model="formData.price" :min="0" :precision="2" :step="0.01" controls-position="right" style="width: 200px" />
                <span class="unit">元</span>
              </el-form-item>

              <el-form-item label="商品库存" prop="stock">
                <el-input-number v-model="formData.stock" :min="0" :step="1" controls-position="right" style="width: 200px" />
                <span class="unit">件</span>
              </el-form-item>

              <el-form-item label="商品描述" prop="description">
                <el-input
                  v-model="formData.description"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入商品描述"
                  maxlength="2000"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="详细内容">
                <el-input
                  v-model="formData.content"
                  type="textarea"
                  :rows="8"
                  placeholder="请输入商品详细内容（支持富文本）"
                />
              </el-form-item>
            </el-col>

            <el-col :span="8">
              <el-form-item label="商品主图" prop="image">
                <ImageUploader v-model="formData.image" :limit="1" />
              </el-form-item>

              <el-form-item label="商品状态">
                <el-radio-group v-model="formData.status">
                  <el-radio value="draft">草稿</el-radio>
                  <el-radio value="published">发布</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="是否推荐">
                <el-switch v-model="formData.is_featured" />
              </el-form-item>

              <el-form-item label="排序权重">
                <el-input-number v-model="formData.sort_order" :min="-9999" :max="9999" controls-position="right" style="width: 150px" />
                <span class="unit-hint">数值越大越靠前</span>
              </el-form-item>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 商品图片 -->
        <el-tab-pane label="商品图片" name="images">
          <ImageUploader
            v-model="formData.images"
            :limit="10"
            list-type="picture-card"
            @update:model-value="handleImagesChange"
          />
          <div class="image-tip">
            <el-icon><InfoFilled /></el-icon>
            <span>最多上传10张图片，第一张为主图，拖拽可调整顺序</span>
          </div>
        </el-tab-pane>

        <!-- 商品属性 -->
        <el-tab-pane label="商品属性" name="attributes">
          <div class="attributes-header">
            <el-button type="primary" size="small" :icon="Plus" @click="addAttribute">添加属性</el-button>
          </div>
          <el-table :data="formData.attributes" border style="width: 100%; margin-top: 10px">
            <el-table-column label="属性名称" width="200">
              <template #default="{ row }">
                <el-input v-model="row.attr_name" placeholder="如：适配车型" />
              </template>
            </el-table-column>
            <el-table-column label="属性值">
              <template #default="{ row }">
                <el-input v-model="row.attr_value" placeholder="如：宝马3系/奥迪A4" />
              </template>
            </el-table-column>
            <el-table-column label="排序" width="100">
              <template #default="{ row }">
                <el-input-number v-model="row.sort_order" :min="0" size="small" controls-position="right" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{ $index }">
                <el-button link type="danger" size="small" :icon="Delete" @click="removeAttribute($index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- SEO设置 -->
        <el-tab-pane label="SEO设置" name="seo">
          <el-form-item label="SEO标题">
            <el-input v-model="formData.seo_title" placeholder="请输入SEO标题" maxlength="100" show-word-limit />
          </el-form-item>
          <el-form-item label="SEO关键词">
            <el-input v-model="formData.seo_keywords" placeholder="多个关键词用逗号分隔" maxlength="200" show-word-limit />
          </el-form-item>
          <el-form-item label="SEO描述">
            <el-input
              v-model="formData.seo_description"
              type="textarea"
              :rows="3"
              placeholder="请输入SEO描述"
              maxlength="300"
              show-word-limit
            />
          </el-form-item>
        </el-tab-pane>
      </el-tabs>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="handleSubmit">保存</el-button>
      <el-button v-if="!isEdit" type="success" :loading="publishLoading" @click="handlePublish">保存并发布</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete, InfoFilled } from '@element-plus/icons-vue'
import {
  getProductDetailApi,
  createProductApi,
  updateProductApi,
  getCategoryTreeApi,
  getProductImagesApi,
  createProductImageApi,
  deleteProductImageApi,
  getProductAttributesApi
} from '@/api/modules/product'
import ImageUploader from './ImageUploader.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  productId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isEdit = computed(() => !!props.productId)

const activeTab = ref('basic')
const formRef = ref(null)
const submitLoading = ref(false)
const publishLoading = ref(false)
const categoryTree = ref([])

// 表单数据
const formData = reactive({
  name: '',
  category: null,
  price: 0,
  stock: 0,
  description: '',
  content: '',
  image: '',
  images: [],
  status: 'draft',
  is_featured: false,
  sort_order: 0,
  seo_title: '',
  seo_keywords: '',
  seo_description: '',
  attributes: []
})

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择商品分类', trigger: 'change' }],
  price: [{ required: true, message: '请输入商品价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入商品库存', trigger: 'blur' }]
}

// 获取分类树
const fetchCategoryTree = async () => {
  try {
    const data = await getCategoryTreeApi()
    categoryTree.value = data || []
  } catch (error) {
    console.error('获取分类树失败:', error)
  }
}

// 获取商品详情
const fetchProductDetail = async () => {
  if (!props.productId) return

  try {
    const data = await getProductDetailApi(props.productId)

    // 填充表单数据
    Object.assign(formData, {
      name: data.name || '',
      category: data.category || null,
      price: data.price || 0,
      stock: data.stock || 0,
      description: data.description || '',
      content: data.content || '',
      image: data.image || '',
      images: data.images?.map(img => img.image_url) || [],
      status: data.status || 'draft',
      is_featured: data.is_featured || false,
      sort_order: data.sort_order || 0,
      seo_title: data.seo_title || '',
      seo_keywords: data.seo_keywords || '',
      seo_description: data.seo_description || '',
      attributes: data.attributes?.map(attr => ({
        id: attr.id,
        attr_name: attr.attr_name,
        attr_value: attr.attr_value,
        sort_order: attr.sort_order
      })) || []
    })
  } catch (error) {
    ElMessage.error('获取商品详情失败')
  }
}

// 添加属性
const addAttribute = () => {
  formData.attributes.push({
    attr_name: '',
    attr_value: '',
    sort_order: formData.attributes.length
  })
}

// 删除属性
const removeAttribute = (index) => {
  formData.attributes.splice(index, 1)
}

// 图片变化处理
const handleImagesChange = (images) => {
  formData.images = images
  if (images.length > 0 && !formData.image) {
    formData.image = images[0]
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    name: '',
    category: null,
    price: 0,
    stock: 0,
    description: '',
    content: '',
    image: '',
    images: [],
    status: 'draft',
    is_featured: false,
    sort_order: 0,
    seo_title: '',
    seo_keywords: '',
    seo_description: '',
    attributes: []
  })
  formRef.value?.clearValidate()
  activeTab.value = 'basic'
}

// 关闭对话框
const handleClose = () => {
  resetForm()
  dialogVisible.value = false
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitLoading.value = true
  try {
    const data = {
      name: formData.name,
      category: formData.category,
      price: formData.price,
      stock: formData.stock,
      description: formData.description,
      content: formData.content,
      image: formData.image,
      status: formData.status,
      is_featured: formData.is_featured,
      sort_order: formData.sort_order,
      seo_title: formData.seo_title,
      seo_keywords: formData.seo_keywords,
      seo_description: formData.seo_description
    }

    let result
    if (isEdit.value) {
      result = await updateProductApi(props.productId, data)
    } else {
      result = await createProductApi(data)
    }

    // 处理属性
    const productId = result.id || props.productId
    if (formData.attributes.length > 0) {
      // TODO: 调用属性更新 API
    }

    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    emit('success')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

// 保存并发布
const handlePublish = async () => {
  formData.status = 'published'
  await handleSubmit()
}

// 监听对话框打开
watch(() => props.modelValue, (val) => {
  if (val) {
    fetchCategoryTree()
    if (isEdit.value) {
      fetchProductDetail()
    }
  }
})
</script>

<style scoped>
.product-form {
  max-height: 60vh;
  overflow-y: auto;
}

.form-tabs {
  padding: 0 10px;
}

.unit {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}

.unit-hint {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}

.attributes-header {
  margin-bottom: 10px;
}

.image-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  padding: 10px;
  background: #f0f9ff;
  border: 1px solid #b3d8ff;
  border-radius: 4px;
  color: #409eff;
  font-size: 13px;
}

/* 滚动条样式 */
.product-form::-webkit-scrollbar {
  width: 6px;
}

.product-form::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 3px;
}

.product-form::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
