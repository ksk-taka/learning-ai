# Phase1 学習メモ

## Pydantic (BaseModel)
- データの「型チェック」と「バリデーション（検証）」を自動でやってくれるライブラリ
- クラスを定義するだけで、送られてきたデータが正しい形かを自動チェックしてくれる
- FastAPI は内部で Pydantic を使っているので、バリデーションコードを自分で書かなくていい

### Optional（あってもなくてもいいデータ）
- `name: str` → 必須。無いとエラー
- `price: int | None = None` → 任意。無ければ None が入る
- `done: bool = False` → 任意。無ければ False が入る

## HTTP メソッドと CRUD の対応
| 操作 | HTTPメソッド | 意味 |
|------|-------------|------|
| Create（作成） | POST | 新しく作る |
| Read（取得） | GET | 読み取る |
| Update（更新） | PUT | 書き換える（全体を置き換え） |
| Delete（削除） | DELETE | 消す |

- PATCH というメソッドもあり、こちらは「一部だけ更新」

## for文 (`for t in todos:`)
- `todos` リストの中身を1つずつ `t` に入れて繰り返す
- `t` には id, name, done をまとめた1個の Todo オブジェクト（かたまり）が丸ごと入る
- `t.id`, `t.name`, `t.done` で各値にアクセスできる
- C言語のようにインデックス（`todos[i]`）を使わず、中身を直接受け取れるのが Python の特徴

### C言語との比較
```c
// C: インデックスで回す
for (int i = 0; i < 3; i++) {
    printf("%s", todos[i]);
}
```
```python
# Python: 中身を直接取り出す
for t in todos:
    print(t)
```

### remove の対象
- `todos.remove(t)` の `t` は、for文で今見ているかたまり全体を指す
- 一致したかたまり丸ごとリストから削除される

## 同期処理 vs 非同期処理 (async/await)
- **同期処理**: タスクを1つずつ順番に実行する。前のタスクが終わるまで次に進めない
- **非同期処理**: 待ち時間（I/O待ちなど）の間に別のタスクを進められる

### キーワード
- `async def` → この関数は非同期ですよ、という宣言
- `await` → ここで待ち時間が発生するよ（その間に他のタスクを進めてOK）
- `asyncio.gather()` → 複数のタスクを同時に実行する

### 実行時間の違い（async_test.py で確認）
- 順番に実行（同期的）: タスクA(2秒) + タスクB(1秒) = **合計3秒**
- 同時に実行（非同期的）: タスクC(2秒) と タスクD(1秒) を同時に走らせる = **合計2秒**（遅い方に合わせるだけ）

## PostgreSQL 基本操作（SQL）
- `CREATE TABLE` → テーブル作成（C言語の構造体定義に相当）
- `INSERT INTO` → データ追加（Create）
- `SELECT * FROM` → 全件取得（Read）
- `UPDATE ... SET ... WHERE` → 条件付き更新（Update）
- `DELETE FROM ... WHERE` → 条件付き削除（Delete）
- `WHERE` → C言語の `if` 条件に相当。絞り込みに使う
- `LIKE '%keyword%'` → ワイルドカード検索（`%` は何でもOK）
- `SERIAL` 型 → 自動インクリメント。削除しても番号は戻らない

## SQLAlchemy（ORM）
- ORM = Object Relational Mapping。SQLを直接書かずにPythonオブジェクトでDB操作
- 生SQL = レジスタ直叩き、ORM = HAL経由アクセス という対比

### ORM → SQL 対応表
| ORM | SQL |
|-----|-----|
| `db.query(Todo).all()` | `SELECT * FROM todos` |
| `db.query(Todo).filter(Todo.id == 5).first()` | `SELECT * FROM todos WHERE id = 5 LIMIT 1` |
| `db.add(obj)` + `db.commit()` | `INSERT INTO todos ...` |
| `obj.name = "new"` + `db.commit()` | `UPDATE todos SET name = 'new' WHERE ...` |
| `db.delete(obj)` + `db.commit()` | `DELETE FROM todos WHERE ...` |

### `.first()` vs `.all()`
- `.all()` → リスト（複数件）を返す
- `.first()` → 1件 or None を返す（`LIMIT 1`）

### FastAPIの引数の自動判別
| 書き方 | 値の出どころ |
|--------|------------|
| `todo: TodoCreate`（Pydanticモデル） | リクエストボディ（JSON） |
| `todo_id: int`（パスに `{todo_id}` あり） | パスパラメータ（URL） |
| `skip: int = 0`（パスにない普通の型） | クエリパラメータ（`?skip=10`） |
| `db: Session = Depends(get_db)` | サーバー内部で自動生成 |

### Depends（依存性注入）
- `Depends(get_db)` → FastAPIが関数実行前にDB接続を自動で開き、終了後に自動で閉じる
- 組込みでいうRTOSのリソースハンドル自動管理に近い
- 各エンドポイントでopen/closeのコードを書かなくて済む

