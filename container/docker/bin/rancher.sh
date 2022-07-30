docker run -d --name rancher --restart=unless-stopped -p 80:80 -p 443:443 \
-v /var/lib/rancher/:/var/lib/rancher/ rancher/rancher:stable