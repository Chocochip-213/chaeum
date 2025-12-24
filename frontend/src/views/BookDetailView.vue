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
          <div class="image-wrapper">
             <div class="carousel-container">
               <div 
                 class="carousel-track" 
                 :style="{ transform: `translateX(-${currentImageIndex * 100}%)` }"
               >
                  <!-- 통합 슬라이드 루프 -->
                  <div 
                    v-for="(img, index) in allImages" 
                    :key="index" 
                    class="carousel-slide"
                  >
                     <img :src="img" :alt="book.title" class="real-cover" />
                  </div>
                  
                  <!-- 이미지가 아예 없는 경우 (allImages empty) -->
                  <div v-if="allImages.length === 0" class="carousel-slide placeholder-slide">
                    <div class="cover-placeholder">
                      <span class="cover-title">{{ book.title }}</span>
                      <span class="cover-deco">No Image</span>
                    </div>
                  </div>
               </div>
             </div>
            
            <!-- Navigation Buttons -->
            <button 
              v-if="allImages && allImages.length > 1" 
              class="nav-btn prev" 
              @click.stop="prevImage"
            >
              <ChevronLeft size="32" stroke-width="2.5" />
            </button>
            <button 
              v-if="allImages && allImages.length > 1" 
              class="nav-btn next" 
              @click.stop="nextImage"
            >
              <ChevronRight size="32" stroke-width="2.5" />
            </button>
 
             <!-- Dots Indicator -->
            <div v-if="allImages && allImages.length > 1" class="carousel-dots">
              <span 
                v-for="(_, idx) in allImages" 
                :key="idx" 
                class="dot" 
                :class="{ active: idx === currentImageIndex }"
              ></span>
            </div>
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

              <button class="check-stock-btn" @click="checkStock" :disabled="stockLoading">
                <span v-if="stockLoading">위치 확인 중...</span>
                <span v-else>내 주변 서점 재고 확인</span>
              </button>
            </div>

            <div v-if="showStockList" class="stock-result-box">
              <div v-if="stockLoading" class="stock-loading">데이터를 불러오고 있습니다...</div>

              <div v-else-if="stockInfo && stockInfo.stores.length > 0" class="store-list">
                <div class="stock-summary">
                  총 <strong>{{ stockInfo.count }}</strong
                  >개의 서점이 발견되었습니다.
                </div>
                <div
                  v-for="(store, idx) in stockInfo.stores.slice(0, 4)"
                  :key="idx"
                  class="store-item"
                >
                  <div class="store-info">
                    <span class="store-name">{{ store.name }}</span>
                    <span class="store-dist">{{ store.distance_km.toFixed(1) }}km</span>
                  </div>
                  <div class="store-status">
                    <span class="status-badge" :class="{ 'in-stock': store.stock_status !== '0' }">
                      {{ store.stock_status }}
                    </span>
                    <a v-if="store.link" :href="store.link" target="_blank" class="store-link"
                      >위치보기</a
                    >
                  </div>
                </div>
              </div>

              <div v-else-if="stockInfo" class="no-stock">재고가 있는 서점이 없습니다.</div>
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
          <div v-for="post in posts" :key="post.id" class="thread-card" @click="goToPost(post.id)">
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
                <span class="action-item"> <Eye :size="16" /> {{ post.view_count }} </span>
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
import api from '@/api'
import aladinApi from '@/api/aladin'
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plus, MessageSquare, Eye, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { usePosts } from '@/composables/usePosts'
import { formatTimeAgo } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const book = ref({})
const stockInfo = ref(null)
const stockLoading = ref(false)
const showStockList = ref(false)

// [추가] 이미지 슬라이드 관련 상태
const currentImageIndex = ref(0)
const allImages = computed(() => {
  // 1. 미리보기가 있으면 미리보기만 보여줌 (표지 제외)
  if (book.value.previewImgList && book.value.previewImgList.length > 0) {
    return book.value.previewImgList
  }
  // 2. 미리보기가 없으면 표지만 보여줌
  if (book.value.cover) {
    return [book.value.cover]
  }
  return []
})

const prevImage = (e) => {
  e.stopPropagation() // 클릭 이벤트 전파 방지
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  } else {
    currentImageIndex.value = allImages.value.length - 1 // 루프
  }
}

const nextImage = (e) => {
  e.stopPropagation()
  if (currentImageIndex.value < allImages.value.length - 1) {
    currentImageIndex.value++
  } else {
    currentImageIndex.value = 0 // 루프
  }
}

