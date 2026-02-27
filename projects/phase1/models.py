from sqlalchemy import Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Todo(Base):
    """
    todosテーブルに対応するモデル

    ファームウェア視点:
    - クラス = 構造体定義
    - __tablename__ = テーブル名（メモリ領域の名前）
    - Mapped[型] = 型アノテーション付きのカラム定義
    """
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[int] = mapped_column(Integer,  ForeignKey("users.id"), nullable=False)  # 外部キー（ユーザID）

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)