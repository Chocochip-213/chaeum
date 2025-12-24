import asyncio
import httpx
import os
from django.db import connection
from apps.analysis.models import AnalysisResult
from apps.books.models import TOCChunk

# 환경변수에서 URL 로드
INFERENCE_URL = os.getenv("INFERENCE_API_URL", "http://localhost:8000/embed")


class RAGService:
    @staticmethod
    async def get_embeddings(texts: list[str]):
        """Inference Service로 비동기 요청을 보내 임베딩을 받아옵니다."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            tasks = [
                client.post(INFERENCE_URL, json={"text": text})
                for text in texts
            ]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            vectors = []
            for resp in responses:
                if isinstance(resp, httpx.Response) and resp.status_code == 200:
                    vectors.append(resp.json()['vector'])
                else:
                    vectors.append(None)
            return vectors

    @staticmethod
    def search_similar_chapters(vector, top_k=3):
        """pgvector를 사용하여 유사한 챕터를 검색하고 중복을 제거합니다."""
        if not vector:
            return []

        from pgvector.django import CosineDistance
        
        # 1. 중복 제거를 위해 더 많은 후보군 검색 (3배수)
        candidates = list(TOCChunk.objects.order_by(
            CosineDistance('embedding', vector)
        )[:top_k * 3])

        # 2. 중복 제거 (ISBN + Chapter Title 기준)
        unique_results = []
        seen = set()

        for doc in candidates:
            # 키: (책 ISBN, 챕터 제목) -> 같은 책의 같은 챕터면 중복으로 간주
            key = (doc.book_id, doc.chapter_title)
            
            if key not in seen:
                seen.add(key)
                unique_results.append(doc)
                
            if len(unique_results) >= top_k:
                break
        
        return unique_results

    @classmethod
    async def recommend_chapters(cls, analysis_result_id: int):
        result = await AnalysisResult.objects.aget(id=analysis_result_id)
        
        if result.rag_recommendations:
            return result.rag_recommendations

        queries = result.gap_missing_chapters
        if not queries:
            return []
            
        vectors = await cls.get_embeddings(queries)

        recommended_data = []
        for i, (query_text, vector) in enumerate(zip(queries, vectors)):
            if vector:
                # search_similar_chapters는 DB 접근하므로 sync_to_async 필요
                docs = await asyncio.to_thread(cls.search_similar_chapters, vector)
                
                recommended_data.append({
                    "query": query_text,
                    "recommendations": [
                        {
                            "isbn": doc.book_id,       # ISBN
                            "chapter": doc.chapter_title, # 목차 제목
                            # "text": doc.composite_text  # [제외] 긴 텍스트는 응답 크기 최적화를 위해 제거
                        } for doc in docs
                    ]
                })

        # 4. 결과 DB 저장
        # 비동기 환경에서 저장을 위해 필드 할당 후 asave 호출
        result.rag_recommendations = recommended_data
        await result.asave()

        return recommended_data