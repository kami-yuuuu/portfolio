FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY . .
RUN pip install --no-cache-dir pyproject.toml

# アプリケーションコードをコピー

# 非rootユーザーを作成
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# ポート8000を公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# アプリケーションを起動
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
