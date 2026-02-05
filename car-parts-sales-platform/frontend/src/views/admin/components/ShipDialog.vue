<template>
  <el-dialog
    v-model="visible"
    title="订单发货"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <!-- 订单信息展示 -->
      <div class="order-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ order?.order_no }}</el-descriptions-item>
          <el-descriptions-item label="用户">{{ order?.user_nickname || order?.user_phone }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 发货表单 -->
      <el-form-item label="物流公司" prop="express_company" style="margin-top: 20px">
        <el-select
          v-model="form.express_company"
          placeholder="请选择物流公司"
          filterable
          allow-create
          style="width: 100%"
        >
          <el-option
            v-for="company in expressCompanies"
            :key="company"
            :label="company"
            :value="company"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="物流单号" prop="tracking_number">
        <el-input
          v-model="form.tracking_number"
          placeholder="请输入物流单号"
          clearable
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        确认发货
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { shipOrderApi } from '@/api/modules/order'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  order: {
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

// 常用物流公司
const expressCompanies = [
  '顺丰速运',
  '京东物流',
  '圆通速递',
  '中通快递',
  '申通快递',
  '韵达速递',
  '邮政EMS',
  '德邦快递',
  '极兔速递',
  '百世快递'
]

// 表单数据
const form = ref({
  express_company: '',
  tracking_number: ''
})

// 表单验证规则
const rules = {
  express_company: [
    { required: true, message: '请选择物流公司', trigger: 'change' }
  ],
  tracking_number: [
    { required: true, message: '请输入物流单号', trigger: 'blur' },
    { min: 5, message: '物流单号长度不能少于5位', trigger: 'blur' }
  ]
}

// 提交发货
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  if (!props.order?.id) {
    ElMessage.error('订单信息异常')
    return
  }

  submitting.value = true
  try {
    await shipOrderApi(props.order.id, {
      express_company: form.value.express_company,
      tracking_number: form.value.tracking_number
    })
    ElMessage.success('发货成功')
    emit('success')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '发货失败')
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    express_company: '',
    tracking_number: ''
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
.order-info {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 80px;
}

:deep(.el-descriptions__body) {
  background: #fafafa;
}
</style>
