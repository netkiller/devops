htpasswd -Bbn netkiller passw0rd > /var/lib/registry/passwd

docker run -d -p 5000:5000 --name registry \
--restart=always \
-v /var/lib/registry:/var/lib/registry \
-e REGISTRY_AUTH=htpasswd \
-e REGISTRY_AUTH_HTPASSWD_REALM=Registry_Realm \
-e REGISTRY_AUTH_HTPASSWD_PATH=/var/lib/registry/passwd \
registry:latest

docker run -d -p 5001:5001 --name registry-ui \
-e REGISTRY_HOST=registry.netkiller.cn \
-e REGISTRY_SSL=true \
-e REGISTRY_DOMAIN=registry.netkiller.cn \
-e REGISTRY_USER=netkiller \
-e REGISTRY_PASS=passw0rd \
jc21/registry-ui