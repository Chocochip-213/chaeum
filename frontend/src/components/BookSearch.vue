<template>
  <div class="search-page-container" :class="{ invisible: isRestoring }">
    <div class="header-section" id="top-anchor">
      <h1 class="main-title">
        {{ mode === 'select' ? '글을 작성할 책을 선택해주세요' : '도서 검색' }}
      </h1>
      <p class="sub-title">
        {{
          mode === 'select'
            ? '어떤 책에 대한 이야기를 나누고 싶으신가요?'
            : '알라딘 DB를 통해 원하는 책을 찾아보세요.'
        }}
      </p>
    </div>

    <div class="search-bar-wrapper">
      <div class="search-input-box">
        <Search :size="20" class="search-icon" />
        <input
          v-model="store.keyword"
          type="text"
          class="search-input"
          :placeholder="'책 제목, 저자명, 출판사로 검색...'"
          @keyup.enter="handleNewSearch"
        />
        <button class="search-btn" @click="handleNewSearch">검색</button>
      </div>
    </div>

    <div class="results-container">
      <div v-if="!store.hasSearched" class="status-msg guide">
        {{
          mode === 'select'
            ? '리뷰를 남길 책을 검색해보세요.'
            : '추천 검색어: React, Python, 베스트셀러'
        }}
      </div>

      <div v-else-if="store.books.length > 0" class="book-list-wrapper">
        <p class="result-count">
          '<strong>{{ store.lastKeyword }}</strong
          >' 검색 결과: 총 {{ Number(store.totalCount).toLocaleString() }}권
        </p>

        <div class="book-grid">
          <div
            v-for="book in store.books"
            :key="book.isbn13"
            class="book-card"
            @click="handleBookClick(book)"
          >
            <div class="card-image">
              <img :src="book.cover" :alt="book.title" />
            </div>

            <div class="card-content">
              <div class="badge-row">
                <span class="category-badge">{{ book.categoryName }}</span>
              </div>
              <h3 class="book-title" :title="book.title">{{ book.title }}</h3>
              <p class="book-meta">{{ book.author }}</p>
              <p class="book-publisher">{{ book.publisher }} | {{ book.pubDate }}</p>

              <div class="tag-row">
                <span class="tag">#개발</span>
                <span class="tag">#{{ book.categoryName }}</span>
              </div>

              <div v-if="mode === 'select'" class="select-btn-area">
                <button class="select-btn">선택하기</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="store.books.length < store.totalCount" class="more-btn-wrapper">
          <button class="more-btn" @click="handleLoadMore" :disabled="loading">
            {{ loading ? '불러오는 중...' : '결과 더보기 (+10)' }}
          </button>
        </div>
      </div>

      <div v-else-if="store.hasSearched && !loading" class="status-msg">검색 결과가 없습니다.</div>

      <div v-if="loading && store.books.length === 0" class="status-msg">검색 중입니다...</div>
    </div>

    <Transition name="fade">
      <button v-show="showScrollBtn" class="scroll-top-btn" @click="scrollToTop">
        <ArrowUp :size="24" />
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { onBeforeRouteLeave, useRouter } from 'vue-router'
import aladinApi from '@/api/aladin'
import { Search, ArrowUp } from 'lucide-vue-next'
import { useBookSearchStore } from '@/stores/bookSearch'

// --- Props 정의 ---
// mode: 'search'(일반 검색, 상세페이지 이동) / 'select'(글쓰기용 선택, 작성페이지 이동)
const props = defineProps({
  mode: {
    type: String,
    default: 'search',
  },
})

const router = useRouter()
const store = useBookSearchStore()

const loading = ref(false) // API 요청 중인지 여부
const showScrollBtn = ref(false) // '맨 위로' 버튼 표시 여부
const isRestoring = ref(false) // 스크롤 복구 중인지 여부 (화면 깜빡임 방지용)

// --- 1. 검색 로직 ---

/**
 * 새로운 키워드로 검색을 시작합니다.
 * 기존 결과 리스트를 초기화하고 첫 페이지부터 다시 조회합니다.
 */
