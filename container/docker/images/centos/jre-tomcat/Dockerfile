############################################################
# Dockerfile to build Nginx container
# Based on centos7
############################################################

FROM centos:latest

MAINTAINER Netkiller <netkiller@msn.com>


#USER www
WORKDIR /srv

# Install EPEL
#RUN yum install -y epel-release

# Update RPM Packages
#RUN yum -y update 
RUN yum install -y wget
RUN yum clean all

# Install Server JRE
COPY server-jre-8u131-linux-x64.tar.gz /srv
#RUN ls /usr/local/src/ && curl -s https://raw.githubusercontent.com/oscm/shell/master/lang/java/server-jre-8u131-linux-x64.sh | bash 
RUN tar -zxf /srv/server-jre-8u131-linux-x64.tar.gz* && \
	ln -s /srv/jdk1.8.0_131 /srv/java && \
	rm -rf server-jre-8u131-linux-x64.tar.gz
# Install Tomcat
ENV CATALINA_HOME /srv/tomcat
ENV PATH $CATALINA_HOME/bin:$PATH
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

ENV TOMCAT_MAJOR 8
ENV TOMCAT_VERSION 8.5.15

#RUN curl -s https://raw.githubusercontent.com/oscm/shell/master/web/tomcat/8.5/apache-tomcat-8.5.15.sh | bash
ENV TOMCAT_TGZ_URL https://www.apache.org/dyn/closer.cgi?action=download&filename=tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz
RUN set -x \
	\
	&& wget -O tomcat.tar.gz "$TOMCAT_TGZ_URL" \
	&& tar -xvf tomcat.tar.gz --strip-components=1 \
	&& rm bin/*.bat \
	&& rm tomcat.tar.gz* \
	&& rm -rf $CATALINA_HOME/webapps/{docs,examples,manager,host-manager,ROOT/*} \
	&& rm -rf $CATALINA_HOME/logs/* \
	&& sed -i "16s/3manager.org.apache.juli.AsyncFileHandler, 4host-manager.org.apache.juli.AsyncFileHandler,//" $CATALINA_HOME/conf/logging.properties

ADD setenv.sh $CATALINA_HOME/bin

VOLUME $CATALINA_HOME/work
VOLUME $CATALINA_HOME/temp

# forward request and error logs to docker log collector
#RUN ln -sf /dev/stdout /var/log/nginx/access.log
#RUN ln -sf /dev/stderr /var/log/nginx/error.log

# be backwards compatible with pre-official images
#RUN ln -sf ../share/nginx /usr/local/nginx


# add startup script
#ADD startup.sh /root/startup.sh
#RUN chmod 755 /root/startup.sh

VOLUME $CATALINA_HOME/work
VOLUME $CATALINA_HOME/temp

EXPOSE 8080

CMD ["catalina.sh", "run"]
