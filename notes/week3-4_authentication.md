# Week 3-4: ユーザー認証（bcrypt + JWT + OAuth2）

## 認証フロー全体像
```
1. POST /register → パスワードをハッシュ化してDBに保存
2. POST /login   → パスワード検証 → JWTトークン発行
3. 以降のリクエスト → Authorization: Bearer <token> ヘッダで認証
4. サーバー側でトークンをデコードしてユーザーを特定
```

## パスワードハッシュ化（bcrypt）
- パスワードを一方向変換して保存。元に戻せない
- **組込みでいうと**: OTP(One-Time Programmable)メモリ。書き込んだら読み出せない

### salt（ソルト）
- 同じパスワードでも毎回違うハッシュが生成される仕組み
- **なぜ必要？**: saltがないと同じパスワードは同じハッシュ → レインボーテーブル（よく使うパスワードのハッシュ一覧）で逆引きされる
- **組込みでいうと**: 暗号通信のIV（初期化ベクトル）と同じ発想

### 実装
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

## JWT（JSON Web Token）
- ログイン成功後に発行される「入館証」
- **組込みでいうと**: BLEのペアリング後の暗号化キー交換に近い

### トークンの構造
```
eyJhbGci...  ← ヘッダ（アルゴリズム情報）
.
eyJzdWIi...  ← ペイロード（sub: ユーザー名, exp: 有効期限）
.
TwpeUHNY...  ← 署名（改竄されてないことの証明）
```

### 実装
```python
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token")
        return username
    except JWTError:
        raise ValueError("Invalid token")
```

## OAuth2PasswordBearer
```python
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
```
- FastAPIが `Authorization: Bearer <token>` ヘッダからトークンを自動抽出
- `Depends(oauth2_scheme)` でエンドポイントに認証を追加
- トークンなしのリクエスト → 自動で `{"detail":"Not authenticated"}` を返す

## エンドポイントへの認証追加パターン
```python
@app.get("/todos")
def read_todos(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)                                    # トークン→ユーザー名
    user = db.query(User).filter(User.username == username).first()      # ユーザー名→DBユーザー
    return db.query(Todo).filter(Todo.user_id == user.id).all()          # 自分のTODOだけ取得
```

## curlでのテスト方法
```bash
# 1. ユーザー登録
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"mypassword"}'

# 2. ログイン（トークン取得）
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"mypassword"}'

# 3. 認証付きリクエスト（トークンをAuthorizationヘッダに入れる）
curl -X GET http://localhost:8000/todos \
  -H "Authorization: Bearer <取得したトークン>"
```

## つまずきポイント
- `passlib` と `bcrypt` 4.1以降はバージョン非互換 → `pip install bcrypt==4.0.1` で解決
- `datetime.utcnow()` は非推奨 → `datetime.now(timezone.utc)` を使う
- curlの `TOKEN` は Authorization ヘッダ内の値を置き換える（nameフィールドではない）
- 変数名の衝突に注意: リクエストの `user` と DBの `db_user` を区別する
