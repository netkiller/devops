FROM ubuntu:18.04

RUN apt-get update && apt-get install -y build-essential

# java 8
RUN apt-get install -y openjdk-8-jdk maven gradle

# maven central 镜像源
RUN cd /usr/share/maven/conf/ \
    && sed -i "/<mirrors>/a <mirror> \
        \n\t<id>nexus-tencentyun</id> \
        \n\t<mirrorOf>central</mirrorOf> \
        \n\t<name>Nexus tencentyun</name> \
        \n\t<url>https://mirrors.cloud.tencent.com/nexus/repository/maven-public/</url> \
        \n</mirror>" settings.xml

# gradle 全局镜像源
RUN mkdir -p ~/.gradle \
    &&  echo 'allprojects { \
                repositories { \
                    maven { \
                        url "https://mirrors.cloud.tencent.com/nexus/content/groups/public" \
                    } \
                } \
              }'  \
    > ~/.gradle/init.gradle
