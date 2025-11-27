mkdir -p cert
openssl req -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key -x509 -days 365 -out certs/domain.crt

docker run -d -p 443:443 --name=registry --restart=always \
-v ./certs:/certs \
-e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \ 
-e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
registry:latest