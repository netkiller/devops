FROM openjdk:latest
VOLUME ["/opt/netkiller","/app"]
RUN apt update -y && apt install -y procps
EXPOSE 80 443
WORKDIR /opt
COPY index.html /var/www
