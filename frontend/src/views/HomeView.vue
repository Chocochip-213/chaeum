<template>
  <div class="container">
    <div class="wrapper">
      <div class="card-container">
        <h1>당신의 부족한 2%를 채우는 시간</h1>
        <p>이력서 기반 역량 분석부터 맞춤형 도서 추천까지.<br />깊이 있는 성장을 경험하세요.</p>
        <div class="card-btn-container">
          <RouterLink to="analysis" class="first-btn">내 역량 분석하기</RouterLink>
          <RouterLink to="books" class="second-btn">인기 도서 보기</RouterLink>
        </div>
      </div>
      <div class="category-container">
        <div class="category-label">
          <Search color="#8d6e63" />
          <span>카테고리 탐색</span>
        </div>
        <div class="categories-container">
          <CategoryLabel v-for="category in categories" :key="category"
            >{{ category }}
          </CategoryLabel>
        </div>
      </div>
      <div class="best-container">
        <div class="category-label">
          <Star color="#eab308" fill="#eab308" />
          <span>베스트셀러</span>
        </div>
        <BestsellerList />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search, Star } from 'lucide-vue-next'
import CategoryLabel from '@/components/CategoryLabel.vue'
import BestsellerList from '@/components/BestsellerList.vue'

const categories = ref(['Engineering', 'Frontend', 'Backend', 'System Design', 'AI/ML'])
</script>

<style scoped>
.container {
  width: 100%;
  min-height: calc(100vh - 80px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.wrapper {
  width: 100%;
  max-width: 1024px;
  margin: 0 auto;
  padding: 60px 16px;
}

.card-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: linear-gradient(to right, #2c2c2c, #4a4a4a);
  color: #ffffff;
  border-radius: 12px;
  padding: 40px;
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -4px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.card-container p {
  color: #d1dadb;
}

.card-btn-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-btn-container a {
  padding: 12px 16px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
  cursor: pointer;
}

.first-btn {
  background-color: #ffffff;
  color: #1a1a1a;
}

.second-btn {
  background-color: #1a1a1a;
  color: #ffffff;
}

.category-container {
  display: flex;
  flex-direction: column;
  margin-top: 48px;
  gap: 24px;
}

.category-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-label span {
  font-size: 20px;
  font-weight: 600;
}

.categories-container {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.best-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 48px;
}
</style>
