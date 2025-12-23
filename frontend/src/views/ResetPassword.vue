<template>
  <div class="container">
    <AuthTemplate>
      <div class="reset-form-container">
        <div class="header">
          <h1>비밀번호 재설정</h1>
          <p>계정에 사용할 새로운 비밀번호를 설정해주세요.</p>
        </div>

        <form @submit.prevent="onResetPassword">
          <div class="input-group">
            <Lock class="input-icon" :size="20" />
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="새로운 비밀번호"
              class="styled-input"
              required
              minlength="8"
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
              <Eye v-if="!showPassword" :size="20" />
              <EyeOff v-else :size="20" />
            </button>
          </div>

          <div class="input-group">
            <Lock class="input-icon" :size="20" />
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="비밀번호 확인"
              class="styled-input"
              :class="{ 'input-error': passwordMismatch }"
              required
            />
            <button
              type="button"
              class="eye-btn"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <Eye v-if="!showConfirmPassword" :size="20" />
              <EyeOff v-else :size="20" />
            </button>
          </div>

          <p v-if="passwordMismatch" class="error-message">비밀번호가 일치하지 않습니다.</p>

          <div class="form-footer">
            <button type="submit" class="submit-btn">비밀번호 변경하기</button>
            <div class="login-link">
              비밀번호가 기억나셨나요?
              <RouterLink to="/login">로그인</RouterLink>
            </div>
          </div>
        </form>
      </div>
    </AuthTemplate>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AuthTemplate from '@/components/AuthTemplate.vue'
import { Lock, Eye, EyeOff } from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const uidb64 = ref('')
const token = ref('')

onMounted(() => {
  uidb64.value = route.params.uidb64
  token.value = route.params.token
})

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && password.value !== confirmPassword.value
})

const onResetPassword = async () => {
  if (password.value !== confirmPassword.value) {
    alert('비밀번호가 서로 일치하지 않습니다.')
    return
  }
  try {
    await api.post('/users/password/reset/confirm/', {
      new_password: password.value,
      uidb64: uidb64.value,
      token: token.value,
    })
    alert('비밀번호가 성공적으로 변경되었습니다.')
    router.push('/login')
  } catch (error) {
    console.error('비밀번호 변경 실패:', error)
    alert('비밀번호 변경 중 오류가 발생했습니다.')
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
.reset-form-container {
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
  transition: border-color 0.2s;
}
.styled-input:focus {
  border-color: #333333;
}

.styled-input.input-error {
  border-color: #ef4444;
}

.input-icon {
  position: absolute;
  left: 14px;
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

.error-message {
  font-size: 13px;
  color: #ef4444;
  margin-top: -10px;
  margin-bottom: 10px;
  padding-left: 4px;
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
