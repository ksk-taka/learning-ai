import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# .envファイルから環境変数を読み込み
load_dotenv()

# 環境変数から接続URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

# エンジン = DBへの接続を管理（ファームウェアでいうドライバ初期化）
engine = create_engine(DATABASE_URL)

# セッション = DBとの通信単位（UARTのトランザクションに近い）
SessionLocal = sessionmaker(bind=engine)


# モデルの基底クラス（全テーブルの親クラス）
class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPIの依存性注入で使うDB接続取得関数"""
    db = SessionLocal()
    try:
        yield db  # リクエスト中はDBセッションを提供
    finally:
        db.close()  # リクエスト終了時に必ずクローズ
