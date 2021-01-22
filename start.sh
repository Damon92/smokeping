#/bin/sh
systemctl start prometheus
systemctl start pushgateway
systemctl start crond
service grafana-server start
/usr/local/smokeping/bin/smokeping
echo "* * * * * python /usr/local/smokeping/collection_to_prometheus.py" >> /var/spool/cron/root
mv /etc/localtime /etc/localtime.bak
cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
