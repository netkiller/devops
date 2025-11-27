docker pull redis

docker run --name redis -v /var/lib/redis:/data -p 6379:6379 -d redis redis-server --appendonly yes