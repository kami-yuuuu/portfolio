# 即座に対応すべき項目（Quick Fixes）

このドキュメントでは、すぐに対応可能で影響の大きい項目をリストアップします。

## 🚀 今すぐ実行可能（30分以内）

### 1. README.md の更新
**所要時間**: 15分
**優先度**: 最高

README.md を実際の実装（家計簿アプリ）に合わせて書き換える。

```bash
# バックアップを作成
mv README.md README_old.md

# 新しい README を作成
cat > README.md << 'EOF'
# 家計簿アプリケーション（Finance App）

FastAPI と PostgreSQL を使用した家計簿管理アプリケーションのバックエンドです。

## 機能

- 取引（Transaction）の管理
- カテゴリ（Category）の管理
- 支払い方法（PaymentMethod）の管理

詳細は [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md) を参照してください。
EOF
```

---

### 2. .env.example の作成
**所要時間**: 10分
**優先度**: 高

```bash
cd backend

cat > .env.example << 'EOF'
# データベース設定
DATABASE_URL=postgresql://postgres:password@localhost:5432/postgresdb

# アプリケーション設定
DEBUG=True
LOG_LEVEL=INFO

# サーバー設定
HOST=0.0.0.0
PORT=8000
EOF
```

---

### 3. Dockerfile の CMD を有効化
**所要時間**: 2分
**優先度**: 中

```bash
cd backend

# Dockerfile の最終行のコメントを解除
sed -i 's/# CMD/CMD/' Dockerfile
```

または手動で：
```dockerfile
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
↓
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 4. .gitignore の追加
**所要時間**: 5分
**優先度**: 中

```bash
# ルートディレクトリの .gitignore に追加
cat >> .gitignore << 'EOF'

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Alembic
alembic/versions/*_*.py

# Logs
*.log
EOF
```

---

## ⏱️ 1-2時間で完了

### 5. テストの修正
**所要時間**: 1時間
**優先度**: 高

```python
# backend/test/conftest.py を作成
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.dependencies import get_session

# テスト用のインメモリデータベース
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

```python
# backend/test/router/test_transaction.py を修正
def test_get_transactions(client):
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

### 6. docker-compose.yml の環境変数統一
**所要時間**: 15分
**優先度**: 高

```yaml
# docker-compose.yml を修正
version: "3.9"
services:
  backend:
    build: ./backend
    container_name: backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    volumes:
      - ./backend/src:/app/src
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/postgresdb
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: postgresdb
    ports:
      - "5432:5432"
    volumes:
      - ./db/postgres:/var/lib/postgresql/data
```

---

### 7. pytest.ini の作成
**所要時間**: 10分
**優先度**: 中

```bash
cd backend

cat > pytest.ini << 'EOF'
[pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers

markers =
    unit: Unit tests
    integration: Integration tests
EOF
```

---

## 🔧 2-3時間で完了

### 8. Alembic の設定
**所要時間**: 2時間
**優先度**: 高

```bash
cd backend

# Alembic の初期化
alembic init alembic

# env.py の編集（SQLModel のメタデータを使用）
```

```python
# alembic/env.py の target_metadata を変更
from src.models import transaction, category, payment_method
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata
```

```bash
# 初期マイグレーションの作成
alembic revision --autogenerate -m "Initial migration"

# マイグレーションの適用
alembic upgrade head
```

---

### 9. K8s の ConfigMap/Secret 作成
**所要時間**: 1時間
**優先度**: 中

```bash
mkdir -p k8s/shared

cat > k8s/shared/namespace.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: portfolio
EOF

cat > k8s/shared/configmap.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: portfolio-config
  namespace: portfolio
data:
  DEBUG: "False"
  HOST: "0.0.0.0"
  PORT: "8000"
  DATABASE_URL: "postgresql://portfolio:portfolio@postgres:5432/portfolio"
  REDIS_URL: "redis://redis:6379"
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
  LOG_LEVEL: "INFO"
EOF

cat > k8s/shared/secret.yaml << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: portfolio-secret
  namespace: portfolio
type: Opaque
stringData:
  jwt-secret: "change-me-in-production"
EOF
```

---

## 📝 実行チェックリスト

完了したらチェック：

- [ ] README.md の更新
- [ ] .env.example の作成
- [ ] Dockerfile の CMD 有効化
- [ ] .gitignore の更新
- [ ] テストの修正
- [ ] docker-compose.yml の統一
- [ ] pytest.ini の作成
- [ ] Alembic の設定
- [ ] K8s ConfigMap/Secret の作成

---

## 🎯 次のステップ

全ての Quick Fixes を完了したら：

1. **動作確認**
   ```bash
   docker-compose up --build
   docker-compose exec backend python -m models.session create
   pytest
   ```

2. **ドキュメントの確認**
   - QUICK_START_GUIDE.md の手順を実行
   - API ドキュメント（/docs）を確認

3. **次の開発フェーズへ**
   - TASK_ANALYSIS.md のフェーズ2へ進む
   - 機能の拡充を検討

---

*作成日: 2026-01-08*
*推定完了時間: 合計 4-6時間*
