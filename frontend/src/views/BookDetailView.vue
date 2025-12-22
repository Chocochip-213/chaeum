<template>
  <div class="book-detail-container">
    <div class="back-link" @click="$router.go(-1)">
      <span class="arrow">&lt;</span> 이전 페이지로 돌아가기
    </div>

    <div v-if="loading" class="loading-container">
      <p>도서 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else class="content-wrapper">
      <section class="book-info-section">
        <div class="book-cover">
          <img v-if="book.cover" :src="book.cover" :alt="book.title" class="real-cover" />
          <div v-else class="cover-placeholder">
            <span class="cover-title">{{ book.title }}</span>
            <span class="cover-deco">No Image</span>
          </div>
        </div>

        <div class="book-details">
          <div class="badge-row">
            <span class="category-badge">{{ book.categoryName }}</span>
          </div>
          <h1 class="title">{{ book.title }}</h1>
          <p class="author-publisher">
            {{ book.author }} | {{ book.publisher }} | {{ book.pubDate }}
          </p>
          <div class="purchase-box">
            <div class="price-stock-row">
              <span class="price">{{ Number(book.priceSales).toLocaleString() }}원</span>
              <span class="stock-badge"> 📍 {{ book.stockStatus }}: 재고 있음 (위치: C-21) </span>
            </div>
            <a :href="book.link" target="_blank" class="buy-btn">
              온라인 서점 구매하기 (OutLink)
            </a>
          </div>
          <p class="description">{{ book.description }}</p>
          <div class="tag-section">
            <span v-for="(tag, index) in book.tags" :key="index" class="book-tag">
              {{ tag }}
            </span>
          </div>
        </div>
      </section>

      <section class="thread-section">
        <div class="section-header">
          <h3 class="section-title">
            <MessageSquare :size="20" class="icon-title" /> 독서 모임 스레드
          </h3>
          <button class="join-btn" @click="goToWrite">
            <Plus :size="14" stroke-width="3" /> 모임 글 작성하기
          </button>
        </div>

        <div v-if="isPostsLoading" class="status-msg">관련 게시글을 불러오는 중입니다...</div>

        <div v-else-if="posts.length > 0" class="thread-list">
          <div v-for="post in posts" :key="post.id" class="thread-card">
            <div class="card-header">
              <div class="user-profile">
                <div class="avatar">{{ post.user_nickname?.charAt(0) || '?' }}</div>
                <div class="user-info">
                  <div class="name-row">
                    <span class="username">{{ post.user_nickname }}</span>
                  </div>
                  <div class="meta-row">{{ formatTimeAgo(post.created_at) }}</div>
                </div>
              </div>
            </div>

            <div class="book-badge-sm">
              <span class="book-title-text">
                {{ bookTitles[post.book_isbn] || book.title }}
              </span>
            </div>

            <h3 class="post-title">{{ post.title }}</h3>

            <div class="card-content">{{ post.content }}</div>

            <div class="card-footer">
              <div class="actions">
                <span class="action-item"> <Heart :size="16" /> {{ post.view_count }} </span>
                <span class="action-item">
                  <MessageSquare :size="16" /> {{ post.comments?.length || 0 }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="thread-card empty-card">
          아직 작성된 스레드가 없습니다. 첫 번째 리뷰를 남겨보세요!
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import aladinApi from '@/api/aladin'
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plus, MessageSquare, Heart } from 'lucide-vue-next'
import { usePosts } from '@/composables/usePosts'
import { formatTimeAgo } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const book = ref({})

const { posts, bookTitles, isLoading: isPostsLoading, fetchPosts } = usePosts()

