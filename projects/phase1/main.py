from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Todo, User
from schemas import UserCreate
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()


# --- Pydantic スキーマ（リクエスト/レスポンスの型定義） ---

class TodoCreate(BaseModel):
    name: str


class TodoResponse(BaseModel):
    id: int
    name: str
    done: bool

    model_config = {"from_attributes": True}  # ORMオブジェクト→Pydanticに変換許可



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# --- エンドポイント ---

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with PostgreSQL!"}


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    """
    Depends(get_db) = 依存性注入
    ファームウェアでいうと、関数呼び出し時に自動でハードウェアハンドルを渡す仕組み
    """
    username = get_current_user(token)  # トークンからユーザー名を取得
    user = db.query(User).filter(User.username == username).first()  # DBからユーザーを取得
    new_todo = Todo(name=todo.name, user_id=user.id)
    db.add(new_todo)       # INSERT準備
    db.commit()            # 実際にDBに書き込み
    db.refresh(new_todo)   # DBから最新データを取得（IDが振られる）
    return new_todo


@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    return db.query(Todo).filter(Todo.user_id == user.id).all()  # SELECT * FROM todos where user_id = user.id


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.name = todo.name
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.patch("/todos/{todo_id}/done", response_model=TodoResponse)
def toggle_done(todo_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    """完了状態をトグルするエンドポイント"""
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.done = not db_todo.done
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "deleted"}

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username,hashed_password=hash_password(user.password))
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")

    db.add(new_user)       # INSERT準備
    db.commit()            # 実際にDBに書き込み
    db.refresh(new_user)   # DBから最新データを取得（IDが振られる）
    return new_user
    
@app.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"access_token": create_access_token(data={"sub": user.username})}