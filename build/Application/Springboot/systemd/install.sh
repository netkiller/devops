wget -q https://raw.githubusercontent.com/oscm/build/master/Application/Spring/systemd/spring.service -O /usr/lib/systemd/system/spring.service
systemctl enable spring
systemctl start spring