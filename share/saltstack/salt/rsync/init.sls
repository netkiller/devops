rsync:
  pkg:
    - installed
  service:
    - name: rsync
    - running
    - enable: True
    - file: /etc/rsyncd.conf
    - file: /etc/rsyncd.passwd
    - file: /etc/init.d/rsync

/etc/init.d/rsync:
  file:
    - managed
    - user: root
    - group: root
    - mode: 700
    - source: salt://rsync/rsync
  cmd.run:
    - unless: chkconfig --add rsync
    

/etc/rsyncd.conf:
  file:
    - managed
    - user: root
    - group: root
    - mode: 600
    - name: /etc/rsyncd.conf
    - source: salt://rsync/rsyncd.conf

/etc/rsyncd.passwd:
  file:
    - managed
    - user: root
    - group: root
    - mode: 600
    - source: salt://rsync/rsyncd.passwd
