minikube stop

minikube start --memory 4096mb --cpus 2 --cache-images=true --driver=hyperkit \
--extra-config="kubelet.allowed-unsafe-sysctls=kernel.msg*,net.core.somaxconn,vm.*" \
--image-mirror-country=cn \
--insecure-registry="127.0.0.1:5000,192.168.3.0/24,192.168.64.0/24,172.17.0.0/16,10.10.0.0/24" \
--registry-mirror="https://registry.docker-cn.com,https://docker.mirrors.ustc.edu.cn" \
--service-cluster-ip-range='10.10.0.0/24'

minikube dashboard