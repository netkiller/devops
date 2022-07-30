docker pull gitlab/gitlab-ce

sudo docker run --detach \
--hostname gitlab.netkiller.cn \
--publish 443:443 --publish 80:80 --publish 22:22 \
--name gitlab \
--restart always \
--volume ~/gitlab/config:/etc/gitlab \
--volume ~/gitlab/logs:/var/log/gitlab \
--volume ~/gitlab/data:/var/opt/gitlab \
gitlab/gitlab-ce:latest