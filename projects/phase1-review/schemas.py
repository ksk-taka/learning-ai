
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str    # ← 生パスワード（APIで受け取る用。DBには保存しない）

class MemoCreate(BaseModel):
    title: str
    content: str
