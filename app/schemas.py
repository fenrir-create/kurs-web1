from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    description: str | None = None

# class UserCreate(UserBase):
#     password: str  # Поле для пароля
    
class UserCreate(BaseModel):
    username: str
    password: str
    description: str

class UserUpdate(BaseModel):
    description: str | None = None
    password: str | None = None  # Возможность обновления пароля

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
        
