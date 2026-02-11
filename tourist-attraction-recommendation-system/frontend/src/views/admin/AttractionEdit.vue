<template>
  <div class="bg-white rounded-xl shadow-md p-6">
    <h2 class="text-xl font-bold mb-6">{{ isEdit ? '编辑景点' : '新增景点' }}</h2>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="景点名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="类别" prop="category">
        <el-select v-model="form.category" placeholder="选择类别">
          <el-option label="自然风光" value="NATURE" />
          <el-option label="人文古迹" value="HISTORY" />
          <el-option label="主题乐园" value="THEME" />
          <el-option label="其他" value="OTHER" />
        </el-select>
      </el-form-item>
      <el-form-item label="地区" prop="region">
        <el-input v-model="form.region" />
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="form.address" />
      </el-form-item>
      <el-form-item label="开放时间" prop="openingHours">
        <el-input v-model="form.openingHours" placeholder="如: 9:00-18:00" />
      </el-form-item>
      <el-form-item label="价格" prop="price">
        <el-input-number v-model="form.price" :min="0" />
      </el-form-item>
      <el-form-item label="封面图片" prop="coverImage">
        <el-upload action="/api/attractions/upload/" :show-file-list="false" :on-success="handleCoverSuccess">
          <el-image v-if="form.coverImage" :src="form.coverImage" fit="cover" class="w-32 h-32" />
          <el-icon v-else class="text-4xl"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="景点介绍" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="5" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveAttraction" :loading="loading">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '@/api/request'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const route = useRoute()
const formRef = ref(null)
const loading = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  category: '',
  region: '',
  address: '',
  openingHours: '',
  price: 0,
  coverImage: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入景点名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
}

async function fetchAttraction() {
  if (!isEdit.value) return
  try {
    const res = await request.get(`/attractions/${route.params.id}/`)
    Object.assign(form, res.data)
  } catch (error) {
    console.error(error)
  }
}

function handleCoverSuccess(res) {
  form.coverImage = res.data?.url || res.data
}

async function saveAttraction() {
  await formRef.value.validate()
  loading.value = true
  try {
    if (isEdit.value) {
      await request.put(`/attractions/${route.params.id}/`, form)
    } else {
      await request.post('/attractions/', form)
    }
    ElMessage.success('保存成功')
    $router.push('/admin/attractions')
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchAttraction)
</script>
