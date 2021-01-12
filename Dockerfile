From centos:7.4.1708
MAINTAINER Damon.Dai daikaiguo@rayvision.com
RUN yum -y install epel-release
RUN (yum install git vixie-cron crontabs wget fping gcc make python-pip python-rrdtool rrdtool perl-rrdtool openssl openssl-devel -y ;\
     yum install perl-Sys-Syslog perl-Module-CoreList perl-ExtUtils-Manifest \
                 perl-Digest-MD5 perl-IPC-Cmd -y ;\
     yum install perl-CPAN perl-Sys-Syslog perl-Module-CoreList perl-CGI \
                 perl-Digest-MD5 perl-Digest-HMAC perl-Test-NoWarnings \
                 perl-Test-Deep perl-Test-Warn perl-CPAN-Meta perl-Module-Build \
                 perl-Test-RequiresInternet perl-URI -y)
#RUN wget https://oss.oetiker.ch/smokeping/pub/smokeping-2.6.11.tar.gz
RUN wget https://oss.oetiker.ch/smokeping/pub/smokeping-2.7.1.tar.gz
RUN tar -zxvf smokeping-2.7.1.tar.gz
RUN cd smokeping-2.7.1 && ./configure --prefix=/usr/local/smokeping && make && make install
RUN cd /usr/local/smokeping && mkdir -p data cache var
RUN chmod -R 755 /usr/local/smokeping
RUN chmod 600 /usr/local/smokeping/etc/smokeping_secrets.dist
RUN git clone https://github.com/Damon92/smokeping.git
RUN cp -rf smokeping/collection_to_prometheus.py /usr/local/smokeping/ 
RUN cp -rf smokeping/location /usr/local/smokeping/etc/
RUN cp -rf smokeping/config /usr/local/smokeping/etc/
RUN curl -s https://packagecloud.io/install/repositories/prometheus-rpm/release/script.rpm.sh | bash
RUN yum -y install prometheus
RUN yum -y install pushgateway
RUN yum -y install https://dl.grafana.com/oss/release/grafana-7.3.6-1.x86_64.rpm 
RUN cp -rf smokeping/prometheus.yml /etc/prometheus/
EXPOSE 3000 9090
RUN cp -rf smokeping/start.sh /usr/local/sbin/start.sh
CMD [ "sh", "/usr/local/sbin/start.sh"]
