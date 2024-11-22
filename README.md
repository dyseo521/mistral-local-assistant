# Mistral Local Assistant

AI 챗봇 프로젝트 - Mistral-7B 모델 기반의 로컬 챗봇 시스템

## 📌 주요 기능

- 🤖 Mistral-7B 모델 기반 로컬 AI 챗봇
- 🌏 한국어 인터페이스 지원
- 💾 대화 기록 저장 및 조회
- 📝 다양한 대화 템플릿 지원

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: Python 웹 프레임워크
- **CTransformers**: LLM 모델 추론 라이브러리
- **Pydantic**: 데이터 검증 및 설정 관리
- **Mistral-7B**: LLM 모델

### 프론트엔드
- **Gradio**: ML 모델을 위한 웹 인터페이스 프레임워크
- **Requests**: HTTP 통신 라이브러리

## 💻 주요 기능 설명

### 1. AI 응답 생성
- Mistral-7B 모델을 사용한 텍스트 생성
- 4가지 프롬프트 템플릿 지원:
  - Default: 일반적인 대화
  - Code: 프로그래밍 관련 응답
  - Analysis: 분석 중심의 응답
  - Creative: 창의적인 응답

### 2. 대화 기록 관리
- JSON 형식으로 대화 내용 저장
- 시간, 질문, 답변 기록
- 대화 기록 조회 및 새로고침 기능

### 3. 사용자 인터페이스
- 직관적인 웹 인터페이스
- 대화하기/대화 기록 탭 구조
- 복사 버튼 등 편의 기능 제공

## 🚀 시작하기

## 📝 참고사항
- 영어 입력 권장 (더 나은 응답 품질)
- 로컬 실행 환경에서 테스트

### 사전 요구사항

- Python 3.8+
- pip package manager

### 설치 방법

1. **백엔드 설치**
   ```bash
   cd backend
   pip install -r requirements_be.txt
   ```

2. **프론트엔드 설치**
   ```bash
   cd frontend
   pip install -r requirements_fe.txt
   ```

### 모델 설치

1. [TheBloke의 Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)에서 모델 다운로드
2. 다운로드한 `mistral-7b-instruct-v0.1.Q4_K_M.gguf` 파일을 `models/` 폴더에 위치

> ⚠️ **주의**: 모델 파일이 없으면 프로그램이 실행되지 않습니다.

### 실행 방법

1. **백엔드 실행**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **프론트엔드 실행**
   ```bash
   cd frontend
   python app.py
   ```

## 🔎 오픈소스 출처

이 프로젝트는 다음의 오픈소스 프로젝트들을 기반으로 제작되었습니다:

### AI 모델
- **Mistral-7B**: [mistralai/Mistral-7B-Instruct-v0.1](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1)
  - 라이선스: Apache 2.0
  - 제작: Mistral AI
  - GGUF 변환: [TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

### 백엔드
- **FastAPI**: [tiangolo/fastapi](https://github.com/tiangolo/fastapi)
  - 라이선스: MIT
  - 버전: 0.104.1
- **CTransformers**: [marella/ctransformers](https://github.com/marella/ctransformers)
  - 라이선스: MIT
  - 버전: 0.2.27
- **Pydantic**: [pydantic/pydantic](https://github.com/pydantic/pydantic)
  - 라이선스: MIT
  - 버전: >=2.4.2

### 프론트엔드
- **Gradio**: [gradio-app/gradio](https://github.com/gradio-app/gradio)
  - 라이선스: Apache 2.0
  - 버전: 4.12.0
- **Requests**: [psf/requests](https://github.com/psf/requests)
  - 라이선스: Apache 2.0
  - 버전: 2.31.0

### 개발 도구
- **Uvicorn**: [encode/uvicorn](https://github.com/encode/uvicorn)
  - 라이선스: BSD 3-Clause
  - 버전: 0.24.0

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
