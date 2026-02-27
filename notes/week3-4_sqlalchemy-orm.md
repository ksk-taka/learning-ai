# Week 3-4: SQLAlchemy（ORM）

## ORMとは
- ORM = Object Relational Mapping
- SQLを直接書かずに、Pythonオブジェクトでデータベース操作ができる
- **組込みでいうと**: 生SQL = レジスタ直叩き、ORM = HAL経由アクセス

## ORM → SQL 対応表
| ORM | SQL |
|-----|-----|
| `db.query(Todo).all()` | `SELECT * FROM todos` |
| `db.query(Todo).filter(Todo.id == 5).first()` | `SELECT * FROM todos WHERE id = 5 LIMIT 1` |
| `db.add(obj)` + `db.commit()` | `INSERT INTO todos ...` |
| `obj.name = "new"` + `db.commit()` | `UPDATE todos SET name = 'new' WHERE ...` |
| `db.delete(obj)` + `db.commit()` | `DELETE FROM todos WHERE ...` |

## `.first()` vs `.all()`
- `.all()` → リスト（複数件）を返す
- `.first()` → 1件 or None を返す（`LIMIT 1`）
- 見つからなければ `None` → だから `if not todo:` で404チェックが必要

## モデル定義
```python
class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
```
- クラス = C言語の構造体定義に相当
- `__tablename__` = テーブル名（メモリ領域の名前）
- `Mapped[型]` = 型アノテーション付きのカラム定義

## ForeignKey（外部キー）
```python
user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
```
- テーブル間の関連付け（「このTODOはどのユーザーのもの？」）
- **組込みでいうと**: ポインタが特定の構造体を指すことを型で保証するようなもの

## DB接続の仕組み（database.py）
```python
engine = create_engine(DATABASE_URL)     # DB接続エンジン
SessionLocal = sessionmaker(bind=engine) # セッション生成器
Base = declarative_base()                # モデルの基底クラス

def get_db():
    db = SessionLocal()
    try:
        yield db     # dbをエンドポイントに渡す
    finally:
        db.close()   # 最後に必ず閉じる
```
