FROM openjdk:8
VOLUME ["/srv"]
RUN apt update -y && apt install -y procps net-tools iputils-ping iproute2 telnet
EXPOSE 80 443
WORKDIR /srv
