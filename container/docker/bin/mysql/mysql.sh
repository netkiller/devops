
docker run --name mysql -d \
    --restart always \
    -e MYSQL_ROOT_PASSWORD=D120852B-CFEA-4CC3-951B-AA934B5A527C \
    -e MYSQL_DATABASE=test \
    -e MYSQL_USER=test \
    -e MYSQL_PASSWORD=D120852B-CFEA-4CC3-951B-AA934B5A527C \
    -p 3306:3306 \
    mysql:latest