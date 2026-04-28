from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleable
import shutil
import os
import json
from datetime import datetime

app = FastAPI()

# Разрешаем запросы с вашего фронтенда (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload")
async def upload_registration(
    fio: str = Form(...),
    branch: str = Form(...),
    tab_number: str = Form(...),
    gender: str = Form(...),
    position: str = Form(...),
    arrival_date: str = Form(...),
    phone: str = Form(...),
    photo: UploadFile = File(...)
):
    try:
        # 1. Сохраняем фото
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(photo.filename)[1]
        photo_filename = f"{timestamp}_{fio.replace(' ', '_')}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, photo_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # 2. Формируем данные пользователя
        user_data = {
            "fio": fio,
            "branch": branch,
            "tab_number": tab_number,
            "gender": gender,
            "position": position,
            "arrival_date": arrival_date,
            "phone": phone,
            "photo_path": file_path,
            "registration_date": timestamp
        }

        # 3. Сохраняем данные в JSON-лог (или в базу данных)
        with open("registrations.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(user_data, ensure_ascii=False) + "\n")

        return {"status": "success", "message": "Данные и фото успешно сохранены!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)