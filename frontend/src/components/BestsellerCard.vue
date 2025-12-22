<template>
  <div class="book-card" @click="onClick(book.isbn13)">
    <div class="cover-wrapper">
      <div class="rank-badge">{{ rank }}</div>
      <img :src="book.cover.replace('coversum', 'cover500')" :alt="book.title" class="book-cover" />
    </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-author">{{ book.author }}</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  book: Object,
  rank: Number,
})

const onClick = (isbn13) => {
  router.push(`/books/${isbn13}`)
}
</script>

<style scoped>
.book-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
}

.cover-wrapper {
  position: relative;
  aspect-ratio: 2 / 3;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.cover-wrapper:hover {
  transform: translateY(-5px);
}

.rank-badge {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #1a1a1a;
  color: white;
  padding: 4px 10px;
  font-weight: bold;
  font-size: 14px;
  z-index: 1;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  word-break: keep-all;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
