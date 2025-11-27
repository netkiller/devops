port ${PORT}
protected-mode no
appendonly yes

cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-announce-ip 123.207.67.174
cluster-announce-port ${PORT}
cluster-announce-bus-port 1${PORT}
cluster-node-timeout 5000
