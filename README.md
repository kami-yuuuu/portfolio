# 家計簿アプリ（バックエンド）

FastAPI・SQLModel・PostgreSQL で実装した、家計簿アプリのバックエンドAPIです。現在は取引・カテゴリ・支払い方法のCRUD APIを提供しています。リポジトリ名は `portfolio` ですが、ポートフォリオアプリではありません。

> **開発段階:** 試作段階です。テスト環境、DBマイグレーション、認証、フロントエンドは未整備です。本番環境での利用を想定した状態ではありません。

## 実装済みの機能

- 取引（Transaction）の作成・一覧・詳細・更新・削除
- カテゴリ（Category）の作成・一覧・詳細・更新・削除
- 支払い方法（PaymentMethod）の作成・一覧・詳細・更新・削除
- `GET /health` によるヘルスチェック
- FastAPIが生成するAPIドキュメント

認証、ユーザー管理、集計・レポート、レシート画像のアップロード、フロントエンドは実装されていません。

## 技術構成

- Python 3.11+
- FastAPI、SQLModel / SQLAlchemy
- PostgreSQL 16
- Docker Compose

## 起動方法（Docker Compose）

Docker と Docker Compose がインストールされていることを確認し、リポジトリのルートで実行します。

```bash
docker compose up --build
```

APIとデータベースが起動したら、**初回のみ**テーブルを作成します。

```bash
docker compose exec backend python -m models.session create
```

アクセス先:

- APIドキュメント: <http://localhost:8000/docs>
- ヘルスチェック: <http://localhost:8000/health>
- PostgreSQL: `localhost:5432`

停止するには `Ctrl+C` を押します。バックグラウンドで起動した場合は `docker compose down` を実行してください。

ComposeのDB接続情報は開発用です。`docker-compose.yml` に設定されている認証情報を本番環境で使用しないでください。

## APIエンドポイント

各リソースは一覧・詳細取得、作成、部分更新、削除のエンドポイントを持ちます。

| リソース | エンドポイント |
| --- | --- |
| 取引 | `/transactions/`、`/transactions/{transaction_id}` |
| カテゴリ | `/categories/`、`/categories/{category_id}` |
| 支払い方法 | `/payment_methods/`、`/payment_methods/{payment_method_id}` |
| ヘルスチェック | `/health` |

一覧・詳細取得は `GET`、作成は `POST`、部分更新は `PATCH`、削除は `DELETE` です。リクエストとレスポンスの詳細は `/docs` を参照してください。

### 取引作成の例

先にカテゴリと支払い方法を作成し、それぞれのIDを指定します。

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

## データモデル

- **Category**: 名前、種別（収入・支出など）、表示色
- **PaymentMethod**: 名前、説明
- **Transaction**: 日付、カテゴリ、金額、メモ、支払い方法、繰り返し設定、レシートURL

詳細なフィールド定義は `backend/src/models/` を参照してください。

## 開発・運用上の注意

- テーブル作成は `create_all` による初期化です。Alembicのマイグレーションはまだ整備されていません。スキーマ変更の履歴管理や安全な更新が必要な環境には未対応です。
- テストは未整備で、現在のテストコードには未定義のDBセッションなどの問題があります。テストが通ることを品質保証として扱わないでください。
- Kubernetes用の設定ファイルはありますが、フロントエンドや参照先の共有設定などが揃っていないため、そのままデプロイできる状態ではありません。
- 認証・認可は実装されていません。ネットワークに公開しないでください。

## 主なディレクトリ

```text
backend/src/       FastAPIアプリ、モデル、ルーター
backend/test/      テスト（未整備）
k8s/               Kubernetes設定（未完成）
docker-compose.yml 開発用バックエンド・PostgreSQL構成
```

## 次に取り組むこと

1. テスト用DBとfixtureを整備し、APIテストを実行可能にする
2. AlembicによるDBマイグレーションを導入する
3. 環境変数と開発用設定を整理する
4. アプリの提供形態を決め、必要に応じて認証やフロントエンドを実装する

タスクの詳細は [`TASK_ANALYSIS.md`](./TASK_ANALYSIS.md)、起動時の補足は [`QUICK_START_GUIDE.md`](./QUICK_START_GUIDE.md) を参照してください。
