from fastapi import FastAPI,HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User, Memo
from schemas import UserCreate, MemoCreate
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token}

@app.post("/memos")
def create_memo(memo: MemoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    new_memo = Memo(title=memo.title, content=memo.content, user_id=user.id)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return new_memo

@app.get("/memos")
def read_memos(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    return db.query(Memo).filter(Memo.user_id == user.id).all()

@app.get("/memos/{memo_id}")
def read_memo(memo_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user.id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memo

@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, memo: MemoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    db_memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user.id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    db_memo.title = memo.title
    db_memo.content = memo.content
    db.commit()
    db.refresh(db_memo)
    return db_memo

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user = db.query(User).filter(User.username == username).first()
    db_memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user.id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    db.delete(db_memo)
    db.commit()
    return {"message": "Memo deleted"}



