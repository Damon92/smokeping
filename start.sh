#/bin/sh
systemctl start prometheus
systemctl start pushgateway
service grafana-server start
/usr/local/smokeping/bin/smokeping