const checkStock = () => {
  stockLoading.value = true
  showStockList.value = true
  stockInfo.value = null
  if (!navigator.geolocation) {
    alert('브라우저가 위치 정보를 지원하지 않습니다.')
    stockLoading.value = false
    return
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const lat = position.coords.latitude
      const lon = position.coords.longitude

      try {
        const response = await api.get(`/books/${route.params.isbn13}/stock/`, {
          params: { lat: lat, lon: lon },
        })
        stockInfo.value = response.data
      } catch (error) {
        console.error('재고 조회 실패:', error)
      } finally {
        stockLoading.value = false
      }
    },
    (err) => {
      console.error(err)
      alert('위치 정보를 허용해 주세요.')
      stockLoading.value = false
    },
  )
}

const { posts, bookTitles, isLoading: isPostsLoading, fetchPosts } = usePosts()
const goToPost = (id) => router.push({ name: 'community-detail', params: { id: id } })

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
        OptResult: 'previewImgList,packing,ratingInfo', 
      },
    })

    if (response.data.item && response.data.item.length > 0) {
      const item = response.data.item[0]
      const rawCategory = item.categoryName || ''
      const tags = rawCategory
        .split('>')
        .slice(1)
        .map((cat) => `#${cat.trim()}`)

      let previews = item.previewImgList || []
      if (!previews || previews.length === 0) {
        if (item.subInfo && item.subInfo.previewImgList) {
          previews = item.subInfo.previewImgList
        }
      }

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
        tags: tags.length > 0 ? tags : ['#개발', '#프로그래밍'],
        isbn13: item.isbn13,
        previewImgList: previews
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
.loading-container,
.status-msg {
  text-align: center;
  padding: 100px 0;
  color: #888;
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

.book-info-section {
  display: flex;
  gap: 40px;
  margin-bottom: 60px;
}
.book-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
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

.check-stock-btn {
  background-color: #fff;
  border: 1px solid #1e8e3e;
  color: #1e8e3e;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.check-stock-btn:hover {
  background-color: #e6f4ea;
}
.check-stock-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.stock-result-box {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #eee;
  animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stock-summary {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}
.store-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
}
.store-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #eee;
}
.store-info {
  display: flex;
  flex-direction: column;
}
.store-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: #333;
}
.store-dist {
  font-size: 0.8rem;
  color: #888;
}
.store-status {
  display: flex;
  align-items: center;
  gap: 8px;
}
.status-badge {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #eee;
  color: #666;
  font-weight: 600;
}
.status-badge.in-stock {
  background-color: #e6f4ea;
  color: #1e8e3e;
}
.store-link {
  font-size: 0.8rem;
  color: #4f46e5;
  text-decoration: underline;
}
.no-stock,
.stock-loading {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  padding: 10px;
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
  cursor: default;
  transform: none;
  box-shadow: none;
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

/* [추가] 이미지 슬라이드 스타일 */
.image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}
.image-wrapper:hover .nav-btn {
  opacity: 1;
}

/* Slick Slide Effect */
.carousel-container {
  width: 100%;
  height: 100%;
  overflow: hidden; /* 넘치는 부분 숨김 */
  position: relative;
}
.carousel-track {
  display: flex;
  height: 100%;
  transition: transform 0.4s ease-in-out; /* 부드러운 슬라이드 전환 */
}
.carousel-slide {
  flex-shrink: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}
.carousel-slide img.real-cover {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 꽉 채우기 (글자 잘릴 수 있음) - contain으로 바꾸면 여백 생김 */
}
.carousel-slide.placeholder-slide {
  background-color: #fdfdfd;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.3);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0; 
  transition: opacity 0.3s, background-color 0.2s;
  z-index: 10;
}
.nav-btn:hover {
  background-color: rgba(0, 0, 0, 0.6);
}
.nav-btn.prev {
  left: 10px;
}
.nav-btn.next {
  right: 10px;
}

.carousel-dots {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  transition: all 0.2s;
}
.dot.active {
  background-color: white;
  transform: scale(1.2);
}

/* [추가] 미리보기 스타일 */
.preview-section {
  margin-bottom: 60px;
}
.preview-scroll-container {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 12px;
}
.preview-item {
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #eee;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.preview-img {
  height: 300px; /* 높이 고정 */
  width: auto;
  display: block;
}
</style>
