<template>
  <div class="community-container">
    <header class="detail-header">
      <button class="back-btn" @click="goBack">
        <ChevronLeft :size="24" />
        <span>이전 페이지로 돌아가기</span>
      </button>
    </header>

    <div v-if="isLoading" class="status-msg">게시글을 불러오는 중...</div>

    <div v-else-if="post" class="content-wrapper">
      <article class="post-card detail-card">
        <div class="card-header">
          <div class="user-profile">
            <div class="avatar">{{ post.user_nickname?.charAt(0) || '?' }}</div>
            <div class="user-info">
              <span class="username">{{ post.user_nickname }}</span>
              <span class="time">{{ formatTimeAgo(post.created_at) }}</span>
            </div>
          </div>
          <div class="post-header-actions">
            <div v-if="isMine" class="action-buttons">
              <button class="btn-text edit" @click="goToEdit">수정</button>
              <span class="divider">|</span>
              <button class="btn-text delete" @click="handleDelete">삭제</button>
            </div>
          </div>
        </div>

        <div v-if="post.book_isbn" class="book-badge" @click="goToBookDetail(post.book_isbn)">
          <Book :size="14" />
          <span class="book-text">
            {{ bookTitle || '도서 정보 로딩 중...' }}
          </span>
          <ChevronRight :size="14" class="arrow-icon" />
        </div>

        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-content">
          {{ post.content }}
        </div>

        <div class="card-footer">
          <button class="action-btn">
            <Eye :size="18" />
            <span>{{ post.view_count }}</span>
          </button>
        </div>
      </article>

      <section class="comments-section">
        <h3 class="section-title">
          <MessageCircle :size="20" />
          댓글 <span class="count">{{ post.comments?.length || 0 }}</span>
        </h3>

        <div class="comment-form">
          <div class="avatar sm">나</div>
          <div class="input-wrapper">
            <input
              type="text"
              v-model="newCommentContent"
              placeholder="따뜻한 댓글을 남겨주세요..."
              @keydown.enter.prevent="submitComment($event)"
            />

            <button
              class="send-btn"
              :disabled="!newCommentContent.trim() || isSubmitting"
              @click="submitComment"
            >
              <Send :size="18" />
            </button>
          </div>
        </div>

        <div class="comment-list">
          <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
            <div class="comment-avatar">
              <div class="avatar sm">{{ comment.user_nickname?.charAt(0) }}</div>
            </div>
            <div class="comment-body">
              <div class="comment-meta">
                <span class="username">{{ comment.user_nickname }}</span>
                <span class="time">{{ formatTimeAgo(comment.created_at) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
            </div>
          </div>

          <div v-if="!post.comments?.length" class="no-comments">
            아직 댓글이 없습니다. 첫 번째 댓글을 남겨보세요!
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeft, ChevronRight, Book, Eye, MessageCircle, Send } from 'lucide-vue-next'
import { formatTimeAgo } from '@/utils/date'
import api from '@/api'
import aladinApi from '@/api/aladin'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()

const post = ref(null)
const isLoading = ref(true)
const newCommentContent = ref('')
const isSubmitting = ref(false)
const bookTitle = ref('')

// TODO: 글 작성자 여부 판단 로직 추가 필요
const isMine = computed(() => {
  // return currentUser.value?.id === post.value?.user_id
  return true
})

const goToEdit = () => {
  router.push({
    name: 'community-edit',
    params: { id: post.value.id },
    query: {
      book_title: bookTitle.value || '책 정보',
      book_isbn: post.value.book_isbn,
    },
  })
}

const handleDelete = async () => {
  if (confirm('게시글을 삭제하시겠습니까?')) {
    try {
      await api.delete(`/community/posts/${post.value.id}/`)

      alert('삭제되었습니다.')
      router.push({ name: 'community' })
    } catch (error) {
      console.error('삭제 실패:', error)
      alert('삭제 중 오류가 발생했습니다.')
    }
  }
}

const postId = route.params.id

const fetchBookTitle = async (isbn) => {
  if (!isbn) return

  try {
    const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY
    const response = await aladinApi.get('/ItemLookUp.aspx', {
      params: {
        ttbkey: TTB_KEY,
        itemIdType: 'ISBN13',
        ItemId: isbn,
        output: 'js',
        Version: '20131101',
      },
    })

    if (response.data?.item?.length > 0) {
      bookTitle.value = response.data.item[0].title
    } else {
      bookTitle.value = '도서 정보 없음'
    }
  } catch (error) {
    console.error(`책 제목 조회 실패 (${isbn})`, error)
    bookTitle.value = '도서 정보 조회 실패'
  }
}

const fetchPost = async () => {
  try {
    isLoading.value = true
    const response = await api.get(`/community/posts/${postId}/`)
    post.value = response.data

    if (post.value.book_isbn) {
      fetchBookTitle(post.value.book_isbn)
    }
  } catch (error) {
    console.error('Error fetching post:', error)
    alert('게시글을 불러오지 못했습니다.')
    router.back()
  } finally {
    isLoading.value = false
  }
}

const submitComment = async (event) => {
  if (event && event.isComposing) return

  const content = newCommentContent.value.trim()
  if (!content || isSubmitting.value) return

  try {
    isSubmitting.value = true

    const response = await api.post(`/community/posts/${postId}/comments/`, {
      content: content,
    })

    const newComment = response.data

    if (!post.value.comments) {
      post.value.comments = []
    }

    post.value.comments.push(newComment)

    newCommentContent.value = ''
  } catch (error) {
    console.error('Comment submit error:', error)
    alert('댓글 작성 실패')
  } finally {
    isSubmitting.value = false
  }
}

const goBack = () => router.back()
const goToBookDetail = (isbn) => router.push({ name: 'book-detail', params: { isbn13: isbn } })

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.community-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 40px 20px 100px;
}

