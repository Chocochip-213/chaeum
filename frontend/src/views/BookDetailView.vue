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
          <div class="category-badge">{{ book.categoryName }}</div>

          <h1 class="title">{{ book.title }}</h1>
          <p class="author-publisher">{{ book.author }} | {{ book.publisher }}</p>

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
        </div>
      </section>

      <section class="thread-section">
        <div class="section-header">
          <h3 class="section-title">
            <MessageSquare :size="20" class="icon-title" /> 독서 모임 스레드
          </h3>

          <button class="join-btn"><Plus :size="14" stroke-width="3" /> 모임 글 작성하기</button>
        </div>

        <div v-if="dummyThreads.length > 0" class="thread-list">
          <div v-for="thread in dummyThreads" :key="thread.id" class="thread-card">
            <div class="card-header">
              <div class="user-profile">
                <div class="avatar">{{ thread.username.charAt(0) }}</div>
                <div class="user-info">
                  <div class="name-row">
                    <span class="username">{{ thread.username }}</span>
                  </div>
                  <div class="meta-row">{{ thread.time }}</div>
                </div>
              </div>
            </div>
            <div class="card-content">{{ thread.content }}</div>
            <div class="card-footer">
              <div class="actions">
                <span class="action-item"> <Heart :size="16" /> {{ thread.likes }} </span>
                <span class="action-item">
                  <MessageSquare :size="16" /> {{ thread.comments }}
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Plus, MessageSquare, Heart } from 'lucide-vue-next'

const route = useRoute()
const loading = ref(true)
const book = ref({})

// 임시 스레드 데이터
const dummyThreads = ref([
  {
    id: 1,
    username: '서주미',
    time: '2시간 전',
    content:
      'AI 튜터가 설명해준 3장 함수 요약이 정말 좋네요. "함수는 한 가지만 해야 한다"는 원칙을 제 코드에 적용해보았습니다.',
    likes: 24,
    comments: 2,
  },
  {
    id: 2,
    username: '김민우',
    time: '5시간 전',
    content:
      '이 책 처음 읽어보는데 생각보다 어렵네요 ㅠㅠ 다들 1장 깨끗한 코드 부분 어떻게 이해하셨나요?',
    likes: 5,
    comments: 8,
  },
])

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
      }
    } else {
      console.error('책 정보를 찾을 수 없습니다.')
    }
  } catch (error) {
    console.error('상세 데이터를 불러오지 못했습니다.', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBookDetail()
})
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
.category-badge {
  background-color: #f0f0f0;
  color: #666;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  align-self: flex-start;
  margin-bottom: 12px;
}
.title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 10px 0;
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
}
.empty-card {
  text-align: center;
  color: #888;
  padding: 40px;
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
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
