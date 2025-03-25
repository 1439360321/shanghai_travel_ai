# DeepSeek RAG 项目

## 项目简介
本项目整合了微调后的 DeepSeek 模型与 RAG（检索增强生成）技术，通过 FAISS 向量检索和 LangChain 构建 RetrievalQA 链，部署成 API 并用 Vue3 前端展示问答界面。

## 目录结构

project/ ├── backend/ # 后端代码（FastAPI 部署 DeepSeek RAG API） │ ├── app.py │ └── requirements.txt ├── frontend/ # 前端代码（基于 Vite + Vue3） │ ├── package.json │ ├── vite.config.js │ ├── public/ │ │ └── index.html │ └── src/ │ ├── main.js │ ├── App.vue │ └── components/ │ └── AskForm.vue └── README.md

## 后端部署

   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## 前端部署
```bash
    cd frontend
    npm install
    npm run dev
```

