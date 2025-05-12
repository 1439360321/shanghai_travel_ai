# 上海旅游助手 项目

## 项目简介上海旅游助手
本项目整合了 DeepSeek 模型，部署成 API 并用 Vue3 前端展示问答界面。（尝试微调和rag技术但是失败）

## 目录结构

project/ ├── backend/ # 后端代码（FastAPI 部署 DeepSeek RAG API） │ ├── app.py │ └── requirements.txt ├── frontend/ # 前端代码（基于 Vite + Vue3） │ ├── package.json │ ├── vite.config.js │ ├── public/ │ │ └── index.html │ └── src/ │ ├── main.js │ ├── App.vue │ └── components/ │ └── AskForm.vue └── README.md

## 后端部署

   ```bash
   cd backend
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## 前端部署
```bash
    cd frontend
    npm install
    npm run dev
```

