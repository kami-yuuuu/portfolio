FROM nginx:1.21-alpine

# ローカルのdefault.confをコンテナにコピー
COPY docker/nginx/conf/default.conf /etc/nginx/conf.d/default.conf


COPY nginx/ssl/server.crt /etc/nginx/ssl/server.crt
COPY nginx/ssl/server.key /etc/nginx/ssl/server.key
COPY nginx/ssl/server.password /etc/nginx/ssl/server.password