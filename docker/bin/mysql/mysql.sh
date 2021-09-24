
docker run --name mysql -d \
    --restart always \
    -e MYSQL_ROOT_PASSWORD=chen \
    -e MYSQL_DATABASE=neo \
    -e MYSQL_USER=neo \
    -e MYSQL_PASSWORD=neo \
    -p 127.0.0.1:3306:3306 \
    mysql:latest