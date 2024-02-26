FROM nginx:1.21-alpine

# ローカルのdefault.confをコンテナにコピー
COPY docker/nginx/conf/default.conf /etc/nginx/conf.d/default.conf


COPY /home/ubuntu/server.crt /etc/nginx/ssl/server.crt
COPY /home/ubuntu/server.key /etc/nginx/ssl/server.key
COPY /home/ubuntu/server.password /etc/nginx/ssl/server.password