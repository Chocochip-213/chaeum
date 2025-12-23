<template>
  <div class="write-page-wrapper">
    <div class="step-write animate-slide-up">
      <div class="write-container">
        <div class="top-nav">
          <button class="back-link" @click="$router.back()">
            <ChevronLeft :size="16" /> 뒤로 가기
          </button>
          <h1 class="page-title">글 수정하기</h1>
        </div>

        <div class="input-section">
          <label class="input-label">제목</label>
          <div class="input-wrapper">
            <input
              v-model="postTitle"
              type="text"
              placeholder="게시글 제목을 입력해주세요."
              class="title-input"
            />
          </div>
        </div>

        <div class="input-section">
          <label class="input-label">내용</label>
          <div class="textarea-wrapper">
            <textarea
              v-model="content"
              placeholder="내용을 입력해주세요."
              class="content-textarea"
            ></textarea>
          </div>
        </div>

        <div class="button-group">
          <button class="btn-cancel" @click="$router.back()">취소</button>
          <button
            class="btn-submit"
            @click="handleUpdate"
            :disabled="!content.trim() || !postTitle.trim()"
          >
            <Check :size="16" /> 수정 완료
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ChevronLeft, Check } from 'lucide-vue-next'
import api from '@/api'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const { id: currentUserId } = storeToRefs(userStore)

const postId = route.params.id
const postTitle = ref('')
const content = ref('')

const post = ref(null)
const isLoading = ref(true)

const fetchPostDetail = async () => {
  try {
    const response = await api.get(`/community/posts/${postId}/`)
    post.value = response.data

    postTitle.value = post.value.title
    content.value = post.value.content

    checkPermission()
  } catch (error) {
    console.error('게시글 불러오기 실패:', error)
    router.back()
  } finally {
    isLoading.value = false
  }
}

const checkPermission = () => {
  if (!post.value || !currentUserId.value) return

  const authorId = post.value.user_id

  if (String(currentUserId.value) !== String(authorId)) {
    alert('수정 권한이 없는 게시글입니다.')
    router.replace({ name: 'community-detail', params: { id: postId } })
  }
}

const handleUpdate = async () => {
  if (!postTitle.value.trim() || !content.value.trim()) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  try {
    await api.put(`/community/posts/${postId}/`, {
      title: postTitle.value,
      content: content.value,
    })

    router.replace({ name: 'community-detail', params: { id: postId } })
  } catch (error) {
    console.error('글 수정 실패:', error)
  }
}

onMounted(async () => {
  isLoading.value = true

  if (!userStore.userInfo) {
    await userStore.fetchUserProfile()
  }

  if (postId) {
    await fetchPostDetail()
  }
})
</script>

<style scoped>
.write-page-wrapper {
  width: 100%;
  min-height: 100vh;
}
.write-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 40px 20px;
}
.top-nav {
  margin-bottom: 30px;
}
.back-link {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 0;
  margin-bottom: 12px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #111;
}

.input-section {
  margin-bottom: 30px;
}
.input-label {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin-bottom: 12px;
}

.input-wrapper {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  padding: 0 16px;
  background: white;
  transition: border-color 0.2s;
}
.input-wrapper:focus-within {
  border-color: #111;
}
.title-input {
  width: 100%;
  height: 50px;
  border: none;
  font-size: 16px;
  outline: none;
  font-weight: 500;
  color: #333;
}

.textarea-wrapper {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  padding: 16px;
  transition: border-color 0.2s;
  background: white;
}
.textarea-wrapper:focus-within {
  border-color: #111;
}
.content-textarea {
  width: 100%;
  height: 300px;
  border: none;
  resize: none;
  font-size: 16px;
  line-height: 1.6;
  outline: none;
  font-family: inherit;
  color: #333;
}
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.btn-cancel {
  padding: 14px 32px;
  border-radius: 8px;
  border: none;
  background-color: #f3f4f6;
  color: #4b5563;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn-submit {
  padding: 14px 32px;
  border-radius: 8px;
  border: none;
  background-color: #111;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-submit:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
