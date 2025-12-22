<template>
  <div class="community-container">
    <header class="community-header">
      <div class="title-area">
        <h1 class="main-title">독서 모임</h1>
        <p class="sub-title">함께 읽고, 성장하는 개발자들의 공간</p>
      </div>

      <div class="sort-tabs">
        <button
          class="tab-btn"
          :class="{ active: currentSort === '-created_at' }"
          @click="handleSortChange('-created_at')"
        >
          최신순
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentSort === '-view_count' }"
          @click="handleSortChange('-view_count')"
        >
          추천순
        </button>
      </div>
    </header>

    <div class="post-list">
      <div v-if="isLoading && posts.length === 0" class="status-msg">게시글을 불러오는 중...</div>
      <div v-else-if="!isLoading && posts.length === 0" class="status-msg">
        아직 작성된 게시글이 없습니다.
      </div>

      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="card-header">
          <div class="user-profile">
            <div class="avatar">{{ post.user_nickname?.charAt(0) || '?' }}</div>
            <div class="user-info">
              <span class="username">{{ post.user_nickname }}</span>
            </div>
          </div>
          <span class="time">{{ formatTimeAgo(post.created_at) }}</span>
        </div>
        <div class="book-badge" @click="goToBookDetail(post.book_isbn)">
          <Book :size="14" />
          <span class="book-title">
            {{ bookTitles[post.book_isbn] || '도서 정보 로딩 중...' }}
          </span>
        </div>

        <h3 class="post-title">{{ post.title }}</h3>

        <div class="post-content">
          {{ post.content }}
        </div>
        <div class="card-footer">
          <div class="actions">
            <button class="action-item"><Heart :size="18" /> {{ post.view_count }}</button>
            <button class="action-item">
              <MessageCircle :size="18" /> 댓글 {{ post.comments?.length || 0 }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <button class="fab-button" @click="goToWrite">
      <PencilLine :size="20" />
      <span>글쓰기</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Book, Heart, MessageCircle, PencilLine } from 'lucide-vue-next'
import { usePosts } from '@/composables/usePosts'
import { formatTimeAgo } from '@/utils/date'

const router = useRouter()
const currentSort = ref('-created_at')

const { posts, bookTitles, isLoading, fetchPosts } = usePosts()

const handleSortChange = (newSort) => {
  currentSort.value = newSort
  fetchPosts({ ordering: newSort })
}

onMounted(() => {
  fetchPosts({ ordering: currentSort.value })
})

const goToWrite = () => router.push({ name: 'community-write', query: { mode: 'select' } })
const goToBookDetail = (isbn) => router.push({ name: 'book-detail', params: { isbn13: isbn } })
</script>

<style scoped>
.community-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px 100px;
  position: relative;
}
.community-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}
.main-title {
  font-size: 28px;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
}
.sub-title {
  color: #666;
  font-size: 15px;
}
.sort-tabs {
  display: flex;
  gap: 16px;
}
.tab-btn {
  background: none;
  border: none;
  font-size: 15px;
  font-weight: 600;
  color: #999;
  padding-bottom: 4px;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn.active {
  color: #111;
  border-bottom: 2px solid #111;
}
.post-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.status-msg {
  text-align: center;
  padding: 40px;
  color: #888;
}
.post-card {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 24px;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}
.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}
.avatar {
  width: 40px;
  height: 40px;
  background-color: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #666;
  font-size: 14px;
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
.book-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background-color: #eef2ff;
  color: #4f46e5;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 16px;
  cursor: pointer;
}
.book-badge:hover {
  background-color: #e0e7ff;
}
.post-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 12px 0;
  line-height: 1.4;
}
.post-content {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 24px;
  word-break: break-all;
}
.card-footer {
  border-top: 1px solid #f5f5f5;
  padding-top: 16px;
}
.actions {
  display: flex;
  gap: 20px;
}
.action-item {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #888;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}
.action-item:hover {
  color: #111;
}
.fab-button {
  position: fixed;
  bottom: 40px;
  right: 40px;
  background-color: #111;
  color: white;
  padding: 14px 24px;
  border-radius: 50px;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.2s;
  z-index: 100;
}
.fab-button:hover {
  background-color: #333;
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
}
@media (max-width: 768px) {
  .community-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  .fab-button {
    bottom: 24px;
    right: 24px;
    padding: 12px 20px;
  }
}
</style>
