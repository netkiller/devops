mysql-server:
  pkg:
    - installed
    - pkgs:
      - mysql-server
  service:
    - running
    - name: mysqld
    - enable: True
    - require:
      - pkg: mysql-server
#  mysql_user:
#    - present
#    - name: dba
#    - password: 'dba'
#    - require:
#      - service: mysqld