const handleNewSearch = () => {
  if (!store.keyword.trim()) {
    alert('검색어를 입력해주세요.')
    return
  }

  // Store의 이전 결과 초기화 (검색어는 유지)
  store.clearResults()
  store.lastKeyword = store.keyword
  store.hasSearched = true

  fetchBooks()
}

/**
 * '더보기' 버튼 클릭 시 실행됩니다.
 * 페이지 번호를 1 증가시키고 데이터를 추가로 불러옵니다.
 */
const handleLoadMore = () => {
  store.currentPage++
  fetchBooks()
}

/**
 * 알라딘 API를 호출하여 도서 데이터를 가져옵니다.
 */
const fetchBooks = async () => {
  loading.value = true
  try {
    const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY

    const response = await aladinApi.get('/ItemSearch.aspx', {
      params: {
        ttbkey: TTB_KEY,
        Query: store.lastKeyword, // Store에 저장된 검색어 사용
        QueryType: 'Keyword',
        MaxResults: 10,
        start: store.currentPage, // Store에 저장된 페이지 번호 사용
        SearchTarget: 'Book',
        output: 'js',
        Version: '20131101',
        Cover: 'Big',
      },
    })

    if (response.data.item) {
      // API 응답 데이터를 앱에서 쓰기 편한 형태로 가공
      const newBooks = response.data.item.map((item) => ({
        title: item.title,
        author: item.author,
        publisher: item.publisher,
        pubDate: item.pubDate,
        description: item.description || '상세 설명이 없습니다.',
        cover: item.cover,
        isbn13: item.isbn13,
        // 카테고리 문자열 파싱 (예: 국내도서>IT>Web -> IT)
        categoryName: item.categoryName.split('>')[1] || 'IT',
      }))

      // 기존 리스트 뒤에 새로운 데이터를 붙입니다 (무한 스크롤 방식)
      store.books = [...store.books, ...newBooks]
      store.totalCount = response.data.totalResults
    }
  } catch (error) {
    console.error('검색 실패:', error)
  } finally {
    loading.value = false
  }
}

// --- 2. 네비게이션 및 스크롤 저장 로직 ---

/**
 * 책 카드를 클릭했을 때 실행됩니다.
 * 이동하기 직전에 현재 스크롤 위치를 Store에 저장합니다.
 */
const handleBookClick = (book) => {
  // !! 현재 스크롤 위치 저장 !!
  store.scrollY = window.scrollY

  if (props.mode === 'select') {
    // 글 작성 모드 -> 글쓰기 페이지로 이동
    router.push({
      name: 'community-write',
      query: {
        isbn: book.isbn13,
        title: book.title,
        cover: book.cover,
      },
    })
  } else {
    // 일반 검색 모드 -> 도서 상세 페이지로 이동
    router.push({
      name: 'book-detail',
      params: { isbn13: book.isbn13 },
    })
  }
}

// 스크롤 이벤트 핸들러 (버튼 표시 여부 결정)
const handleScroll = () => {
  showScrollBtn.value = window.scrollY > 300
}

// 맨 위로 부드럽게 이동
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// --- 3. 라이프사이클 훅 (스크롤 복구 및 초기화) ---

