docker pull gitlab/gitlab-ce

--rm --detach \
--hostname gitlab.netkiller.cn \
--restart always \
 --publish 22:22

docker container rm gitlab
docker run --name gitlab --rm \
--publish 443:443 --publish 80:80 \
--volume /opt/gitlab/config:/etc/gitlab \
--volume /opt/gitlab/logs:/var/log/gitlab \
--volume /opt/gitlab/data:/var/opt/gitlab \
gitlab/gitlab-ce:latest