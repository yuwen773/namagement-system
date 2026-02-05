<template>
  <el-dialog
    v-model="visible"
    :title="isEdit ? '编辑优惠券' : '新增优惠券'"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      label-position="left"
    >
      <el-form-item label="优惠券名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入优惠券名称，如：新用户专享券"
          maxlength="50"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="优惠券描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入优惠券描述"
          maxlength="200"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="优惠类型" prop="discount_type">
        <el-radio-group v-model="formData.discount_type" @change="handleDiscountTypeChange">
          <el-radio value="full_reduction">满减券</el-radio>
          <el-radio value="discount">折扣券</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="使用门槛" prop="min_amount">
        <el-input-number
          v-model="formData.min_amount"
          :min="0"
          :precision="2"
          :step="10"
          controls-position="right"
          style="width: 200px"
        />
        <span class="unit-text">元（0表示无门槛）</span>
      </el-form-item>

      <el-form-item
        v-if="formData.discount_type === 'full_reduction'"
        label="满减金额"
        prop="discount_amount"
      >
        <el-input-number
          v-model="formData.discount_amount"
          :min="0.01"
          :precision="2"
          :step="5"
          controls-position="right"
          style="width: 200px"
        />
        <span class="unit-text">元</span>
      </el-form-item>

      <el-form-item
        v-if="formData.discount_type === 'discount'"
        label="折扣率"
        prop="discount_rate"
      >
        <el-input-number
          v-model="formData.discount_rate"
          :min="0.1"
          :max="9.9"
          :precision="1"
          :step="0.1"
          controls-position="right"
          style="width: 200px"
        />
        <span class="unit-text">折（如8.5表示8.5折）</span>
      </el-form-item>

      <el-form-item label="有效期" required>
        <div class="date-range-wrapper">
          <el-form-item prop="valid_from" style="margin-bottom: 0;">
            <el-date-picker
              v-model="formData.valid_from"
              type="datetime"
              placeholder="开始时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ssZ"
              :disabled-date="disableStartDate"
              style="width: 100%"
            />
          </el-form-item>
          <span class="date-separator">至</span>
          <el-form-item prop="valid_until" style="margin-bottom: 0;">
            <el-date-picker
              v-model="formData.valid_until"
              type="datetime"
              placeholder="结束时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ssZ"
              :disabled-date="disableEndDate"
              style="width: 100%"
            />
          </el-form-item>
        </div>
      </el-form-item>

      <el-form-item label="发放总量" prop="total_quantity">
        <el-input-number
          v-model="formData.total_quantity"
          :min="0"
          :step="100"
          controls-position="right"
          style="width: 200px"
        />
        <span class="unit-text">张（0表示不限量）</span>
      </el-form-item>

      <el-form-item label="每人限领" prop="per_user_limit">
        <el-input-number
          v-model="formData.per_user_limit"
          :min="1"
          :max="99"
          controls-position="right"
          style="width: 200px"
        />
        <span class="unit-text">张</span>
      </el-form-item>

      <el-form-item label="状态" prop="is_active">
        <el-switch
          v-model="formData.is_active"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>

      <!-- 预览区域 -->
      <el-divider content-position="left">优惠预览</el-divider>
      <div class="coupon-preview">
        <div class="preview-card">
          <div class="preview-header">
            <span class="preview-name">{{ formData.name || '优惠券名称' }}</span>
            <el-tag :type="formData.is_active ? 'success' : 'info'" size="small">
              {{ formData.is_active ? '启用' : '禁用' }}
            </el-tag>
          </div>
          <div class="preview-body">
            <div class="preview-discount">
              <span v-if="formData.discount_type === 'full_reduction'" class="discount-amount">
                ¥{{ formData.discount_amount || 0 }}
              </span>
              <span v-else class="discount-rate">
                {{ formData.discount_rate || 8.5 }}折
              </span>
              <span v-if="formData.min_amount > 0" class="discount-condition">
                满¥{{ formData.min_amount }}可用
              </span>
              <span v-else class="discount-condition">
                无门槛
              </span>
            </div>
            <div class="preview-info">
              <div class="info-row">
                <span>有效期：</span>
                <span>{{ formatDateRange }}</span>
              </div>
              <div class="info-row">
                <span>限量：</span>
                <span>{{ formData.total_quantity === 0 ? '不限量' : formData.total_quantity + '张' }}</span>
              </div>
              <div class="info-row">
                <span>限领：</span>
                <span>每人{{ formData.per_user_limit }}张</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  createCouponApi,
  updateCouponApi,
  getCouponDetailApi
} from '@/api/modules/marketing'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  couponId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isEdit = computed(() => !!props.couponId)

const formRef = ref(null)
const submitting = ref(false)

