<template>
  <div class="container">
    <div class="auth-card">
      <div class="left-template">
        <div class="logo-container">
          <div class="logo"><BookOpen :size="20" /></div>
          <h2>채움.</h2>
        </div>
        <h1>성장의 빈틈을 채우는 시간</h1>
        <p>이력서 기반 AI 역량 분석과 맞춤형 도서 추천으로 더 나은 개발자로 성장하세요.</p>
      </div>
      <div class="right-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { BookOpen } from 'lucide-vue-next'
</script>

<style scoped>
.auth-card {
  background-color: #ffffff;
  width: 100%;
  max-width: 896px;
  height: 600px;
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  overflow: hidden;
  position: relative;
  word-break: keep-all;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo {
  background-color: #5b5b5b;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
}

.logo svg {
  stroke: #ffffff;
}

.left-template {
  width: 50%;
  display: none;

  flex-direction: column;
  gap: 12px;
  padding: 48px;
  color: #ffffff;
  background: linear-gradient(to bottom right, #222222, #666666);
}

@media (min-width: 768px) {
  .left-template {
    display: flex;
  }
}

.right-content {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
