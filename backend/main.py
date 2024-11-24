# 필요한 라이브러리 임포트
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # CORS 설정을 위한 미들웨어
from pydantic import BaseModel, ConfigDict  # 데이터 검증을 위한 모델
from ctransformers import AutoModelForCausalLM  # LLM 모델 로드
import json
import os
from datetime import datetime
from fastapi.responses import StreamingResponse

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# CORS 미들웨어 설정
# 프론트엔드에서 API 접근을 허용하기 위한 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mistral AI 모델 로드
llm = AutoModelForCausalLM.from_pretrained(
    "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    max_new_tokens=1024,    # 생성할 최대 토큰 수
    context_length=2048,    # 컨텍스트 윈도우 크기
)

# 채팅 기록을 저장할 파일 경로
CHAT_HISTORY_FILE = "chat_history.json"

# API 요청을 위한 데이터 모델
class Query(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    prompt: str          # 사용자 입력 텍스트
    template: str = "default"  # 사용할 프롬프트 템플릿

# 프롬프트 템플릿 정의
TEMPLATES = {
    "default": "<s>[INST] {prompt} [/INST]",
    "code": "<s>[INST] Please perform the following programming tasks: {prompt} [/INST]",
    "analysis": "<s>[INST] Please analyze the following: {prompt} [/INST]",
    "creative": "<s>[INST] Please write the following creatively: {prompt} [/INST]"
}

# AI 응답 생성 API 엔드포인트
@app.post("/api/generate")
async def generate_response(query: Query):
    """
    사용자 입력을 받아 AI 응답을 생성하는 엔드포인트
    
    Args:
        query (Query): 사용자 입력과 템플릿 정보를 담은 객체
    
    Returns:
        dict: AI 모델의 응답을 담은 딕셔너리
    """
    prompt_template = TEMPLATES.get(query.template, TEMPLATES["default"])
    formatted_prompt = prompt_template.format(prompt=query.prompt)
    response = llm(formatted_prompt)
    
    save_chat_history(query.prompt, response)
    return {"response": response}

# 채팅 기록 저장 함수
def save_chat_history(prompt, response):
    """
    대화 내용을 JSON 파일에 저장하는 함수
    
    Args:
        prompt (str): 사용자 입력
        response (str): AI 응답
    """
    history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    # 새로운 대화 내용 추가
    history.append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    })
    
    # JSON 파일로 저장
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# 채팅 기록 조회 API 엔드포인트
@app.get("/api/history")
async def get_chat_history():
    """
    저장된 대화 기록을 조회하는 엔드포인트
    
    Returns:
        list: 대화 기록 리스트 또는 에러 메시지
    """
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history
        return []
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/generate/stream")
async def generate_stream_response(query: Query):
    prompt_template = TEMPLATES.get(query.template, TEMPLATES["default"])
    formatted_prompt = prompt_template.format(prompt=query.prompt)
    
    async def generate():
        for token in llm(formatted_prompt, stream=True):
            yield f"data: {token}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )