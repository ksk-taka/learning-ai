from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Todo

app = FastAPI()


# --- Pydantic スキーマ（リクエスト/レスポンスの型定義） ---

class TodoCreate(BaseModel):
    name: str


class TodoResponse(BaseModel):
    id: int
    name: str
    done: bool

    model_config = {"from_attributes": True}  # ORMオブジェクト→Pydanticに変換許可


# --- エンドポイント ---

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with PostgreSQL!"}


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Depends(get_db) = 依存性注入
    ファームウェアでいうと、関数呼び出し時に自動でハードウェアハンドルを渡す仕組み
    """
    new_todo = Todo(name=todo.name)
    db.add(new_todo)       # INSERT準備
    db.commit()            # 実際にDBに書き込み
    db.refresh(new_todo)   # DBから最新データを取得（IDが振られる）
    return new_todo


@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()  # SELECT * FROM todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.name = todo.name
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.patch("/todos/{todo_id}/done", response_model=TodoResponse)
def toggle_done(todo_id: int, db: Session = Depends(get_db)):
    """完了状態をトグルするエンドポイント"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.done = not db_todo.done
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "deleted"}
