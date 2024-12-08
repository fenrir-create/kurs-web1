from sqlalchemy.orm import Session
from . import models, schemas
import logging
from sqlalchemy.exc import IntegrityError

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(
#         username=user.username,
#         password=user.password,  # Сохранение пароля
#         description=user.description,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
def create_user(db: Session, user: schemas.UserCreate):
    # Проверяем, существует ли пользователь с таким именем
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise ValueError(f"User with username '{user.username}' already exists")

    # Создаем нового пользователя
    db_user = models.User(username=user.username, password=user.password, description=user.description)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()  # Откатить транзакцию при ошибке
        raise ValueError("Failed to create user: username must be unique") from e

    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
