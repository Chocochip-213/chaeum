<template>
  <div class="write-page-wrapper">
    <div v-if="!selectedBook" class="step-search">
      <div class="step-header">
        <button class="close-btn" @click="$router.push({ name: 'community' })">
          &lt; 독서 모임으로 돌아가기
        </button>
      </div>
      <BookSearch mode="select" @select-book="handleSelectBook" />
    </div>

    <div v-else class="step-write animate-slide-up">
      <div class="write-container">
        <div class="top-nav">
          <button class="back-link" @click="selectedBook = null">
            <ChevronLeft :size="16" /> 책 다시 선택하기
          </button>
          <h1 class="page-title">글 작성하기</h1>
        </div>

        <div class="selected-book-card">
          <div class="book-cover">
            <img :src="selectedBook.cover" :alt="selectedBook.title" />
          </div>
          <div class="book-info">
            <span class="label">선택된 도서</span>
            <h3 class="book-title">{{ selectedBook.title }}</h3>
            <p class="book-author">{{ selectedBook.author || '저자 미상' }}</p>
          </div>
          <button class="change-btn" @click="selectedBook = null">변경</button>
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
              placeholder="이 책을 읽고 어떤 생각을 하셨나요? 자유롭게 이야기를 나눠보세요."
              class="content-textarea"
            ></textarea>
          </div>
        </div>

        <div class="button-group">
          <button class="btn-cancel" @click="$router.push({ name: 'community' })">취소</button>
          <button
            class="btn-submit"
            @click="handleSubmit"
            :disabled="!content.trim() || !postTitle.trim()"
          >
            <Send :size="16" /> 등록하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ChevronLeft, Send } from 'lucide-vue-next'
import api from '@/api'
import BookSearch from '@/components/BookSearch.vue'

const router = useRouter()
const route = useRoute()

const selectedBook = ref(null)
const postTitle = ref('')
const content = ref('')

//  검색 컴포넌트에서 선택 시
const handleSelectBook = (bookData) => {
  selectedBook.value = bookData
  window.scrollTo(0, 0)
}

const handleSubmit = async () => {
  if (!content.value.trim() || !postTitle.value.trim()) return

  try {
    await api.post('/community/posts/', {
      book_isbn: selectedBook.value.isbn || selectedBook.value.isbn13,
      title: postTitle.value,
      content: content.value,
    })

    alert('게시글이 등록되었습니다!')
    router.push({ name: 'community' })
  } catch (error) {
    console.error('글 등록 실패:', error)
    alert('등록 중 오류가 발생했습니다.')
  }
}

onMounted(() => {
  if (route.query.isbn) {
    selectedBook.value = {
      isbn: route.query.isbn,
      title: route.query.title,
      cover: route.query.cover,
      author: route.query.author,
    }
  }
})
</script>

<style scoped>
.write-page-wrapper {
  width: 100%;
  min-height: 100vh;
}
.step-header {
  max-width: 1024px;
  margin: 0 auto;
  padding: 20px 20px 0;
}
.close-btn {
  background: none;
  border: none;
  font-size: 0.95rem;
  color: #666;
  cursor: pointer;
  font-weight: 600;
}
.close-btn:hover {
  color: #111;
  text-decoration: underline;
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
.selected-book-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background-color: #f9fafb;
  margin-bottom: 30px;
} /* 마진 조정 */
.book-cover {
  width: 60px;
  height: 87px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #eee;
  background-color: #fff;
  margin-right: 20px;
  flex-shrink: 0;
}
.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.book-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.label {
  font-size: 13px;
  color: #d97706;
  font-weight: 600;
  margin-bottom: 4px;
}
.book-title {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin: 0 0 4px 0;
}
.book-author {
  font-size: 14px;
  color: #666;
  margin: 0;
}
.change-btn {
  background: none;
  border: none;
  font-size: 14px;
  color: #6b7280;
  text-decoration: underline;
  cursor: pointer;
  padding: 8px;
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

/* ★ 제목 입력창 스타일 추가 */
.input-wrapper {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  padding: 0 16px; /* 좌우 패딩만 */
  background: white;
  transition: border-color 0.2s;
}
.input-wrapper:focus-within {
  border-color: #111;
}
.title-input {
  width: 100%;
  height: 50px; /* 높이 고정 */
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
