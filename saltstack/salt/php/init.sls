
php:
  pkg:
   - installed
   - require_in: 
   - service: apache2
  cmd:
    - run: a2enmod php5
    - require: 
    pkg: php
