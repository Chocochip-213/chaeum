<template>
  <div class="container">
    <AuthTemplate>
      <div v-if="!isEmailSent" class="form-container">
        <div class="header">
          <h1>비밀번호 찾기 🔓</h1>
          <p>가입한 이메일 주소를 입력하시면 재설정 링크를 보내드립니다.</p>
        </div>

        <form @submit.prevent="onFindPassword">
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

          <div class="form-footer">
            <button type="submit" class="submit-btn" :disabled="isLoading">
              <span v-if="isLoading" class="loading-content">
                <Loader2 class="spin-icon" :size="20" />
                처리중...
              </span>
              <span v-else>재설정 링크 보내기</span>
            </button>
            <div class="login-link">
              비밀번호가 기억나셨나요? <RouterLink to="/login">로그인</RouterLink>
            </div>
          </div>
        </form>
      </div>

      <div v-else class="success-container">
        <div class="header">
          <h1>비밀번호를 잊으셨나요?</h1>
        </div>

        <div class="success-icon-area">
          <div class="icon-circle">
            <MailCheck :size="40" color="#22c55e" />
          </div>
        </div>

        <div class="success-message">
          <h2>메일 발송 완료!</h2>
          <p>
            입력하신 <strong>{{ email }}</strong
            >으로
            <br />
            재설정 링크를 보냈습니다.
            <br />
            메일함을 확인해주세요.
          </p>
        </div>

        <div class="form-footer">
          <router-link to="/login" class="submit-btn text-center">
            로그인 화면으로 돌아가기
          </router-link>

          <div class="login-link">비밀번호가 기억나셨나요? <a href="/login">로그인</a></div>
        </div>
      </div>
    </AuthTemplate>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AuthTemplate from '@/components/AuthTemplate.vue'
import { Mail, MailCheck, Loader2 } from 'lucide-vue-next'
import api from '@/api'

const email = ref('')
const isEmailSent = ref(false)
const isLoading = ref(false)

const onFindPassword = async () => {
  if (isLoading.value) return
  try {
    isLoading.value = true
    await api.post('/users/password/reset/', {
      email: email.value,
    })
    isEmailSent.value = true
  } catch {
    alert('가입된 메일을 찾을 수 없습니다.')
  } finally {
    isLoading.value = false
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

.form-container,
.success-container {
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
  color: #666;
  font-size: 14px;
  line-height: 1.5;
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
  transition: border-color 0.2s;
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
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.submit-btn:disabled {
  background-color: #555;
  cursor: not-allowed;
  opacity: 0.8;
}

.loading-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.spin-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.submit-btn:hover {
  background-color: #1a1a1a;
}

.login-link {
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #333;
  font-weight: bold;
  text-decoration: underline;
}

.success-icon-area {
  display: flex;
  justify-content: center;
  margin: 20px 0 10px 0;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background-color: #dcfce7;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.success-message {
  text-align: center;
}

.success-message h2 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
}

.success-message p {
  color: #666666;
  font-size: 14px;
  line-height: 1.6;
}

.success-message strong {
  color: #333333;
  text-decoration: underline;
}
</style>
