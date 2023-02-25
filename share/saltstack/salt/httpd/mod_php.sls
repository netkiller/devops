include:
  - httpd

php:
  pkg:
    - installed
  service:
    - name: httpd
    - reload: True
