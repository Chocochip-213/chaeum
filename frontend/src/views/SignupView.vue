<template>
  <div class="container">
    <AuthTemplate>
      <div class="signup-form-container">
        <div class="header">
          <h1>계정 만들기 🚀</h1>
          <p>채움과 함께 성장의 여정을 시작해보세요.</p>
        </div>
        <form @submit.prevent="onSignup">
          <div class="input-group">
            <User class="input-icon" :size="20" />
            <input type="text" v-model="name" placeholder="이름" class="styled-input" required />
          </div>
          <div class="input-group">
            <Building2 class="input-icon" :size="20" />
            <select v-model="selectedCampus" class="styled-input custom-select" required>
              <option value="서울 캠퍼스">서울 캠퍼스</option>
              <option value="대전 캠퍼스">대전 캠퍼스</option>
              <option value="구미 캠퍼스">구미 캠퍼스</option>
              <option value="광주 캠퍼스">광주 캠퍼스</option>
              <option value="부울경 캠퍼스">부울경 캠퍼스</option>
            </select>
            <ChevronDown class="arrow-icon" :size="20" />
          </div>
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
            <button type="submit" class="submit-btn">회원가입</button>
            <div class="login-link">
              이미 계정이 있으신가요?
              <RouterLink to="/login">로그인</RouterLink>
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
import { Mail, Lock, Eye, EyeOff, User, Building2, ChevronDown } from 'lucide-vue-next'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const showPassword = ref(false)
const name = ref('')
const selectedCampus = ref('서울 캠퍼스')
const email = ref('')
const password = ref('')

const onSignup = async () => {
  try {
    await api.post('/users/signup/', {
      email: email.value,
      password: password.value,
      nickname: name.value,
      campus: selectedCampus.value,
    })

    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data) {
      const errorData = error.response.data

      if (errorData.email) {
        const goToLogin = confirm('이미 가입된 이메일입니다. 로그인 페이지로 이동하시겠습니까?')

        if (goToLogin) {
          router.push('/login')
        } else {
          password.value = ''
        }
        return
      }
    }
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
.signup-form-container {
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
  color: #888;
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
  background-color: #f9fafb;
  color: #333333;
}
.styled-input:focus {
  border-color: #333333;
}

.custom-select {
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}

.arrow-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
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
  gap: 16px;
  margin-top: 10px;
}
.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: #2c2c2c;
  color: #ffffff;
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
.login-link {
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: #666666;
}
.login-link a {
  color: #333333;
  font-weight: bold;
  text-decoration: underline;
}
</style>
