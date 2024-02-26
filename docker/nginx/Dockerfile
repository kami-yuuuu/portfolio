FROM nginx:1.21-alpine

# ローカルのdefault.confをコンテナにコピー
COPY docker/nginx/conf/default.conf /etc/nginx/conf.d/default.conf


COPY docker/nginx/ssl/server.crt /etc/nginx/ssl/server.crt
COPY docker/nginx/ssl/server.key /etc/nginx/ssl/server.key
COPY docker/nginx/ssl/server.password /etc/nginx/ssl/server.password