// 表单数据
const formData = reactive({
  name: '',
  description: '',
  discount_type: 'full_reduction',
  min_amount: 0,
  discount_amount: null,
  discount_rate: null,
  valid_from: '',
  valid_until: '',
  total_quantity: 1000,
  per_user_limit: 1,
  is_active: true
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入优惠券名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  discount_type: [
    { required: true, message: '请选择优惠类型', trigger: 'change' }
  ],
  min_amount: [
    { required: true, message: '请输入使用门槛', trigger: 'blur' }
  ],
  discount_amount: [
    {
      validator: (rule, value, callback) => {
        if (formData.discount_type === 'full_reduction') {
          if (!value || value <= 0) {
            callback(new Error('请输入满减金额'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  discount_rate: [
    {
      validator: (rule, value, callback) => {
        if (formData.discount_type === 'discount') {
          if (!value || value < 0.1 || value > 9.9) {
            callback(new Error('折扣率必须在0.1-9.9之间'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  valid_from: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  valid_until: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  total_quantity: [
    { required: true, message: '请输入发放总量', trigger: 'blur' }
  ],
  per_user_limit: [
    { required: true, message: '请输入每人限领数量', trigger: 'blur' }
  ]
}

// 格式化日期范围显示
const formatDateRange = computed(() => {
  if (!formData.valid_from || !formData.valid_until) return '未设置'
  const start = new Date(formData.valid_from).toLocaleDateString('zh-CN')
  const end = new Date(formData.valid_until).toLocaleDateString('zh-CN')
  return `${start} - ${end}`
})

// 禁用开始日期（今天之前的日期）
const disableStartDate = (date) => {
  return date < new Date(new Date().setHours(0, 0, 0, 0))
}

// 禁用结束日期（开始日期之前的日期）
const disableEndDate = (date) => {
  if (formData.valid_from) {
    return date < new Date(formData.valid_from)
  }
  return date < new Date(new Date().setHours(0, 0, 0, 0))
}

// 优惠类型变化处理
const handleDiscountTypeChange = (type) => {
  if (type === 'full_reduction') {
    formData.discount_rate = null
  } else {
    formData.discount_amount = null
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    name: '',
    description: '',
    discount_type: 'full_reduction',
    min_amount: 0,
    discount_amount: null,
    discount_rate: null,
    valid_from: '',
    valid_until: '',
    total_quantity: 1000,
    per_user_limit: 1,
    is_active: true
  })
  formRef.value?.clearValidate()
}

// 加载优惠券详情
const loadCouponDetail = async () => {
  if (!props.couponId) return

  try {
    const data = await getCouponDetailApi(props.couponId)
    Object.assign(formData, {
      name: data.name || '',
      description: data.description || '',
      discount_type: data.discount_type || 'full_reduction',
      min_amount: parseFloat(data.min_amount) || 0,
      discount_amount: data.discount_amount ? parseFloat(data.discount_amount) : null,
      discount_rate: data.discount_rate ? parseFloat(data.discount_rate) : null,
      valid_from: data.valid_from || '',
      valid_until: data.valid_until || '',
      total_quantity: data.total_quantity || 1000,
      per_user_limit: data.per_user_limit || 1,
      is_active: data.is_active ?? true
    })
  } catch (error) {
    ElMessage.error('加载优惠券详情失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    const submitData = {
      name: formData.name,
      description: formData.description,
      discount_type: formData.discount_type,
      min_amount: formData.min_amount.toFixed(2),
      total_quantity: formData.total_quantity,
      per_user_limit: formData.per_user_limit,
      is_active: formData.is_active,
      valid_from: formData.valid_from,
      valid_until: formData.valid_until
    }

    if (formData.discount_type === 'full_reduction') {
      submitData.discount_amount = formData.discount_amount.toFixed(2)
    } else {
      submitData.discount_rate = formData.discount_rate.toFixed(1)
    }

    if (isEdit.value) {
      await updateCouponApi(props.couponId, submitData)
      ElMessage.success('优惠券更新成功')
    } else {
      await createCouponApi(submitData)
      ElMessage.success('优惠券创建成功')
    }

    emit('success')
    handleClose()
  } catch (error) {
    if (error !== false) { // 表单验证失败时 error 为 false
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  } finally {
    submitting.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  resetForm()
  emit('update:modelValue', false)
}

// 监听对话框打开
watch(() => props.modelValue, (val) => {
  if (val && isEdit.value) {
    loadCouponDetail()
  }
})
</script>

<style scoped>
.unit-text {
  margin-left: 8px;
  color: #94a3b8;
  font-size: 13px;
}

.date-range-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.date-range-wrapper .el-form-item {
  flex: 1;
}

.date-separator {
  color: #94a3b8;
}

.coupon-preview {
  padding: 0 20px;
}

.preview-card {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
}

.preview-name {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.preview-body {
  padding: 20px;
  background: #fff;
}

.preview-discount {
  text-align: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #e5e7eb;
}

.discount-amount {
  font-size: 36px;
  font-weight: 700;
  color: #f97316;
}

.discount-rate {
  font-size: 36px;
  font-weight: 700;
  color: #f97316;
}

.discount-condition {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: #64748b;
}

.preview-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.info-row span:first-child {
  color: #64748b;
}

.info-row span:last-child {
  color: #1e293b;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
