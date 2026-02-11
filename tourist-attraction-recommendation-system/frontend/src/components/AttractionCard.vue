<template>
  <div
    class="attraction-card"
    @click="handleClick"
  >
    <!-- 封面图片 -->
    <div class="card-image-wrapper">
      <img
        :src="attraction.cover_image || attraction.coverImage || defaultImage"
        :alt="attraction.name"
        class="card-image"
        @error="handleImageError"
      />
      <!-- 图片叠加渐变 -->
      <div class="image-overlay"></div>

      <!-- 分类标签 -->
      <div class="category-badge">
        {{ attraction.category || '景点' }}
      </div>

      <!-- 评分标签 -->
      <div class="rating-badge" v-if="displayRating > 0">
        <svg class="star-icon" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
        <span>{{ displayRating.toFixed(1) }}</span>
      </div>
    </div>

    <!-- 景点信息 -->
    <div class="card-content">
      <h3 class="attraction-name">{{ attraction.name }}</h3>
      <p class="attraction-description">{{ attraction.description || '暂无简介' }}</p>

      <!-- 底部信息 -->
      <div class="card-footer">
        <div class="location-info">
          <svg class="location-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
          </svg>
          <span class="location-text">{{ attraction.address || '地址未知' }}</span>
        </div>
        <div class="view-details">
          <span>查看详情</span>
          <svg class="arrow-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  attraction: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const router = useRouter()
const defaultImage = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop'

// 计算评分 - 如果有直接评分就用，否则基于评论计算
const displayRating = computed(() => {
  if (props.attraction.rating) return props.attraction.rating
  if (props.attraction.avg_rating) return props.attraction.avg_rating
  return 0
})

function handleClick() {
  router.push(`/attractions/${props.attraction.id}`)
}

function handleImageError(e) {
  e.target.src = defaultImage
}
</script>

<style scoped>
.attraction-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.attraction-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-image-wrapper {
  position: relative;
  height: 220px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.attraction-card:hover .card-image {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent 50%,
    rgba(0, 0, 0, 0.6) 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.attraction-card:hover .image-overlay {
  opacity: 1;
}

.category-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 14px;
  background: rgba(249, 115, 22, 0.95);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.rating-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.star-icon {
  width: 16px;
  height: 16px;
  color: #f59e0b;
}

.rating-badge span {
  font-size: 13px;
  font-weight: 700;
  color: #1f2937;
}

.card-content {
  padding: 20px;
}

.attraction-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.attraction-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.location-icon {
  width: 16px;
  height: 16px;
  color: #9ca3af;
  flex-shrink: 0;
}

.location-text {
  font-size: 13px;
  color: #9ca3af;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.view-details {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
  color: #f97316;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.attraction-card:hover .view-details {
  gap: 8px;
}

.arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.attraction-card:hover .arrow-icon {
  transform: translateX(4px);
}
</style>
