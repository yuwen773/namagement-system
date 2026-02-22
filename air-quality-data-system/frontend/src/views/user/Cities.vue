<template>
  <div class="cities-page">
    <div class="page-header">
      <h1 class="page-title">城市列表</h1>
      <p class="page-subtitle">查看所有监测城市的空气质量数据</p>
    </div>

    <div class="content-grid">
      <div v-for="city in cities" :key="city.city_code" class="city-card" @click="goToCity(city.city_code)">
        <div class="city-info">
          <div class="city-name">{{ city.city_name }}</div>
          <div class="city-province">{{ city.province_name }}</div>
        </div>
        <div class="city-aqi">
          <span class="aqi-value" :style="{ color: getAQIColor(city.aqi) }">{{ city.aqi }}</span>
          <span class="aqi-level" :style="{ background: getAQIBgColor(city.aqi) }">
            {{ getAQILevel(city.aqi) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getOverview } from '@/api/airquality'

const router = useRouter()
const cities = ref([])

const fetchCities = async () => {
  try {
    const response = await getOverview()
    cities.value = response.data.map_data || []
  } catch (error) {
    console.error('Failed to fetch cities:', error)
  }
}

const goToCity = (cityCode) => {
  router.push(`/city/${cityCode}`)
}

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#10B981'
  if (aqi <= 100) return '#FBBF24'
  if (aqi <= 150) return '#F97316'
  if (aqi <= 200) return '#EF4444'
  if (aqi <= 300) return '#A855F7'
  return '#7F1D1D'
}

const getAQIBgColor = (aqi) => {
  return getAQIColor(aqi) + '20'
}

const getAQILevel = (aqi) => {
  if (aqi <= 50) return '优'
  if (aqi <= 100) return '良'
  if (aqi <= 150) return '轻度'
  if (aqi <= 200) return '中度'
  if (aqi <= 300) return '重度'
  return '严重'
}

onMounted(() => {
  fetchCities()
})
</script>

<style scoped>
.cities-page {
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.city-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
}

.city-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.city-name {
  font-size: 16px;
  font-weight: 600;
}

.city-province {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

.city-aqi {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.aqi-value {
  font-size: 24px;
  font-weight: 700;
}

.aqi-level {
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
}
</style>
