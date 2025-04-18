import os
import torch
import requests
import traceback
import logging

from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# --- 配置 ---
SERPER_API_KEY = os.getenv("HUGGING_FACE_TOKEN")
SERPER_SEARCH_URL = "https://google.serper.dev/search"

# --- 模型加载 ---
quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-chat")
model = AutoModelForCausalLM.from_pretrained(
    "deepseek-ai/deepseek-llm-7b-chat",
    device_map="auto",
    quantization_config=quant_config
)

# --- FastAPI 实例 ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 上线时建议修改为指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 请求参数定义 ---
class Query(BaseModel):
    question: str

# --- 问答逻辑 ---
def generate_initial_answer(question: str) -> str:
    prompt = f"问题：{question}\n回答："
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to("cuda" if torch.cuda.is_available() else "cpu")
    outputs = model.generate(input_ids=input_ids, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def online_search(question: str) -> List[str]:
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": question, "num": 3}
    try:
        response = requests.post(SERPER_SEARCH_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return [f"[{item['title']}]({item['link']})" for item in data.get("organic", [])]
    except Exception as e:
        logging.error(f"搜索失败: {e}")
        return []

def two_stage_generation(question: str) -> dict:
    answer = generate_initial_answer(question)
    links = online_search(question)
    return {
        "answer": answer.replace("问题：", "").replace("回答：", "").strip(),
        "recommendations": links
    }

# --- 路由定义 ---
@app.post("/ask")
def ask(query: Query, request: Request):
    try:
        result = two_stage_generation(query.question)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- 入口 ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