const fetchBookDetail = async () => {
  try {
    const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY
    const isbn13 = route.params.isbn13

    const response = await aladinApi.get('/ItemLookUp.aspx', {
      params: {
        ttbkey: TTB_KEY,
        itemIdType: 'ISBN13',
        ItemId: isbn13,
        output: 'js',
        Version: '20131101',
        Cover: 'Big',
      },
    })

    if (response.data.item && response.data.item.length > 0) {
      const item = response.data.item[0]
      const rawCategory = item.categoryName || ''
      const tags = rawCategory
        .split('>')
        .slice(1)
        .map((cat) => `#${cat.trim()}`)

      book.value = {
        title: item.title,
        author: item.author,
        publisher: item.publisher,
        pubDate: item.pubDate,
        description: item.description || '상세 설명이 없습니다.',
        priceStandard: item.priceStandard,
        priceSales: item.priceSales,
        cover: item.cover,
        categoryName: item.categoryName.split('>')[1] || 'General',
        link: item.link,
        stockStatus: item.stockStatus || 'SSAFY 서울점',
        tags: tags.length > 0 ? tags : ['#개발', '#프로그래밍'],
        isbn13: item.isbn13,
      }
    }
  } catch (error) {
    console.error('상세 데이터 로드 실패:', error)
  } finally {
    loading.value = false
  }
}

const loadBookPosts = () => {
  fetchPosts({
    book_isbn: route.params.isbn13,
    ordering: '-created_at',
  })
}

const goToWrite = () => {
  router.push({
    name: 'community-write',
    query: {
      isbn: route.params.isbn13,
      title: book.value.title,
      cover: book.value.cover,
      author: book.value.author,
      category: book.categoryName,
    },
  })
}

onMounted(() => {
  fetchBookDetail()
  loadBookPosts()
})

watch(
  () => route.params.isbn13,
  () => {
    fetchBookDetail()
    loadBookPosts()
  },
)
</script>

<style scoped>
.book-detail-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 20px;
}
.back-link {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 30px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.loading-container {
  text-align: center;
  padding: 100px;
  color: #888;
}
.book-info-section {
  display: flex;
  gap: 40px;
  margin-bottom: 60px;
}
.book-cover {
  flex-shrink: 0;
  width: 280px;
  height: 400px;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.real-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #fdfdfd;
  color: #e0cea1;
  text-align: center;
}
.cover-title {
  font-size: 2rem;
  font-weight: bold;
  color: #d4c49a;
  margin-top: 20px;
}
.cover-deco {
  font-size: 1.5rem;
  font-weight: bold;
  opacity: 0.3;
  line-height: 1.2;
}
.book-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
.badge-row {
  margin-bottom: 12px;
}
.category-badge {
  background-color: #f3f0e9;
  color: #8d6e63;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  align-self: flex-start;
}
.title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 10px 0;
  line-height: 1.3;
}
.author-publisher {
  color: #666;
  margin-bottom: 30px;
}
.purchase-box {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.price-stock-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.price {
  font-size: 1.5rem;
  font-weight: 700;
}
.stock-badge {
  background-color: #e6f4ea;
  color: #1e8e3e;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}
.buy-btn {
  width: 100%;
  padding: 16px;
  background-color: #222;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: center;
  text-decoration: none;
}
.buy-btn:hover {
  background-color: #444;
}
.description {
  line-height: 1.6;
  color: #444;
  margin-bottom: 24px;
}
.tag-section {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.book-tag {
  font-size: 0.85rem;
  color: #4f46e5;
  background-color: #eef2ff;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 2px solid #222;
  padding-bottom: 12px;
}
.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}
.join-btn {
  background: none;
  border: none;
  border-bottom: 2px solid #333;
  padding: 0 0 2px 0;
  color: #333;
  font-size: 0.95rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}
.join-btn:hover {
  opacity: 0.7;
}
.thread-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.thread-card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 24px;
  background: white;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}
.thread-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}
.empty-card {
  text-align: center;
  color: #888;
  padding: 40px;
}
.status-msg {
  text-align: center;
  color: #888;
  padding: 20px;
}
.card-header {
  margin-bottom: 16px;
}
.user-profile {
  display: flex;
  gap: 12px;
}
.avatar {
  width: 40px;
  height: 40px;
  background-color: #eee;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #666;
}
.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.username {
  font-weight: 700;
  font-size: 0.95rem;
}
.meta-row {
  font-size: 0.8rem;
  color: #888;
}
.post-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #111;
  margin: 0 0 12px 0;
  line-height: 1.4;
}
.card-content {
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #333;
}
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.actions {
  display: flex;
  gap: 16px;
  font-size: 0.85rem;
  color: #666;
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

.book-badge-sm {
  display: inline-block;
  background-color: #f3f4f6;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 12px;
}
.book-title-text {
  font-size: 0.8rem;
  color: #666;
  font-weight: 600;
}
</style>