onMounted(() => {
  // 브라우저의 기본 스크롤 복원 기능 끄기 (수동 제어 위해)
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual'
  }

  window.addEventListener('scroll', handleScroll)

  // 이전에 검색한 결과가 있고, 스크롤 위치가 저장되어 있을 경우 (뒤로가기로 왔을 때)
  if (store.books.length > 0 && store.scrollY > 0) {
    // 1. 화면을 잠시 투명하게 만듦 (깜빡임 방지)
    isRestoring.value = true

    nextTick(() => {
      // 2. 약간의 지연 후 스크롤을 저장된 위치로 강제 이동
      setTimeout(() => {
        window.scrollTo(0, store.scrollY)

        // 3. 스크롤 이동이 끝난 직후 화면을 다시 보이게 함
        requestAnimationFrame(() => {
          isRestoring.value = false
        })
      }, 100) // 0.1초 딜레이
    })
  } else {
    // 복구할 게 없으면 바로 화면 표시
    isRestoring.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// --- 4. 라우터 가드 (검색 기록 초기화 로직) ---

/**
 * 컴포넌트를 떠나기(이동하기) 직전에 실행됩니다.
 * '도서 관련 페이지(/books...)'가 아닌 다른 곳으로 갈 때만 검색어를 초기화합니다.
 */
onBeforeRouteLeave((to, from, next) => {
  // 이동하려는 경로에 '/books'가 포함되지 않았을 경우
  if (!to.path.includes('/books')) {
    store.keyword = '' // 검색어 비우기
  }
  next() // 이동 허용
})
</script>

<style scoped>
/* 스크롤 복구 시 화면이 덜컥거리는 것을 숨기기 위한 클래스 */
.invisible {
  opacity: 0;
}

.search-page-container {
  width: 100%;
  max-width: 1024px;
  margin: 0 auto;
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  min-height: 80vh;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}
.main-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #111;
}
.sub-title {
  color: #666;
  font-size: 1rem;
}
.search-bar-wrapper {
  width: 100%;
  max-width: 680px;
  margin-bottom: 40px;
}
.search-input-box {
  display: flex;
  align-items: center;
  width: 100%;
  height: 64px;
  border: 2px solid #111;
  border-radius: 50px;
  padding: 0 8px 0 24px;
  background-color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}
.search-input-box:focus-within {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}
.search-icon {
  color: #999;
  margin-right: 12px;
}
.search-input {
  flex-grow: 1;
  border: none;
  font-size: 1.1rem;
  outline: none;
  background: transparent;
}
.search-btn {
  background-color: #111;
  color: white;
  border: none;
  height: 48px;
  padding: 0 32px;
  border-radius: 40px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}
.search-btn:hover {
  background-color: #333;
}
.results-container {
  width: 100%;
}
.status-msg {
  text-align: center;
  color: #888;
  padding: 40px 0;
  font-size: 1.1rem;
}
.guide {
  font-size: 0.95rem;
  color: #aaa;
}
.result-count {
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 20px;
  font-weight: 600;
  padding-left: 4px;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
@media (max-width: 768px) {
  .book-grid {
    grid-template-columns: 1fr;
  }
}
.book-card {
  display: flex;
  gap: 20px;
  padding: 24px;
  border: 1px solid #eee;
  border-radius: 16px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  height: 100%;
  box-sizing: border-box;
}
.book-card:hover {
  border-color: #ccc;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}
.card-image {
  flex-shrink: 0;
  width: 120px;
  height: 174px;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #f0f0f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  justify-content: flex-start;
}
.badge-row {
  margin-bottom: 8px;
}
.category-badge {
  background-color: #f3f0e9;
  color: #8d6e63;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
}
.book-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 6px 0;
  color: #111;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.book-meta {
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 4px;
  font-weight: 500;
}
.book-publisher {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 12px;
}
.tag-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: auto;
}
.tag {
  font-size: 0.75rem;
  color: #4f46e5;
  background-color: #eef2ff;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.select-btn-area {
  position: absolute;
  bottom: 24px;
  right: 24px;
}
.select-btn {
  background-color: #f3f4f6;
  color: #111;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}
.book-card:hover .select-btn {
  background-color: #111;
  color: white;
  border-color: #111;
}
.more-btn-wrapper {
  margin-top: 50px;
  text-align: center;
}
.more-btn {
  background-color: white;
  border: 1px solid #ddd;
  color: #555;
  padding: 14px 48px;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.more-btn:hover {
  background-color: #f9f9f9;
  border-color: #bbb;
  color: #111;
  transform: translateY(-2px);
}
.more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.scroll-top-btn {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #111;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 999;
}
.scroll-top-btn:hover {
  background-color: #333;
  transform: scale(1.1);
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
