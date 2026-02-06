<template>
  <div class="image-uploader">
    <!-- 可拖拽的图片列表 (仅在 picture-card 模式且允许多选时启用) -->
    <div v-if="listType === 'picture-card' && limit > 1" class="draggable-uploader">
      <draggable
        v-model="fileList"
        item-key="uid"
        class="el-upload-list el-upload-list--picture-card"
        @end="handleDragEnd"
      >
        <template #item="{ element }">
          <div class="el-upload-list__item">
            <img class="el-upload-list__item-thumbnail" :src="element.url" alt="" />
            <span class="el-upload-list__item-actions">
              <span class="el-upload-list__item-preview" @click="handlePreview(element)">
                <el-icon><ZoomIn /></el-icon>
              </span>
              <span class="el-upload-list__item-delete" @click="handleRemoveFile(element)">
                <el-icon><Delete /></el-icon>
              </span>
            </span>
          </div>
        </template>
        
        <template #footer>
          <el-upload
            v-if="fileList.length < limit"
            class="uploader-trigger"
            :action="uploadUrl"
            :headers="uploadHeaders"
            :on-success="handleSuccess"
            :on-error="handleError"
            :before-upload="beforeUpload"
            :show-file-list="false"
            :multiple="true"
            accept="image/*"
          >
            <div class="el-upload--picture-card">
              <el-icon class="uploader-icon"><Plus /></el-icon>
            </div>
          </el-upload>
        </template>
      </draggable>
    </div>

    <!-- 普通上传模式 (单选或非 picture-card) -->
    <el-upload
      v-else
      v-model:file-list="fileList"
      :action="uploadUrl"
      :headers="uploadHeaders"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      :on-remove="handleRemove"
      :on-exceed="handleExceed"
      :limit="limit"
      :list-type="listType"
      :drag="listType === 'picture-card'"
      :multiple="limit > 1"
      accept="image/*"
    >
      <!-- picture-card 模式 -->
      <template v-if="listType === 'picture-card'">
        <el-icon class="uploader-icon"><Plus /></el-icon>
      </template>

      <!-- drag 模式 -->
      <template v-else-if="listType === 'picture'">
        <div class="upload-drag">
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <div class="upload-text">
            <em>点击上传</em> 或将图片拖到此处
          </div>
          <div class="upload-tip">支持 jpg、png 格式，大小不超过 2MB</div>
        </div>
      </template>

      <!-- 默认按钮模式 -->
      <template v-else>
        <el-button type="primary">
          <el-icon><Upload /></el-icon>
          选择图片
        </el-button>
      </template>
    </el-upload>

    <!-- 图片预览弹窗 -->
    <el-dialog v-model="previewVisible" title="图片预览" width="800px" append-to-body>
      <img :src="previewImage" alt="Preview Image" style="width: 100%; height: auto;" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Upload, UploadFilled, ZoomIn, Delete } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import draggable from 'vuedraggable'

const props = defineProps({
  modelValue: {
    type: [String, Array],
    default: () => []
  },
  limit: {
    type: Number,
    default: 1
  },
  listType: {
    type: String,
    default: 'picture-card' // picture-card, picture, text
  },
  maxSize: {
    type: Number,
    default: 2 * 1024 * 1024 // 2MB
  }
})

const emit = defineEmits(['update:modelValue'])

const authStore = useAuthStore()

// 预览状态
const previewVisible = ref(false)
const previewImage = ref('')

// 上传地址
const uploadUrl = computed(() => {
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'}/products/images/`
})

