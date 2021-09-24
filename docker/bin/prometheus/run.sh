docker run -d -p 9090:9090 --user 996:996 \ 
--net=host \
-v /etc/prometheus/prometheus.yml \ 
-v /data/prometheus \ 
prom/prometheus \ 
--config.file="/etc/prometheus/prometheus.yml" \ 
--storage.tsdb.path="/var/lib/prometheus"

docker run -d -p 9100:9100 --user 995:995 \
-v "/:/hostfs" \
--net="host" \
prom/node-exporter \
--path.rootfs=/hostfs

# prometheus
