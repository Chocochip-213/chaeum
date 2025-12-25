<template>
  <div class="container">
    <AuthTemplate>
      <div class="login-form-container">
        <div class="header">
          <h1>환영합니다!</h1>
          <p>오늘도 성장을 위해 돌아오셨군요.</p>
        </div>
        <form @submit.prevent="onLogin">
          <div class="input-group">
            <Mail class="input-icon" :size="20" />
            <input
              type="email"
              v-model="email"
              placeholder="이메일 주소"
              class="styled-input"
              required
            />
          </div>
          <div class="input-group">
            <Lock class="input-icon" :size="20" />
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="비밀번호"
              class="styled-input"
              required
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
              <Eye v-if="!showPassword" :size="20" />
              <EyeOff v-else :size="20" />
            </button>
          </div>
          <div class="form-footer">
            <RouterLink to="/find-password" class="forgot-pw">비밀번호를 잊으셨나요?</RouterLink>
            <button type="submit" class="submit-btn">로그인</button>
            
            <div class="demo-login-wrapper">
              <button type="button" class="demo-btn" @click="handleDemoLogin">
                <PartyPopper :size="18" />
                체험하기
              </button>
              <div class="tooltip">회원가입 없이 1초 만에<br/>서비스를 이용해보세요!</div>
            </div>

            <div class="signup-link">
              아직 회원이 아니신가요?
              <RouterLink to="/signup">회원가입</RouterLink>
            </div>
          </div>
        </form>
      </div>
    </AuthTemplate>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AuthTemplate from '@/components/AuthTemplate.vue'
import { Mail, Lock, Eye, EyeOff, PartyPopper } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showPassword = ref(false)
const email = ref('')
const password = ref('')

const onLogin = async () => {
  try {
    const response = await api.post('/users/login/', {
      email: email.value,
      password: password.value,
    })

    const { access, refresh } = response.data
    authStore.login(access, refresh)

    router.push('/')
  } catch {
    alert('이메일 혹은 비밀번호를 확인해 주세요.')
  }
}

const handleDemoLogin = async () => {
  try {
    const response = await api.post('/users/demo-login/')
    
    if (response.data.access && response.data.refresh) {
        authStore.login(response.data.access, response.data.refresh)
    }

    router.push('/')
  } catch (error) {
    console.error('Demo login failed', error)
    alert('체험하기 로그인에 실패했습니다.')
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-form-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.header h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.header p {
  color: #888888;
  font-size: 14px;
}

.input-group {
  position: relative;
  margin-bottom: 16px;
}

.styled-input {
  width: 100%;
  padding: 14px;
  padding-left: 48px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
  background-color: #f9fafb;
}

.styled-input:focus {
  border-color: #333333;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.eye-btn {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
}

.form-footer {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 16px;
}

.forgot-pw {
  width: fit-content;
  text-align: right;
  font-size: 13px;
  color: #8d6e63;
  text-decoration: none;
  font-weight: 600;
}

.forgot-pw:hover {
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: #2c2c2c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background-color: #1a1a1a;
}

.signup-link {
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: #666666;
}

.signup-link a {
  color: #333333;
  font-weight: bold;
  text-decoration: underline;
}

.demo-login-wrapper {
  width: 100%;
  position: relative;
  display: flex;
  justify-content: center;
}

.demo-btn {
  width: 100%;
  padding: 14px;
  background-color: #f1f3f5;
  color: #495057;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.demo-btn:hover {
  background-color: #e9ecef;
  border-color: #ced4da;
  color: #212529;
}

/* Tooltip implementation */
.tooltip {
  visibility: hidden;
  background-color: #333;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 8px 12px;
  position: absolute;
  z-index: 1;
  bottom: 115%; /* Position above the button */
  left: 50%;
  transform: translateX(-50%);
  width: max-content;
  font-size: 13px;
  opacity: 0;
  transition: opacity 0.3s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  pointer-events: none;
}

.tooltip::after {
  content: "";
  position: absolute;
  top: 100%; /* At the bottom of the tooltip */
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #333 transparent transparent transparent;
}

.demo-login-wrapper:hover .tooltip {
  visibility: visible;
  opacity: 1;
}
</style>
