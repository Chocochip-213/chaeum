<template>
  <div class="container">
    <AuthTemplate>
      <div class="login-form-container">
        <div class="header">
          <h1>환영합니다! 👋</h1>
          <p>오늘도 성장을 위해 돌아오셨군요.</p>
        </div>
        <form @submit.prevent="">
          <div class="input-group">
            <Mail class="input-icon" :size="20" />
            <input type="email" placeholder="이메일 주소" class="styled-input" required />
          </div>
          <div class="input-group">
            <Lock class="input-icon" :size="20" />
            <input
              :type="showPassword ? 'text' : 'password'"
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
            <a href="/find-password" class="forgot-pw">비밀번호를 잊으셨나요?</a>
            <button type="submit" class="submit-btn">로그인</button>

            <div class="signup-link">아직 회원이 아니신가요? <a href="/signup">회원가입</a></div>
          </div>
        </form>
      </div>
    </AuthTemplate>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AuthTemplate from '@/components/AuthTemplate.vue'
import { Mail, Lock, Eye, EyeOff } from 'lucide-vue-next'

const showPassword = ref(false)
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
</style>
