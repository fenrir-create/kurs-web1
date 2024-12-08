from fastapi import FastAPI, Depends, HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud, database
from app.models import init_db
from app.database import get_db

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Создание администратора при старте приложения
@app.on_event("startup")
def startup():
    init_db()
    db = next(database.get_db())
    admin_user = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin_user:
        crud.create_user(
            db,
            schemas.UserCreate(
                username="admin",
                password="admin123",  # Пароль администратора
                description="Admin user",
            ),
        )

# Ваши маршруты остаются без изменений...
# @app.post("/users/", response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db, user)

# @app.get("/users/{user_id}", response_model=schemas.UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.put("/users/{user_id}", response_model=schemas.UserResponse)
# def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud.update_user(db, user_id, user)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @app.delete("/users/{user_id}", response_model=dict)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.delete_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}


# Страница входа (Login)
@app.get("/", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Панель управления CRUD операциями
@app.get("/dashboard", response_class=HTMLResponse)
def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Создание нового пользователя
# @app.post("/users/", response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.create_user(db, user)
#     return db_user

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Возвращаем читаемую ошибку
    return db_user


# Получение пользователя по ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Обновление данных пользователя
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




# Удаление пользователя по ID
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}