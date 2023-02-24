base:  
  '*':
    - ntp
    - iptables
  'os:(RedHat|CentOS)':
    - match: grain_pcre
    - repos.epel
    - common.centos
  'os:Ubuntu':
    - common.ubuntu	
  'www':
    - nginx
    - php.php-fpm
  'mysql':
    - mysql
