# Mistral Local Assistant

AI 챗봇 프로젝트 - Mistral-7B 모델 기반의 로컬 챗봇 시스템

## 📌 주요 기능

- 🤖 Mistral-7B 모델 기반 로컬 AI 챗봇
- 🌏 한국어 인터페이스 지원
- 💾 대화 기록 저장 및 조회
- 📝 다양한 대화 템플릿 지원

## 🛠️ 기술 스택

- **Backend**: FastAPI
- **Frontend**: Gradio
- **AI Model**: Mistral-7B

## 🚀 시작하기

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

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
