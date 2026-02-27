from sqlalchemy import Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password:Mapped[str] = mapped_column(String(255), nullable=False)


class Memo(Base):
    __tablename__ = "memos"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)