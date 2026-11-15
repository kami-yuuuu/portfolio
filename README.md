# 家計簿アプリ（バックエンド）

FastAPI・SQLModel・PostgreSQL で実装した家計簿アプリのバックエンドAPIです。取引・カテゴリ・支払い方法のCRUD APIを提供します。

> **開発段階:** 試作段階です。認証やフロントエンドは未実装で、本番環境での利用は想定していません。

## 実装済み

- 取引、カテゴリ、支払い方法の作成・一覧・詳細・更新・削除
- 入力値の基本検証とDB制約違反へのHTTP 409応答
- APIレスポンス用スキーマ、`GET /health`
- AlembicによるDBスキーママイグレーション

## 技術構成

- Python 3.11+
- FastAPI、SQLModel / SQLAlchemy、Alembic
- PostgreSQL 16
- Docker Compose

## 起動（Docker Compose）

Docker と Docker Compose がインストールされていることを確認し、リポジトリのルートで実行します。

```bash
cp .env.example .env
docker compose up --build
```

ComposeがDBのヘルスチェックを待ち、バックエンド起動時に `alembic upgrade head` を実行してからAPIを開始します。

- APIドキュメント: <http://localhost:8000/docs>
- ヘルスチェック: <http://localhost:8000/health>
- PostgreSQL: `localhost:5432`

停止は `Ctrl+C`。バックグラウンド起動時は `docker compose down` を実行してください。データも削除する場合は `docker compose down -v` ですが、DBボリュームの内容は復元できないため注意してください。

`.env.example` の認証情報はローカル開発専用です。本番環境では強固な認証情報と秘密情報管理を設定してください。

## 既存データベースから移行する場合

従来の `create_all` で作成済みのDBに対しては、そのまま `alembic upgrade head` を実行すると既存テーブルと衝突します。まずバックアップを取得してスキーマを確認し、初期マイグレーションの内容と一致することを確認した場合に限り、Alembicの履歴を登録します。

```bash
cd backend
# DATABASE_URLを対象DBに設定したうえで、既存スキーマを必ず確認してから実行
alembic stamp 0001_initial
alembic upgrade head
```

スキーマが初期マイグレーションと異なる場合は、データを保全したうえで差分マイグレーションを作成してください。`stamp` はテーブルを作成・検証する操作ではありません。

## API

| リソース | 一覧・作成 | 詳細・更新・削除 |
| --- | --- | --- |
| 取引 | `/transactions/` | `/transactions/{transaction_id}` |
| カテゴリ | `/categories/` | `/categories/{category_id}` |
| 支払い方法 | `/payment_methods/` | `/payment_methods/{payment_method_id}` |
| ヘルスチェック | `/health` | — |

一覧・詳細取得は `GET`、作成は `POST`（201）、部分更新は `PATCH`、削除は `DELETE`（`{"ok": true}`）です。一覧の `skip` は0以上、`limit` は1〜100です。不正な入力は422、対象なしは404、重複データや参照整合性違反は409を返します。具体的な項目は `/docs` を参照してください。

### 取引作成の例

カテゴリと支払い方法を先に作成し、そのIDを指定します。

```bash
curl -X POST http://localhost:8000/transactions/ \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2026-01-08",
    "category_id": 1,
    "amount": 1500.00,
    "memo": "ランチ代",
    "payment_method_id": 1,
    "repeat": {}
  }'
```

## 環境変数

Composeではルートの `.env` から設定します。ローカル実行時は `DATABASE_URL` を設定してください。

- `DATABASE_URL`: SQLAlchemyのPostgreSQL接続URL（必須）
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Compose DB用設定
- `SQL_ECHO`: SQLログ出力（既定 `false`。開発時のみ有効化）

## ローカル開発

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL='postgresql://devuser:devpass@localhost:5432/finance_db'
alembic upgrade head
PYTHONPATH=src uvicorn main:app --reload
```

スキーマ変更はモデルを更新したうえでAlembicリビジョンを作成・確認し、適用します。

```bash
cd backend
alembic revision --autogenerate -m "describe schema change"
# 生成ファイルを確認・修正してから
alembic upgrade head
```

## 注意事項

- 認証・認可がないため、APIをインターネットに公開しないでください。
- Composeはローカル開発用の既定認証情報を持ちます。本番用ではありません。
- テストはまだ不十分で、DBテスト環境の整備が別途必要です。
- `create_all` の旧ヘルパーは互換性のため残っていますが、新規環境の作成やスキーマ更新にはAlembicを使ってください。
