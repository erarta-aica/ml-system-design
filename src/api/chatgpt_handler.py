from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/analyze-food")
async def analyze_food(file: UploadFile = File(...)):
    # Читаем файл и конвертируем в base64
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this food image and provide: 1) What food items you see 2) Estimated calories for the entire portion. Return the result in JSON format with fields: foodItems (array of strings) and totalCalories (number)"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
        )
        
        if response.status_code != 200:
            return {"error": "Failed to analyze image"}
            
        result = response.json()
        try:
            # Пытаемся распарсить JSON из ответа
            content = result["choices"][0]["message"]["content"]
            return content
        except Exception as e:
            return {
                "foodItems": ["Could not parse items"],
                "totalCalories": 0,
                "rawResponse": content
            } 