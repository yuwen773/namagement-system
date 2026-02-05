<template>
  <div class="image-uploader">
    <el-upload
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
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Upload, UploadFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

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
    fileList.value = props.modelValue.map((url, index) => ({
      uid: index,
      name: `image-${index}`,
      status: 'success',
      url: url
    }))
  } else if (props.modelValue) {
    fileList.value = [{
      uid: 0,
      name: 'image',
      status: 'success',
      url: props.modelValue
    }]
  }
}

// 监听 modelValue 变化
watch(() => props.modelValue, () => {
  initFileList()
}, { immediate: true })

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
    emit('update:modelValue', imageUrl)
  } else {
    const urls = list
      .filter(item => item.status === 'success')
      .map(item => item.response?.image_url || item.response?.url || item.url)
    emit('update:modelValue', urls)
  }

  ElMessage.success('上传成功')
}

// 上传失败
const handleError = () => {
  ElMessage.error('上传失败')
  // 移除失败的文件
  fileList.value = fileList.value.filter(item => item.status === 'success')
}

// 移除文件
const handleRemove = (file, list) => {
  if (props.limit === 1) {
    emit('update:modelValue', '')
  } else {
    const urls = list
      .filter(item => item.status === 'success')
      .map(item => item.response?.image_url || item.response?.url || item.url)
    emit('update:modelValue', urls)
  }
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
