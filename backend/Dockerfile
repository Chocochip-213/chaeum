FROM python:3.11-slim

# 파이썬 환경 설정 (버퍼링 끔, pyc 파일 생성 막음)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (PostgreSQL 연결 등 필수 라이브러리)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 패키지 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# 기본 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]