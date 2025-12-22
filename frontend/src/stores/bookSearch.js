import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useBookSearchStore = defineStore('bookSearch', () => {
  const keyword = ref('')
  const lastKeyword = ref('')
  const books = ref([])
  const totalCount = ref(0)
  const currentPage = ref(1)
  const hasSearched = ref(false)
  const scrollY = ref(0)

  const resetSearch = () => {
    keyword.value = ''
    lastKeyword.value = ''
    books.value = []
    totalCount.value = 0
    currentPage.value = 1
    hasSearched.value = false
    scrollY.value = 0
  }

  const clearResults = () => {
    books.value = []
    totalCount.value = 0
    currentPage.value = 1
    hasSearched.value = false
    scrollY.value = 0
  }

  return {
    keyword,
    lastKeyword,
    books,
    totalCount,
    currentPage,
    hasSearched,
    scrollY,
    resetSearch,
    clearResults,
  }
})