.detail-header {
  margin-bottom: 24px;
}
.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}
.back-btn:hover {
  color: #111;
}

.post-card {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  background-color: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #666;
  font-size: 16px;
}
.avatar.sm {
  width: 32px;
  height: 32px;
  font-size: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 700;
  font-size: 16px;
  color: #111;
}

.time {
  font-size: 13px;
  color: #aaa;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #888;
}
.btn-text {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 14px;
  padding: 0;
}
.btn-text:hover {
  text-decoration: underline;
  color: #111;
}
.btn-text.delete:hover {
  color: #ef4444;
}
.divider {
  color: #e5e7eb;
}

.book-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #eef2ff;
  color: #4f46e5;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.book-badge:hover {
  background-color: #e0e7ff;
}
.arrow-icon {
  opacity: 0.5;
}

.post-title {
  font-size: 24px;
  font-weight: 800;
  color: #111;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

.post-content {
  font-size: 16px;
  line-height: 1.7;
  color: #333;
  min-height: 100px;
  white-space: pre-wrap;
  margin-bottom: 40px;
}

.card-footer {
  border-top: 1px solid #f5f5f5;
  padding-top: 20px;
}

.stat-item,
.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #888;
}

.action-btn {
  background: none;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
}

.comments-section {
  margin-top: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #111;
}
.count {
  color: #4f46e5;
}

.comment-form {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  align-items: flex-start;
}
.input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}
.input-wrapper input {
  width: 100%;
  background-color: #f5f5f5;
  border: 1px solid transparent;
  border-radius: 24px;
  padding: 14px 50px 14px 20px;
  font-size: 15px;
  transition: all 0.2s;
  outline: none;
}
.input-wrapper input:focus {
  background-color: white;
  border-color: #ddd;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.send-btn {
  position: absolute;
  right: 8px;
  background-color: #111;
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
}
.send-btn:disabled {
  background-color: #ddd;
  cursor: not-allowed;
  opacity: 0.7;
}
.send-btn:not(:disabled):hover {
  transform: scale(1.05);
  background-color: #333;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-body {
  flex: 1;
  background-color: #fff;
  border-radius: 24px;
  padding: 12px;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-text {
  font-size: 15px;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
}

.no-comments {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 14px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.status-msg {
  text-align: center;
  padding: 60px;
  color: #888;
}

@media (max-width: 768px) {
  .post-card {
    padding: 20px;
  }
  .post-title {
    font-size: 20px;
  }
}
</style>
