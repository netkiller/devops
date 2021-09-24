# sudo useradd -rs /bin/false prometheus
# sudo useradd -rs /bin/false node_exporter

mkdir -p /var/lib/{prometheus,grafana,alertmanager} /var/log/grafana
chown neo:staff /var/lib/{prometheus,grafana,alertmanager}
chmod 777 /var/lib/{prometheus,grafana,alertmanager} /var/log/grafana
docker-compose up
