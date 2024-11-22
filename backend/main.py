from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from ctransformers import AutoModelForCausalLM
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = AutoModelForCausalLM.from_pretrained(
    "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    max_new_tokens=1024,
    context_length=2048,
)

CHAT_HISTORY_FILE = "chat_history.json"

class Query(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    prompt: str
    template: str = "default"

TEMPLATES = {
    "default": "<s>[INST] {prompt} [/INST]",
    "code": "<s>[INST] 다음 프로그래밍 작업을 수행해주세요: {prompt} [/INST]",
    "analysis": "<s>[INST] 다음 내용을 분석해주세요: {prompt} [/INST]",
    "creative": "<s>[INST] 창의적으로 다음 내용을 작성해주세요: {prompt} [/INST]"
}

@app.post("/api/generate")
async def generate_response(query: Query):
    prompt_template = TEMPLATES.get(query.template, TEMPLATES["default"])
    formatted_prompt = prompt_template.format(prompt=query.prompt)
    response = llm(formatted_prompt)
    
    save_chat_history(query.prompt, response)
    return {"response": response}

def save_chat_history(prompt, response):
    history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    history.append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    })
    
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.get("/api/history")
async def get_chat_history():
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history
        return []
    except Exception as e:
        return {"error": str(e)}