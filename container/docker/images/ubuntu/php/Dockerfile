FROM ubuntu:18.04

RUN apt-get update && apt-get install -y build-essential

# RUN apt upgrade 
RUN apt install -y --allow-downgrades ca-certificates apt-transport-https
RUN apt update && apt install -y php7.2 && apt install -y php7.2-cgi php7.2-cli php7.2-dev php7.2-common php7.2-curl  php7.2-imap php7.2-json php7.2-mbstring php7.2-mysql php7.2-xml php7.2-zip php7.2-opcache

RUN wget https://dl.laravel-china.org/composer.phar -O /usr/local/bin/composer \
  && chmod a+x /usr/local/bin/composer \
  && composer config -g repo.packagist composer https://packagist.laravel-china.org


ENV PATH /home/jenkins/.composer/vendor/bin/:$PATH

RUN composer config -g repo.packagist composer https://packagist.phpcomposer.com
