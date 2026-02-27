# Week 3-4: Alembic（DBマイグレーション）

## Alembicとは
- DBテーブルの構造変更をコードで管理する仕組み
- **組込みでいうと**: ファームウェアのOTAアップデート（バージョン管理＋パッチ適用）

## Git/GitHubフローとの対比
| Alembic | Git/GitHub |
|---------|-----------|
| `alembic revision --autogenerate` | PRを作成（差分を自動検出） |
| マイグレーションファイルを確認 | PRのコードレビュー |
| `alembic upgrade head` | マージしてデプロイ |
| `alembic downgrade -1` | revertして前のバージョンに戻す |

## 基本コマンド
```bash
alembic init alembic                          # 初期化
alembic revision --autogenerate -m "説明"     # 差分検出＋ファイル自動生成
alembic upgrade head                          # 最新まで適用
alembic downgrade -1                          # 1つ前に戻す
```

## マイグレーションファイルの構造
```python
def upgrade() -> None:
    # バージョンアップ時の処理（テーブル作成、カラム追加など）
    op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=False))

def downgrade() -> None:
    # ロールバック時の処理（upgrade の逆操作）
    op.drop_column('todos', 'user_id')
```
- `down_revision` → 前のバージョンへのリンク（gitコミットチェーンと同じ）
- `drop_table` → テーブルごと丸ごと削除（データも全部消える。Flashフォーマットに相当）

## NOT NULLカラムの追加（既存データがある場合）
```python
# そのままだとエラー（既存行にNULLが入るから）
op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=False))

# server_default を付けて解決
op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))
```
- DBはFlashと違い、ALTER TABLEで既存データを保持したままカラム追加できる

## セットアップ手順
1. `alembic.ini` の `sqlalchemy.url` をDB接続先に変更
2. `alembic/env.py` の `target_metadata` を `Base.metadata` に設定
3. これで `--autogenerate` がモデルとDBの差分を自動検出してくれる

## つまずきポイント
- `add_column` を2回書いてしまうミス → 元の行を**置き換える**のであって追加ではない
- 仮想環境を有効化しないと `alembic: command not found` になる