## Alembic（マイグレーション）
- DBテーブルの構造変更をコードで管理する仕組み
- ファームウェアのOTAアップデート（バージョン管理＋パッチ適用）に近い

### 基本コマンド
- `alembic init alembic` → 初期化
- `alembic revision --autogenerate -m "説明"` → 差分検出してマイグレーションファイル自動生成
- `alembic upgrade head` → 最新まで適用
- `alembic downgrade -1` → 1つ前に戻す

### マイグレーションファイルの構造
- `upgrade()` → バージョンアップ時の処理
- `downgrade()` → ロールバック時の処理
- `down_revision` → 前のバージョンへのリンク（gitコミットチェーンと同じ）

### NOT NULLカラムの追加
- 既存データがあるテーブルにNOT NULLカラムを追加するには `server_default` が必要
- DBはFlashと違い、ALTER TABLEで既存データを保持したままカラム追加できる

## Q&A・つまずきメモ

### Q: `db` 変数もJSONリクエストから渡されるの？
- **No。** `Depends` がついた引数はサーバー内部で自動生成される
- FastAPIは引数の型・書き方で「外から来る値」と「内部で用意する値」を区別する
- `Depends` = 「カーネルがよしなにやってくれる部分」

### Q: FastAPIの引数判別は `Depends` 以外にもあるの？
- ある。Pydanticモデル→ボディ、パス変数→URL、普通の型→クエリパラメータ、Header/Cookieなど
- 実務でよく使うのは4種類（ボディ、パス、クエリ、Depends）

### Q: `first()` って何？
- `LIMIT 1` に相当。結果の最初の1件だけ返す
- 見つからなければ `None` を返す → だから直後に `if not todo:` で404チェックが必要

### Q: NOT NULLカラムを既存テーブルに追加するには？
- 組込み的発想: 退避→削除→新形式で再書き込み
- DB的発想: `server_default` を指定するだけでOK。ALTER TABLEで既存データ保持したまま追加できる

### つまずき: venvがディレクトリ移動で壊れた
- venvは作成時の絶対パスに依存する
- ディレクトリを移動したら `rm -rf venv` して作り直すのが正解
- 組込みでいうと、絶対アドレスでリンクしたバイナリを別アドレスに配置したのと同じ

### つまずき: passlibとbcryptのバージョン非互換
- bcrypt 4.1以降はpasslibと互換性がない（`__about__`属性が削除された）
- `pip install bcrypt==4.0.1` で解決
- ライブラリ間のバージョン依存は実務でもよくある問題

### Q: `raise` って何？
- エラーを投げて処理を中断する仕組み（C言語の `trigger_fault()` に相当）
- `raise HTTPException(status_code=409)` → FastAPIが自動でHTTPエラーレスポンスに変換
- `raise` された時点で関数を抜ける（以降のコードは実行されない）

### Q: `drop_table` って何？
- テーブルごと丸ごと削除（データも全部消える）
- Alembicのdowngrade関数で使う = ロールバック処理
- Flashのフォーマットに相当。本番では慎重に

## ユーザー認証

### パスワードハッシュ化（bcrypt）
- パスワードを一方向変換して保存。元に戻せない（OTPメモリに近い）
- salt付きで毎回違うハッシュが生成される → レインボーテーブル攻撃を防ぐ
- saltの役割 = 暗号通信のIV（初期化ベクトル）と同じ発想
- `passlib.context.CryptContext` でハッシュ化・検証

### JWT（JSON Web Token）
- ログイン成功後に発行される「入館証」
- 3つのパートで構成（ヘッダ.ペイロード.署名）、`.`で区切られている
- ペイロードに `sub`（ユーザー名）と `exp`（有効期限）を含む
- `python-jose` ライブラリで encode/decode
- BLEのペアリング後の暗号化キー交換に近い

### 認証フロー
```
1. POST /register → パスワードをハッシュ化してDBに保存
2. POST /login → パスワード検証 → JWTトークン発行
3. 以降のリクエスト → Authorization: Bearer <token> ヘッダで認証
4. サーバー側でトークンをデコードしてユーザーを特定
```

### OAuth2PasswordBearer
- FastAPIが `Authorization: Bearer <token>` ヘッダからトークンを自動抽出
- `Depends(oauth2_scheme)` でエンドポイントに認証を追加
- トークンなしのリクエストは自動的に `{"detail":"Not authenticated"}` を返す

### ForeignKey（外部キー）
- `ForeignKey("users.id")` = テーブル間の関連付け
- TodoにユーザーIDを持たせて「誰のTODOか」を管理
- ポインタが特定の構造体を指すことを型で保証するようなもの
- 既存テーブルへのFK追加時は `server_default` が必要（NOT NULL制約のため）
