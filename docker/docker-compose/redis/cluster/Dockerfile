FROM redis:latest

ARG node
ENV REDIS_PORT 6379

#COPY ${node}/redis.conf /etc/redis/redis.conf
COPY redis.conf /etc/redis/redis.conf
COPY docker-entrypoint.sh /

#修复时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
RUN echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' > /etc/rc.local

#修改文件权限,使之可以通过config rewrite重写
RUN chmod +rw /etc/redis/redis.conf
RUN chmod +x /docker-entrypoint.sh

# Redis客户端连接端口
EXPOSE 6379
EXPOSE 16379
EXPOSE $REDIS_PORT

#使用自定义conf启动
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "redis-server", "/etc/redis/redis.conf" ]