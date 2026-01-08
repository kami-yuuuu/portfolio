# Issues and Technical Debt

このドキュメントでは、現在のプロジェクトで発見された問題と技術的負債を整理します。

## 🔴 Critical Issues（緊急対応が必要）

### Issue #1: プロジェクト名と実装の不一致
**優先度**: P0（最高）
**影響度**: 高

**問題**:
- リポジトリ名: `portfolio`
- README.md: ポートフォリオアプリケーションの説明
- 実際の実装: 家計簿アプリケーション（Finance App）
- memo.md: 家計簿アプリと明記

**影響**:
- ドキュメントと実装が完全に乖離
- 新規開発者の混乱を招く
- リポジトリの目的が不明確

**対応策**:
1. プロジェクトの目的を明確に決定
2. README.mdを実装に合わせて書き換え
3. リポジトリ名の変更を検討（または portfolio を finance に統一）

**推定工数**: 1-2時間

---

### Issue #2: データベーススキーマの未管理
**優先度**: P0（最高）
**影響度**: 高

**問題**:
- Alembic が依存関係にあるが、マイグレーションファイルが存在しない
- `alembic/` ディレクトリが無い
- データベースの初期化方法が `session.py` のスクリプト実行のみ
- スキーマの変更履歴が追跡できない

**影響**:
- データベース構造の変更が困難
- 本番環境へのデプロイが危険
- ロールバックができない

**対応策**:
```bash
# Alembic の初期化
cd backend
alembic init alembic

# env.py の設定
# alembic/env.py に SQLModel のメタデータを設定

# 初期マイグレーションの作成
alembic revision --autogenerate -m "Initial migration"

# マイグレーションの適用
alembic upgrade head
```

**推定工数**: 2-3時間

---

### Issue #3: テストの不完全性
**優先度**: P1（高）
**影響度**: 中

**問題**:
- `test_transaction.py` に `session` 変数が未定義
- テストが実行できない状態
- テストデータベースの設定が無い
- pytest の設定ファイル（pytest.ini / pyproject.toml）が無い

**現在のコード**:
```python
# test/router/test_transaction.py (L11)
def get_test_session():
    return session  # ← session が未定義
```

**影響**:
- テストが実行できない
- CI/CD パイプラインが構築できない
- コードの品質保証ができない

**対応策**:
```python
# test/router/test_transaction.py の修正案
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

# テスト用のインメモリデータベース
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_test_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

**推定工数**: 1-2時間

---

## 🟡 High Priority Issues（早期対応が推奨）

### Issue #4: 環境変数管理の不備
**優先度**: P1（高）
**影響度**: 中

**問題**:
- `.env.example` ファイルが存在しない
- 環境変数の一覧が不明確
- `docker-compose.yml` の環境変数が "finance_db" になっている

**対応策**:
1. `.env.example` の作成
2. README への環境変数の説明追加
3. docker-compose.yml の環境変数を統一

**推定工数**: 1時間

---

### Issue #5: Docker Compose の設定不一致
**優先度**: P1（高）
**影響度**: 低

**問題**:
```yaml
# docker-compose.yml
environment:
  - DATABASE_URL=postgresql://devuser:devpass@db:5432/finance_db
```

一方、session.py では:
```python
postgres_url = os.getenv(
    "DATABASE_URL",
    default="postgresql://postgres:password@db:5432/postgresdb"
)
```

デフォルト値が異なる。

**対応策**:
- 環境変数を統一
- .env ファイルで管理

**推定工数**: 30分

---

### Issue #6: 未使用の依存関係
**優先度**: P2（中）
**影響度**: 低

**問題**:
以下の依存関係がインストールされているが、使用されていない：
- `redis==5.0.1` - キャッシュ用（README には記載あり）
- `celery==5.3.4` - バックグラウンドタスク用
- `httpx==0.25.2` - 用途不明
- `python-jose[cryptography]==3.3.0` - JWT認証用（未実装）
- `python-multipart==0.0.6` - ファイルアップロード用（未実装）

**影響**:
- イメージサイズの肥大化
- 依存関係の複雑化
- セキュリティリスクの増加

**対応策**:
1. 使用する予定があるものはそのまま
2. 不要なものは削除
3. 使用予定のものはコメントで明記

**推定工数**: 30分

---

## 🟢 Medium Priority Issues（改善推奨）

### Issue #7: Dockerfile の CMD がコメントアウト
**優先度**: P2（中）
**影響度**: 低

**問題**:
```dockerfile
# Dockerfile (L35)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

