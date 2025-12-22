<template>
  <div class="books-grid">
    <BestsellerCard
      v-for="(book, index) in books"
      :key="book.isbn"
      :book="book"
      :rank="index + 1"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import aladinApi from '@/api/aladin'
import BestsellerCard from '@/components/BestsellerCard.vue'

const books = ref([])

const fetchBestsellers = async () => {
  try {
    const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY
    // IT 카테고리
    const CATEGORY_ID = '351'

    const response = await aladinApi.get('/ItemList.aspx', {
      params: {
        ttbkey: TTB_KEY,
        QueryType: 'Bestseller',
        MaxResults: 8,
        start: 1,
        SearchTarget: 'Book',
        CategoryId: CATEGORY_ID,
        output: 'js',
        Version: '20131101',
      },
    })

    books.value = response.data.item
  } catch (error) {
    console.error('데이터를 불러오지 못했습니다.', error)
  }
}
onMounted(fetchBestsellers)
</script>

<style scoped>
.bestseller-section {
  max-width: 1024px;
  margin: 40px auto;
  padding: 0 16px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.star-icon {
  margin-bottom: 2px;
}

h2 {
  font-size: 20px;
  font-weight: 800;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

@media (max-width: 768px) {
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
