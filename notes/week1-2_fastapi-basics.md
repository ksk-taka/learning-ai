# Week 1-2: FastAPI + Python Web開発の基礎

## Pydantic (BaseModel)
- データの「型チェック」と「バリデーション（検証）」を自動でやってくれるライブラリ
- クラスを定義するだけで、送られてきたデータが正しい形かを自動チェック
- FastAPI は内部で Pydantic を使っている

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

- PATCH = 「一部だけ更新」

## for文（C言語との違い）
```python
# Python: 中身を直接取り出す
for t in todos:
    print(t)
```
```c
// C: インデックスで回す
for (int i = 0; i < 3; i++) {
    printf("%s", todos[i]);
}
```

## FastAPIの引数の自動判別
| 書き方 | 値の出どころ |
|--------|------------|
| `todo: TodoCreate`（Pydanticモデル） | リクエストボディ（JSON） |
| `todo_id: int`（パスに `{todo_id}` あり） | パスパラメータ（URL） |
| `skip: int = 0`（パスにない普通の型） | クエリパラメータ（`?skip=10`） |
| `db: Session = Depends(get_db)` | サーバー内部で自動生成 |

## Depends（依存性注入）
- `Depends(get_db)` → FastAPIが関数実行前にDB接続を自動で開き、終了後に自動で閉じる
- **組込みでいうと**: RTOSのリソースハンドル自動管理に近い
- 各エンドポイントでopen/closeのコードを書かなくて済む

## raise（例外処理）
- エラーを投げて処理を中断する仕組み
- **組込みでいうと**: C言語の `trigger_fault()` に相当
- `raise HTTPException(status_code=409)` → FastAPIが自動でHTTPエラーレスポンスに変換
- `raise` された時点で関数を抜ける（以降のコードは実行されない）

## 成果物
- TODOアプリの REST API（CRUD全操作）
- エンドポイント: GET /, POST /todos, GET /todos, GET /todos/{id}, PUT /todos/{id}, PATCH /todos/{id}/done, DELETE /todos/{id}