// 上传请求头
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${authStore.token}`
}))

// 文件列表
const fileList = ref([])

// 初始化文件列表
const initFileList = () => {
  if (Array.isArray(props.modelValue)) {
    // 只有当 fileList 为空或者与 modelValue 长度不一致/内容不一致时才重新赋值，防止拖拽过程中被重置
    // 这里简单判断长度，或者完全信任 modelValue 如果它是外部传入的
    // 但为了拖拽体验，通常 fileList 是本地维护的，只在初始化时同步
    
    // 简单的 diff 检查，避免循环更新
    const currentUrls = fileList.value.map(f => f.url)
    const newUrls = props.modelValue
    if (JSON.stringify(currentUrls) !== JSON.stringify(newUrls)) {
        fileList.value = props.modelValue.map((url, index) => ({
          uid: Date.now() + index, // 使用时间戳防止 uid 重复
          name: `image-${index}`,
          status: 'success',
          url: url
        }))
    }
  } else if (props.modelValue) {
    if (fileList.value.length !== 1 || fileList.value[0].url !== props.modelValue) {
        fileList.value = [{
          uid: Date.now(),
          name: 'image',
          status: 'success',
          url: props.modelValue
        }]
    }
  } else {
      if (fileList.value.length > 0) {
          fileList.value = []
      }
  }
}

// 监听 modelValue 变化
watch(() => props.modelValue, () => {
  initFileList()
}, { immediate: true })

// 统一触发 update:modelValue
const emitModelValue = () => {
  if (props.limit === 1) {
    const url = fileList.value.length > 0 ? fileList.value[0].url : ''
    emit('update:modelValue', url)
  } else {
    const urls = fileList.value.map(item => item.url)
    emit('update:modelValue', urls)
  }
}

// 拖拽结束
const handleDragEnd = () => {
  emitModelValue()
}

// 预览图片
const handlePreview = (file) => {
  previewImage.value = file.url
  previewVisible.value = true
}

// 删除文件 (Custom)
const handleRemoveFile = (file) => {
  const index = fileList.value.findIndex(item => item.uid === file.uid)
  if (index !== -1) {
    fileList.value.splice(index, 1)
    emitModelValue()
  }
}

// 上传前校验
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }

  const isLtSize = file.size <= props.maxSize
  if (!isLtSize) {
    ElMessage.error(`图片大小不能超过 ${props.maxSize / 1024 / 1024}MB!`)
    return false
  }

  return true
}

// 上传成功
const handleSuccess = (response, file, list) => {
  // 后端返回的图片URL
  const imageUrl = response.image_url || response.url || file.url
  
  if (props.limit === 1) {
      fileList.value = [{
          uid: file.uid,
          name: file.name,
          status: 'success',
          url: imageUrl
      }]
  } else {
      // 如果是多选模式且使用了自定义 draggable，el-upload 的 list 参数可能只包含新上传的文件
      // 我们需要手动将新文件添加到 fileList
      
      // 检查 fileList 中是否已存在该 uid (el-upload 内部维护的 list 可能会导致重复 if not handled carefully)
      // 但在这里我们使用的是自定义的 fileList for draggable
      // el-upload (hidden) 会触发 handleSuccess
      
      // 注意：如果是 el-upload 默认模式（非 draggable），list 参数是完整的
      // 如果是 draggable 模式，el-upload 是独立的，它的 file-list 不绑定到外层 fileList
      
      if (props.listType === 'picture-card' && props.limit > 1) {
          fileList.value.push({
              uid: file.uid,
              name: file.name,
              status: 'success',
              url: imageUrl
          })
      } else {
          // 普通模式，el-upload 自动管理 list，我们只需要 sync
          // 这里的 list 是 el-upload 传递过来的最新列表
          // 但我们需要确保 url 是正确的（后端返回的）
          // 这种情况下，el-upload 的 list item.url 默认是 blob url，需要替换
          const targetItem = list.find(item => item.uid === file.uid)
          if (targetItem) {
              targetItem.url = imageUrl
          }
          // 对于非 draggable 模式，fileList 绑定在 el-upload 上，会自动更新，但我们需要 emit
          // 此时 fileList.value 应该已经被 el-upload 更新了（v-model:file-list）
      }
  }

  emitModelValue()
  ElMessage.success('上传成功')
}

// 上传失败
const handleError = () => {
  ElMessage.error('上传失败')
  if (props.listType !== 'picture-card' || props.limit <= 1) {
      // 移除失败的文件 (仅在默认模式下需要手动处理，draggable 模式下还没 push 进去)
      fileList.value = fileList.value.filter(item => item.status === 'success')
  }
}

// 移除文件 (Default el-upload)
const handleRemove = (file, list) => {
  // 只有在非 draggable 模式下会触发这个
  // fileList 会自动更新，只需要 emit
  emitModelValue()
}

// 超出限制
const handleExceed = () => {
  ElMessage.warning(`最多只能上传 ${props.limit} 张图片`)
}
</script>

<style scoped>
.image-uploader {
  width: 100%;
}

/* picture-card 模式 */
:deep(.el-upload-list--picture-card) {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 100px;
  height: 100px;
  border-radius: 4px;
}

:deep(.el-upload--picture-card) {
  width: 100px;
  height: 100px;
  border-radius: 4px;
  border: 1px dashed #d9d9d9;
  background: #fafafa;
}

.uploader-icon {
  font-size: 24px;
  color: #8c939d;
}

/* drag 模式 */
:deep(.el-upload-dragger) {
  padding: 40px 20px;
}

.upload-drag {
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 16px;
}

.upload-text {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.upload-text em {
  color: #409eff;
  font-style: normal;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
}

/* 按钮模式 */
.el-button {
  width: 120px;
}
</style>
