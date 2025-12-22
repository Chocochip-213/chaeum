<template>
  <header>
    <div class="inner">
      <div class="logo-container" @click="router.push({ name: 'home' })">
        <div class="logo"><BookOpen /></div>
        <h1>채움.</h1>
      </div>

      <button class="mobile-menu-btn" @click="toggleMenu">
        <X v-if="isMenuOpen" />
        <Menu v-else />
      </button>

      <div class="menu-group" :class="{ 'is-open': isMenuOpen }">
        <nav>
          <ul>
            <li @click="handleNavClick('home')">서재</li>
            <li class="search" @click="handleNavClick('book-list')"><Search />도서 검색</li>
            <li @click="handleNavClick('analysis')">AI 커리어</li>
            <li @click="handleNavClick('community')">독서 모임</li>
          </ul>
        </nav>

        <div class="btn-container">
          <template v-if="authStore.isLogin">
            <div class="user-icon-wrapper" @click="">
              <User :size="24" />
            </div>
          </template>

          <template v-else>
            <button class="btn-login" @click="handleNavClick('login')">로그인</button>
            <button class="btn-signup" @click="handleNavClick('signup')">회원가입</button>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { BookOpen, Search, User, Menu, X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleNavClick = (routeName) => {
  router.push({ name: routeName })
  isMenuOpen.value = false
}

</script>

<style scoped>
header {
  width: 100%;
  position: sticky;
  top: 0;
  background-color: #ffffffe6;
  backdrop-filter: blur(8px);
  z-index: 50;
  border-bottom: 1px solid #e5e7eb;
}

.inner {
  max-width: 64rem;
  margin: 0 auto;
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  position: relative;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 51;
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
  white-space: nowrap;
}

.menu-group {
  display: contents;
}

nav {
  justify-self: center;
}

ul {
  display: flex;
  gap: 24px;
  list-style: none;
  padding: 0;
  margin: 0;
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
  white-space: nowrap;
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

.btn-container {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-self: end;
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

button {
  padding: 10px 18px;
  border-radius: 8px;
  border: 0;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
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
}

.mobile-menu-btn {
  display: none;
  background: none;
  padding: 4px;
  color: #1a1a1a;
  z-index: 51;
}

@media (max-width: 768px) {
  .inner {
    display: flex; 
    justify-content: space-between;
    padding: 0.75rem 1rem;
  }

  .mobile-menu-btn {
    display: block;
  }

  .menu-group {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    padding: 0;
    border-bottom: 1px solid #e5e7eb;
    background-color: #ffffffe6;
    backdrop-filter: blur(8px);
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
  }

  .menu-group.is-open {
    max-height: 400px;
    padding-bottom: 20px;
  }

  nav {
    width: 100%;
    justify-self: stretch;
  }

  ul {
    flex-direction: column;
    align-items: center;
    gap: 0;
    width: 100%;
  }

  li {
    width: 100%;
    text-align: center;
    padding: 16px 0;
    border-bottom: 1px solid #f3f4f6;
  }

  .search {
    justify-content: center;
  }

  .btn-container {
    flex-direction: column;
    width: 100%;
    gap: 12px;
    margin-top: 20px;
    justify-self: center;
  }

  .btn-login, .btn-signup {
    width: 90%;
  }
}
</style>