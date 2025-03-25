import torch
import requests
import traceback
import os
import jwt
import mysql.connector
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from dotenv import load_dotenv
from passlib.context import CryptContext

#  环境 & 配置

load_dotenv()

# **JWT 配置**
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# **MySQL 配置**
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "893140",
    "database": "travel"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# **检查 PyTorch**
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())

quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
model = AutoModelForCausalLM.from_pretrained(
    "deepseek-ai/deepseek-llm-7b-chat",
    device_map="auto",
    quantization_config=quant_config
)
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-chat")

# **在线搜索 API**
SERPER_API_KEY = os.getenv("HUGGING_FACE_TOKEN")
SERPER_SEARCH_URL = "https://google.serper.dev/search"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据库操作函数

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"数据库连接失败: {e}")
        return None

def create_user(username: str, email: str, hashed_password: str):
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"数据库错误: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_user_by_username(username: str):
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# JWT 生成 & 验证

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire.timestamp()})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload["exp"] >= datetime.utcnow().timestamp() else None
    except jwt.PyJWTError:
        return None

def get_current_user(token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return token


# 用户身份验证 API

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
def register_user(user: UserRegister):
    hashed_password = pwd_context.hash(user.password)
    if not create_user(user.username, user.email, hashed_password):
        raise HTTPException(status_code=400, detail="注册失败")
    return {"message": "注册成功"}

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_username(user.username)
    if not db_user or not pwd_context.verify(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["sub"]}


#  DeepSeek 生成 在线搜索

class Query(BaseModel):
    question: str

def generate_initial_answer(question: str) -> str:
    prompt = f"问题：{question}\n回答："
    inputs = tokenizer(prompt, return_tensors="pt")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def online_search(question: str) -> List[str]:
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": question, "num": 3}

    try:
        response = requests.post(SERPER_SEARCH_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [f"[{item.get('title', '').strip()}]({item.get('link', '').strip()})" for item in data.get("organic", [])]
    except Exception as e:
        print("在线搜索失败：", str(e))
        return []

def post_process_answer(initial_answer: str, online_links: List[str]) -> str:
    cleaned_answer = initial_answer.replace("问题：", "").replace("回答：", "").strip()
    links_text = "\n".join(online_links)
    return f"{cleaned_answer}\n🔗 相关资料：\n{links_text}"

def two_stage_generation(question: str) -> str:
    initial_answer = generate_initial_answer(question)
    online_links = online_search(question)
    return post_process_answer(initial_answer, online_links)

@app.post("/ask")
async def ask_question(query: Query, request: Request):
    try:
        client_ip = request.client.host
        print(f"[请求] 来自 {client_ip} 的问题：{query.question}")

        answer = two_stage_generation(query.question)
        print(f"[结果] 生成的回答：{answer}...")
        return {"answer": answer}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}")


# FastAPI 启动

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010, reload=True)
