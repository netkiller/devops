FROM centos:latest

MAINTAINER Netkiller <netkiller@msn.com>

ENV CATALINA_HOME /srv/tomcat
ENV PATH $CATALINA_HOME/bin:$PATH
RUN mkdir -p "$CATALINA_HOME"
WORKDIR $CATALINA_HOME

RUN yum install -y java-1.8.0-openjdk wget

ENV TOMCAT_MAJOR 8
ENV TOMCAT_VERSION 8.5.15

# https://issues.apache.org/jira/browse/INFRA-8753?focusedCommentId=14735394#comment-14735394
ENV TOMCAT_TGZ_URL https://www.apache.org/dyn/closer.cgi?action=download&filename=tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz
# not all the mirrors actually carry the .asc files :'(
ENV TOMCAT_ASC_URL https://www.apache.org/dist/tomcat/tomcat-$TOMCAT_MAJOR/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz.asc

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
	
EXPOSE 8080
CMD ["catalina.sh", "run"]
