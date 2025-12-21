<template>
  <header>
    <div class="inner">
      <div class="logo-container" @click="router.push({ name: 'home' })">
        <div class="logo"><BookOpen /></div>
        <h1>채움.</h1>
      </div>

      <nav>
        <ul>
          <li @click="router.push({ name: 'home' })">서재</li>
          <li class="search" @click="router.push({ name: 'book-list' })"><Search />도서 검색</li>
          <li @click="router.push({ name: 'analysis' })">AI 커리어</li>
          <li @click="router.push({ name: 'community' })">독서 모임</li>
        </ul>
      </nav>

      <div class="btn-container">
        <template v-if="authStore.isLogin">
          <div class="user-icon-wrapper" @click="handleLogout">
            <User :size="24" />
          </div>
        </template>

        <template v-else>
          <button class="btn-login" @click="router.push({ name: 'login' })">로그인</button>
          <button class="btn-signup" @click="router.push({ name: 'signup' })">회원가입</button>
        </template>
      </div>
    </div>
  </header>
</template>
<script setup>
import { BookOpen, Search, User } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
</script>

<style scoped>
header {
  width: 100%;
  position: sticky;
  top: 0;
  background-color: #ffffffe6;
  z-index: 10;
  border-bottom: 1px solid #e5e7eb;
}

.inner {
  max-width: 64rem;
  margin: 0 auto;
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo {
  width: 40px;
  height: 40px;
  background-color: #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
}

.logo svg {
  stroke: white;
}

h1 {
  font-size: 28px;
  cursor: pointer;
}

ul {
  display: flex;
  gap: 24px;
}

.search {
  display: flex;
  align-items: center;
  gap: 4px;
}

li {
  cursor: pointer;
  font-size: 18px;
  color: #5c5c5c;
  transition: all 0.2s;
  font-weight: 600;
}

li:hover {
  color: #1a1a1a;
}

li:hover svg {
  stroke: #1a1a1a;
}

.search svg {
  width: 16px;
  height: 16px;
  stroke: #5c5c5c;
  transition: stroke 0.2s;
}

.user-icon-wrapper {
  width: 44px;
  height: 44px;
  background-color: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #4b5563;
}

.user-icon-wrapper:hover {
  background-color: #e5e7eb;
}

.btn-container {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-self: end;
}

button {
  padding: 10px 18px;
  border-radius: 8px;
  border: 0;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
  font-family: inherit;
}

.btn-login {
  background-color: transparent;
  color: #555;
}

.btn-login:hover {
  background-color: #f3f4f6;
  color: #111;
}

.btn-signup {
  background-color: #2a2a2a;
  color: white;
}

.btn-signup:hover {
  background-color: #404040;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
