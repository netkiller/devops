############################################################
# Dockerfile to build Nginx container
# Based on centos7
############################################################

FROM centos:latest

MAINTAINER Netkiller <netkiller@msn.com>

#USER www
#WORKDIR /www

# Install EPEL
RUN yum install -y epel-release && yum clean all

# Update RPM Packages
RUN yum -y update

# Install Nginx
RUN rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
RUN yum install -y nginx
RUN yum clean all

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

# be backwards compatible with pre-official images
#RUN ln -sf ../share/nginx /usr/local/nginx

# prepare container
#ADD prepare.sh /prepare.sh
#RUN chmod 755 /prepare.sh
#RUN /prepare.sh

# add startup script
ADD startup.sh /root/startup.sh
RUN chmod 755 /root/startup.sh

#VOLUME ["/etc/nginx"]
#VOLUME ["/usr/share/nginx/html"]
#VOLUME ["/var/www"]

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
#CMD /startup.sh
