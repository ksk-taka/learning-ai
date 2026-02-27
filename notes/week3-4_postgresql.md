# Week 3-4: PostgreSQL（SQL基礎）

## 基本操作
| SQL | 操作 | 組込み的対比 |
|-----|------|------------|
| `CREATE TABLE` | テーブル作成 | 構造体定義 |
| `INSERT INTO` | データ追加（Create） | Flash書き込み |
| `SELECT * FROM` | 全件取得（Read） | Flash読み出し |
| `UPDATE ... SET ... WHERE` | 条件付き更新（Update） | セクタ書き換え |
| `DELETE FROM ... WHERE` | 条件付き削除（Delete） | セクタ消去 |

## 絞り込み
- `WHERE` → C言語の `if` 条件に相当
- `LIKE '%keyword%'` → ワイルドカード検索（`%` は何でもOK）
- `LIMIT 1` → 最初の1件だけ取得

## データ型
- `SERIAL` 型 → 自動インクリメント。削除しても番号は戻らない
- `VARCHAR(255)` → 可変長文字列（最大255文字）
- `BOOLEAN` → true/false
- `TIMESTAMP` → 日時

## Docker上でのPostgreSQL
```bash
# コンテナ起動
docker-compose up -d

# psqlに接続
docker exec -it todo_postgres psql -U todo_user -d todo_db

# テーブル一覧
\dt

# テーブル構造
\d todos
```
