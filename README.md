# Portfolio Application

A modern portfolio application built with FastAPI, React, Docker, and Kubernetes.

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React (TypeScript)
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Project Structure

```
portfolio/
├── backend/              # FastAPI backend
│   ├── main.py          # メインアプリケーション
│   ├── config.py        # 設定管理
│   ├── database.py      # データベース接続
│   ├── models.py        # SQLAlchemyモデル
│   ├── schemas.py       # Pydanticスキーマ
│   ├── crud.py          # CRUD操作
│   ├── auth.py          # 認証機能
│   ├── requirements.txt # Python依存関係
│   ├── Dockerfile       # バックエンド用Dockerfile
│   └── env.example      # 環境変数例
├── frontend/            # React frontend
│   └── package.json     # Node.js依存関係
├── k8s/                 # Kubernetes manifests
│   ├── shared/          # 共有リソース
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── ingress.yaml
│   │   ├── postgres-deployment.yaml
│   │   ├── postgres-service.yaml
│   │   ├── postgres-pvc.yaml
│   │   ├── redis-deployment.yaml
│   │   └── redis-service.yaml
│   ├── backend/        # バックエンド用リソース
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── frontend/       # フロントエンド用リソース
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── deploy.sh       # デプロイスクリプト
│   └── cleanup.sh      # クリーンアップスクリプト
├── docker-compose.yml   # Docker Compose設定
└── README.md
```

## Features

### Backend API
- **Projects**: プロジェクト管理（CRUD操作）
- **About**: プロフィール情報管理
- **Skills**: スキル管理
- **Contacts**: お問い合わせ管理
- **Authentication**: JWT認証
- **Database**: PostgreSQL with SQLAlchemy
- **Cache**: Redis for caching

### API Endpoints
- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック
- `GET /api/projects` - プロジェクト一覧
- `GET /api/projects/{id}` - プロジェクト詳細
- `POST /api/projects` - プロジェクト作成（認証必要）
- `PUT /api/projects/{id}` - プロジェクト更新（認証必要）
- `DELETE /api/projects/{id}` - プロジェクト削除（認証必要）
- `GET /api/about` - プロフィール情報
- `PUT /api/about` - プロフィール更新（認証必要）
- `GET /api/skills` - スキル一覧
- `POST /api/skills` - スキル作成（認証必要）
- `GET /api/contacts` - お問い合わせ一覧（認証必要）
- `POST /api/contacts` - お問い合わせ送信

## Quick Start

### 1. Development with Docker Compose

```bash
# アプリケーションを起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d --build
```

**Services:**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 2. Kubernetes Deployment

```bash
# デプロイ
./k8s/deploy.sh

# クリーンアップ
./k8s/cleanup.sh
```

**Access:**
- Frontend: http://portfolio.local (Ingress経由)
- Backend API: http://portfolio.local/api

### 3. Manual Kubernetes Deployment

```bash
# 名前空間と共有リソース
kubectl apply -f k8s/shared/

# バックエンド
kubectl apply -f k8s/backend/

# フロントエンド
kubectl apply -f k8s/frontend/
```

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## Environment Variables

### Backend (.env)
```env
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://portfolio:portfolio@localhost:5432/portfolio
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
```

## Database Schema

### Projects Table
- id, title, description, technologies, github_url, demo_url, image_url
- is_featured, is_active, created_at, updated_at

### About Table
- id, name, title, bio, email, github, linkedin, twitter
- location, phone, resume_url, created_at, updated_at

### Skills Table
- id, name, category, level, is_active, created_at

### Contacts Table
- id, name, email, subject, message, is_read, created_at

## Authentication

API認証はJWTトークンを使用します。

```bash
# トークン取得（簡易版）
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 認証付きリクエスト
curl -X GET "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Monitoring

### Health Checks
- Backend: `GET /health`
- Database: PostgreSQL connection check
- Cache: Redis connection check

### Logs
```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes
kubectl logs -f deployment/portfolio-backend -n portfolio
kubectl logs -f deployment/portfolio-frontend -n portfolio
```

## Production Considerations

1. **Security**: 本番環境では適切なSECRET_KEYを設定
2. **Database**: 本番用データベースの設定
3. **SSL/TLS**: HTTPS設定
4. **Monitoring**: ログ監視とアラート設定
5. **Backup**: データベースバックアップ戦略
6. **Scaling**: 水平スケーリング設定

## License

MIT License
