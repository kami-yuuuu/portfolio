# 家計簿アプリ クイックスタートガイド

## 概要

このプロジェクトは FastAPI を使用した家計簿アプリケーションのバックエンドです。
取引（Transaction）、カテゴリ（Category）、支払い方法（PaymentMethod）を管理できます。

## 前提条件

- Docker & Docker Compose
- Python 3.11+ (ローカル開発の場合)
- PostgreSQL (ローカル開発の場合)

## セットアップ

### 1. Docker Compose を使用した起動（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/kami-yuuuu/portfolio.git
cd portfolio

# Docker Compose で起動
docker-compose up --build

# バックグラウンドで起動する場合
docker-compose up -d --build
```

サービスが起動すると、以下のURLでアクセスできます：
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 2. データベースの初期化

```bash
# コンテナ内でデータベーステーブルを作成
docker-compose exec backend python -m models.session create

# または、ホストから実行する場合
docker-compose exec backend python /app/src/models/session.py create
```

### 3. 動作確認

```bash
# ヘルスチェック
curl http://localhost:8000/health

# カテゴリの一覧取得（空の配列が返る）
curl http://localhost:8000/categories/

# カテゴリの作成
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "食費",
    "type": "expense",
    "color": "#FF5733"
  }'

# 支払い方法の作成
curl -X POST "http://localhost:8000/payment_methods/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "現金",
    "description": "現金での支払い"
  }'

# 取引の作成（category_id と payment_method_id は作成したものを使用）
curl -X POST "http://localhost:8000/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-08",
    "category_id": 1,
    "amount": 1500.00,
    "memo": "ランチ代",
    "payment_method_id": 1,
    "repeat": {}
  }'
```

## ローカル開発（Docker なし）

### 1. 環境設定

```bash
cd backend

# uv を使用した依存関係のインストール
pip install uv
uv sync

# または、pip を使用
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
# .env ファイルを作成
cat > .env << EOF
DATABASE_URL=postgresql://postgres:password@localhost:5432/postgresdb
EOF
```

### 3. PostgreSQL の起動

```bash
# Docker で PostgreSQL のみ起動
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=postgresdb \
  -p 5432:5432 \
  postgres:16
```

### 4. データベースの初期化

```bash
cd src
python -m models.session create
```

### 5. アプリケーションの起動

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API エンドポイント

### カテゴリ（Categories）

- `GET /categories/` - カテゴリ一覧取得
- `GET /categories/{id}` - カテゴリ詳細取得
- `POST /categories/` - カテゴリ作成
- `PATCH /categories/{id}` - カテゴリ更新
- `DELETE /categories/{id}` - カテゴリ削除

### 支払い方法（Payment Methods）

- `GET /payment_methods/` - 支払い方法一覧取得
- `GET /payment_methods/{id}` - 支払い方法詳細取得
- `POST /payment_methods/` - 支払い方法作成
- `PATCH /payment_methods/{id}` - 支払い方法更新
- `DELETE /payment_methods/{id}` - 支払い方法削除

### 取引（Transactions）

- `GET /transactions/` - 取引一覧取得
- `GET /transactions/{id}` - 取引詳細取得
- `POST /transactions/` - 取引作成
- `PATCH /transactions/{id}` - 取引更新
- `DELETE /transactions/{id}` - 取引削除

### ヘルスチェック

- `GET /health` - サーバーの状態確認

## データモデル

### Category（カテゴリ）
```json
{
  "name": "食費",
  "type": "expense",  // "income" or "expense"
  "color": "#FF5733"
}
```

### PaymentMethod（支払い方法）
```json
{
  "name": "現金",
  "description": "現金での支払い"
}
```

### Transaction（取引）
```json
{
  "date": "2024-01-08",
  "category_id": 1,
  "amount": 1500.00,
  "memo": "ランチ代",
  "payment_method_id": 1,
  "repeat": {},
  "receipt_url": null
}
```

## テストの実行

```bash
cd backend

# テストの実行（現在は不完全）
pytest

# 特定のテストの実行
pytest test/router/test_transaction.py
```

**注意**: 現在のテストは不完全です。テスト環境の整備が必要です。

## トラブルシューティング

### データベース接続エラー

```bash
# PostgreSQL が起動しているか確認
docker-compose ps

# PostgreSQL のログを確認
docker-compose logs db

# データベースの再作成
docker-compose down -v
docker-compose up -d
```

### ポートが使用中

```bash
# 8000 番ポートを使用しているプロセスを確認
lsof -i :8000

# または
netstat -an | grep 8000
```

### モジュールが見つからない

```bash
# PYTHONPATH を設定
export PYTHONPATH=/app/src:$PYTHONPATH

# または、Docker の場合は Dockerfile で設定済み
```

## 次のステップ

1. **データベース設定の整備**: Alembic マイグレーションの設定
2. **テストの拡充**: テスト環境の整備とテストケースの追加
3. **ドキュメントの更新**: API 仕様書の作成
4. **認証機能の追加**: JWT トークン認証の実装（オプション）
5. **フロントエンドの開発**: React アプリケーションの作成（オプション）

詳細は [TASK_ANALYSIS.md](./TASK_ANALYSIS.md) を参照してください。

## 参考リンク

- [FastAPI ドキュメント](https://fastapi.tiangolo.com/)
- [SQLModel ドキュメント](https://sqlmodel.tiangolo.com/)
- [PostgreSQL ドキュメント](https://www.postgresql.org/docs/)

## ライセンス

未定

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まず issue を開いて変更内容を議論してください。

---

*最終更新: 2026-01-08*
