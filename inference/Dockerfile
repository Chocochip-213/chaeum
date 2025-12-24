FROM python:3.11-slim
WORKDIR /app
# 필수 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*
# Pytorch & Sentence-Transformers 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# FastAPI 서버 실행 (Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]