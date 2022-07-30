#!/bin/bash
set -e

# echo never | tee /sys/kernel/mm/transparent_hugepage/enabled
# echo never | tee /sys/kernel/mm/transparent_hugepage/defrag

# allow the container to be started with `--user`
if [ "$1" = 'redis-server' -a "$(id -u)" = '0' ]; then
	sed -i 's/REDIS_PORT/'$REDIS_PORT'/g' /etc/redis/redis.conf
	# envsubst < redis.conf.template > /etc/redis/redis.conf
	chown -R redis .
	exec gosu redis "$0" "$@"
fi

exec "$@"