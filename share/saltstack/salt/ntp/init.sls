ntp:
  pkg:
    - installed

  service:
    {% if grains['os'] == 'CentOS' or grains['os'] == 'RedHat' %}
    - name: ntpd
    {% endif %}
    - running
    - enable: True
  watch:
    - file: /etc/ntp.conf
  require:
    - pkg: ntp
