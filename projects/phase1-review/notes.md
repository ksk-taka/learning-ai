# Phase 1 復習メモ（Memoアプリ）

## ファイル構成の役割

### schemas.py — APIの入力定義（ユーザーが送るデータだけ）
- UserCreate: username, password（登録とログインで共用）
- MemoCreate: title, content
- **user_idはスキーマに入れない** → トークンからサーバー側で特定する（セキュリティ上重要）

### auth.py — 認証系の道具箱
- hash_password: パスワードのハッシュ化（bcrypt）
- verify_password: パスワードの照合
- create_access_token: JWTトークン作成（sub=ユーザー名, exp=有効期限）
- get_current_user: トークンからユーザー名を取得

### models.py — DBのテーブル定義（SQLAlchemy）
- BaseModel（Pydantic）ではなくBase（SQLAlchemy）を使う
- Mapped[型] + mapped_column() でカラム定義
- ForeignKey でテーブル間の関連付け

### main.py — エンドポイント（APIの窓口）
- ユーザー: 登録（POST /register）、ログイン（POST /login）
- メモ: 作成・一覧取得・個別取得・更新・削除（CRUD）
- 認証が必要なエンドポイントには `token: str = Depends(oauth2_scheme)` を付ける

## 学んだこと
- .first() は「クエリを実行して1件取得」、.all() は「全件取得」
- filter() だけではまだ実行されない（DMA設定 → first()/all() が転送トリガー）
- OAuth2PasswordBearer: Authorization ヘッダからトークンを自動抽出する仕組み
- コードリーディングは割とできるようになった。書く方はまだ自動補完に頼る部分が多い
