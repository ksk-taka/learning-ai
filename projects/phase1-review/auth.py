from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-here"  # 本番では環境変数にする
ALGORITHM = "HS256"                   # 署名アルゴリズム（HMACと同じ発想）
ACCESS_TOKEN_EXPIRE_MINUTES = 30      # トークンの有効期限

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# トークン設定
def hash_password(password: str) -> str:
    # pwd_context.hash() でハッシュ化できる
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # pwd_context.verify() で検証できる
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    # dataのコピーを作り、有効期限(exp)を追加して、jwtでエンコードする
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str) -> str:
    # jwt.decode() でトークンを解読して、中のユーザー名を取り出す
    # 不正なトークンならJWTErrorが発生する
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token")
        return username
    except JWTError:
        raise ValueError("Invalid token")