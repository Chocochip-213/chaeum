# 🚀 채움 - 나를 채우는 AI 커리어 코칭

> **"당신의 이력서와 채용공고 사이의 '빈틈(Gap)'을 찾아, 딱 맞는 전공 서적을 추천해 드립니다."**

<br>

## 1. 프로젝트 소개 (Project Overview)

**채움**은 취업 준비생들이 직면하는 "내가 왜 떨어졌는지, 무엇이 부족한지 모르는" 문제를 해결하기 위해 개발된 **AI 기반 직무 역량 분석 및 도서 추천 서비스**입니다.

사용자는 채용공고(JD) URL과 이력서(PDF)만 입력하면, AI가 두 문서를 비교 분석하여 **부족한 기술 역량을 시각화**하고, 이를 보완할 수 있는 **구체적인 전공 서적의 챕터**를 추천받을 수 있습니다.

### 📅 진행 기간

- 2025.12.19 ~ 2025.12.23.

### 🎯 주요 타겟 및 기대 효과

- **타겟:** 자신의 기술적 부족함을 객관적으로 파악하고 싶은 신입/주니어 개발자
- **효과:** 막연한 취업 준비에서 벗어나, **"지금 당장 읽어야 할 책"**이라는 구체적인 행동 지침(Action Plan) 획득

<br>

## 2. 주요 기능 (Key Features)

### 1) 📄 PDF 이력서 분석 (Resume Parsing)

- 자유 양식의 PDF 이력서에서 **기술 스택(Skills)**과 **프로젝트 경험**을 구조화된 데이터로 정밀 추출합니다.

### 2) 📊 직무 적합도 분석 (Gap Analysis)

- 사용자가 입력한 채용공고(JD)와 이력서를 LLM이 비교 분석합니다.
- **적합도 점수(0~100)**와 함께, 합격을 위해 보완해야 할 **Missing Skills**를 도출합니다.

### 3) 📚 RAG 기반 도서 추천 (RAG Book Recommendation)

- "Spring Security 인증 부분이 부족하니, **'스프링 부트 완벽 가이드'의 15장: 보안 설정**을 추천합니다.
- 33만 개의 IT 도서 목차 데이터를 벡터화하여 검색합니다.

<br>

## 3. 기술 스택 (Tech Stack)

### Frontend

<img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white"> <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=Vite&logoColor=white"> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=black">

### Backend

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white"> <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white">

### Database

<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white"> <img src="https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=PostgreSQL&logoColor=white">

### AI / Infra

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"> <img src="https://img.shields.io/badge/Qwen_2.5-000000?style=for-the-badge&logo=HuggingFace&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=AmazonAWS&logoColor=white">

<br>

## 4. 시스템 아키텍처 (System Architecture)

**Hybrid Cloud Architecture** (AWS + On-Premise GPU)

```mermaid
graph TD
    User([Web Browser]) -->|HTTPS| AWS[AWS EC2 (Web Server)]

    subgraph "AWS Cloud (t2.micro)"
        Nginx[Nginx] --> Django[Django API]
        Django --> DB[(PostgreSQL)]
        Django --> Redis[Redis Queue]
    end

    subgraph "Local GPU Server"
        Ngrok[Ngrok Tunnel]
        Inference[FastAPI LLM Server]
    end

    Redis --> Worker[Celery Worker]
    Worker -->|Secure Tunnel| Ngrok
    Ngrok --> Inference
```

### 📂 디렉토리 구조

```bash
├── backend      # Django API Server & Celery Worker
├── frontend     # Vue.js Client Application
└── inference    # FastAPI LLM Serving (Local GPU)
```

<br>

## 5. 시작 가이드 (Getting Started)

### Prerequisites

- Docker & Docker Compose
- Ngrok (for Local GPU connection)
- Node.js 20+

### Installation & Run

**1. Clone the repository**

```bash
git clone https://lab.ssafy.com/jumee.frontdev/final-pjt.git
cd final-pjt
```

**2. Setup Environment Variables**

- `backend/.env` 및 `frontend/.env` 설정 (API Key 등)

**3. Run with Docker Compose**

```bash
docker-compose up -d --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

<br>

## 6. 트러블 슈팅 (Troubleshooting)

### 🔥 하이브리드 클라우드 연결 (AWS <-> Local GPU)

- **문제:** AWS EC2(외부)에서 로컬 GPU 서버(내부망)로의 직접 통신 불가
- **해결:** **Ngrok 터널링**을 도입하여 로컬 FastAPI 포트를 공인 URL로 노출, Celery 워커가 이를 호출하도록 구성.

<br>

## 7. 팀원 소개 (Team)

| 팀장 (Backend & AI) | 팀원 (Backend & Frontend) |
| :-----------------: | :-----------------------: |
|     **김민우**      |        **서주미**         |
|  Django, RAG, LLM   |   Django, Vue.js, UI/UX   |

---
