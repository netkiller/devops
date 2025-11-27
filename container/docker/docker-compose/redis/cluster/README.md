# Redis Cluster

    $ firewall-cmd --permanent --zone=public --add-port=7000-7005/tcp
    $ firewall-cmd --permanent --zone=public --add-port=17000-17005/tcp
    //重新加载配置
    $ firewall-cmd --reload  
    //查看开放的端口
    $ firewall-cmd --permanent --zone=public --list-ports  


You can change the Redis port by setting REDIS_PORT when running the container.

    docker run -e REDIS_PORT=9999 publicisworldwide/redis-cluster

    redis-cli -a 123123123 --cluster create 172.25.3.21:7000 172.25.3.22:7000 172.25.3.21:7001 172.25.3.22:7001 172.25.3.21:7002 172.25.3.22:7002 172.25.3.21:7003 172.25.3.22:7003  --cluster-replicas 1