CMD がコメントアウトされているため、コンテナが起動しない。

**影響**:
- Docker単体での起動ができない
- docker-compose.yml の command に依存

**対応策**:
- CMD のコメントを解除
- docker-compose.yml でオーバーライドする場合はそのまま

**推定工数**: 5分

---

### Issue #8: フロントエンドの不在
**優先度**: P2（中）
**影響度**: 中

**問題**:
- `k8s/frontend/` ディレクトリに設定があるが、`frontend/` ディレクトリが存在しない
- README.md にフロントエンドの記載がある

**影響**:
- K8s設定が不完全
- 完全なアプリケーションとして動作しない

**対応策**:
1. フロントエンドを開発する（React + TypeScript）
2. または、K8s の frontend 設定を削除

**推定工数**: フロントエンド開発なら数週間、削除なら5分

---

### Issue #9: K8s ConfigMap/Secret の不在
**優先度**: P2（中）
**影響度**: 中

**問題**:
- `k8s/backend/deployment.yaml` で参照されている ConfigMap と Secret が存在しない
- `k8s/shared/` ディレクトリが存在しない

```yaml
# deployment.yaml で参照
configMapKeyRef:
  name: portfolio-config  # ← このファイルが無い
secretKeyRef:
  name: portfolio-secret  # ← このファイルが無い
```

**影響**:
- Kubernetes デプロイができない
- 環境変数が設定されない

**対応策**:
- `k8s/shared/configmap.yaml` の作成
- `k8s/shared/secret.yaml` の作成
- `k8s/shared/namespace.yaml` の作成

**推定工数**: 1-2時間

---

### Issue #10: API ドキュメントの不足
**優先度**: P3（低）
**影響度**: 低

**問題**:
- FastAPI の自動生成ドキュメント（/docs）のみ
- 追加のドキュメントが無い
- レスポンス例が少ない

**対応策**:
1. OpenAPI の description を充実させる
2. example を各モデルに追加
3. 別途 API 仕様書を作成（オプション）

**推定工数**: 2-3時間

---

## 📋 Technical Debt（技術的負債）

### TD-1: 型ヒントの不完全性
- 一部の関数で戻り値の型ヒントが無い
- mypy などの型チェッカーを導入すべき

### TD-2: エラーハンドリングの不足
- データベースエラーのハンドリングが無い
- バリデーションエラーの詳細が不明確

### TD-3: ロギングの不足
- 構造化ログが無い
- デバッグが困難

### TD-4: セキュリティ考慮の不足
- CORS の設定が無い
- レート制限が無い
- SQL インジェクション対策は SQLModel が対応

### TD-5: パフォーマンス最適化
- N+1 問題の可能性
- インデックスの最適化が必要

---

## 推奨される対応順序

1. **Issue #1**: README の修正（30分）
2. **Issue #3**: テストの修正（1-2時間）
3. **Issue #4**: 環境変数の整備（1時間）
4. **Issue #2**: Alembic の設定（2-3時間）
5. **Issue #5**: Docker Compose の統一（30分）
6. **Issue #7**: Dockerfile の修正（5分）
7. **Issue #9**: K8s 設定の整備（1-2時間）
8. **Issue #6**: 依存関係の整理（30分）
9. **Issue #8**: フロントエンドの決定（判断必要）
10. **Issue #10**: ドキュメントの拡充（2-3時間）

**合計推定工数**: 約1-2週間（フロントエンド除く）

---

*最終更新: 2026-01-08*
