import { ref } from 'vue'
import api from '@/api'
import aladinApi from '@/api/aladin'

export function usePosts() {
  const posts = ref([])
  const bookTitles = ref({}) // { "ISBN": "제목" }
  const isLoading = ref(false)

  // 1. 알라딘 책 제목 가져오기
  const fetchBookTitles = async (isbnList) => {
    const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY

    // 유효한 ISBN 필터링
    const validIsbns = isbnList.filter((isbn) => isbn && String(isbn).trim() !== '')

    for (const isbn of validIsbns) {
      if (bookTitles.value[isbn]) continue // 이미 있을 경우 패스

      try {
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
          bookTitles.value[isbn] = response.data.item[0].title
        } else {
          bookTitles.value[isbn] = '정보 없음'
        }
      } catch (err) {
        console.error(`책 제목 조회 실패 (${isbn})`, err)
        bookTitles.value[isbn] = '조회 실패'
      }
    }
  }

  // 2. 게시글 목록 조회
  const fetchPosts = async (params = {}) => {
    isLoading.value = true
    posts.value = []

    try {
      const response = await api.get('/community/posts/', { params })
      posts.value = response.data

      // 게시글에 있는 ISBN들을 모아서 책 제목 조회 실행
      const uniqueIsbns = [
        ...new Set(
          posts.value
            .map((p) => p.book_isbn)
            .filter((isbn) => isbn != null && String(isbn).trim() !== ''),
        ),
      ]

      if (uniqueIsbns.length > 0) {
        fetchBookTitles(uniqueIsbns)
      }
    } catch (err) {
      console.error('게시글 로드 실패:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    posts,
    bookTitles,
    isLoading,
    fetchPosts,
  }
}
