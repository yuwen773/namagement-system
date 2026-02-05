<template>
  <el-dialog
    v-model="visible"
    title="审核退换货申请"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-if="returnData" class="return-info">
      <!-- 申请信息展示 -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ returnData.order_no }}</el-descriptions-item>
        <el-descriptions-item label="用户">{{ returnData.user_phone }}</el-descriptions-item>
        <el-descriptions-item label="申请类型">
          <el-tag :type="returnData.request_type === 'return' ? 'danger' : 'warning'" size="small">
            {{ returnData.request_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">
          {{ formatDate(returnData.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="申请原因" :span="2">
          {{ returnData.reason }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      style="margin-top: 20px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="审核结果" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="approved">
            <span style="color: #67c23a">同意</span>
          </el-radio>
          <el-radio label="rejected">
            <span style="color: #f56c6c">拒绝</span>
          </el-radio>
          <el-radio label="completed">
            <span style="color: #409eff">直接完成</span>
          </el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="处理意见" prop="admin_note">
        <el-input
          v-model="form.admin_note"
          type="textarea"
          :rows="4"
          placeholder="请输入处理意见（如退货地址、换货说明等）"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        确认提交
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { processReturnApi } from '@/api/modules/order'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  returnData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const formRef = ref(null)
const submitting = ref(false)

// 表单数据
const form = ref({
  status: 'approved',
  admin_note: ''
})

// 表单验证规则
const rules = {
  status: [
    { required: true, message: '请选择审核结果', trigger: 'change' }
  ],
  admin_note: [
    { required: true, message: '请输入处理意见', trigger: 'blur' },
    { min: 5, message: '处理意见至少5个字符', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateStr) => {
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

// 提交审核
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  if (!props.returnData?.id) {
    ElMessage.error('退换货申请信息异常')
    return
  }

  submitting.value = true
  try {
    await processReturnApi(props.returnData.id, {
      status: form.value.status,
      admin_note: form.value.admin_note
    })
    ElMessage.success('审核成功')
    emit('success')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '审核失败')
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    status: 'approved',
    admin_note: ''
  }
  nextTick(() => {
    formRef.value?.clearValidate()
  })
}

// 关闭对话框
const handleClose = () => {
  resetForm()
  visible.value = false
}

// 监听对话框打开
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    resetForm()
  }
})
</script>

<style scoped>
.return-info {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 80px;
}

:deep(.el-descriptions__body) {
  background: #fafafa;
}
</style>
