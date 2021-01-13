#coding:utf-8
import requests
import rrdtool
import os
import logging
import logging.handlers


paras = {
    'province_map' : {
	'foshan'	: '佛山' ,
	'nanning'	: '南宁' ,
        'anhui'         : '安徽' ,
        'beijing'       : '北京' ,
        'chongqing'     : '重庆' ,
        'fujian'        : '福建' ,
        'gansu'         : '甘肃' ,
        'guangdong'     : '广东' ,
        'guangxi'       : '广西' ,
        'guizhou'       : '贵州' ,
        'hainan'        : '海南' ,
        'hebei'         : '河北' ,
        'heilongjiang'  : '黑龙江' ,
        'henan'         : '河南' ,
        'hubei'         : '湖北' ,
        'hunan'         : '湖南' ,
        'jiangsu'       : '江苏' ,
        'jiangxi'       : '江西' ,
        'jilin'         : '吉林' ,
        'liaoning'      : '辽宁' ,
        'neimenggu'     : '内蒙古' ,
        'ningxia'       : '宁夏' ,
        'qinghai'       : '青海' ,
        'shaanxi'       : '陕西' ,
        'shandong'      : '山东' ,
        'shanghai'      : '上海' ,
        'shanxi'        : '山西' ,
        'shenzhen'      : '深圳' ,
        'sichuan'       : '四川' ,
        'tianjin'       : '天津' ,
        'xinjiang'      : '新疆' ,
        'xizang'        : '西藏' ,
        'yunnan'        : '云南' ,
        'zhejiang'      : '浙江' ,	
        'wy001'   	: '杭州BGP-42.186.120.168' ,
        'wy002'   	: '杭州BGP-42.186.125.162' ,
        'wy003'     	: '杭州BGP-106.2.94.76' ,
        'wy004'      	: '杭州BGP-123.58.180.7',
        'wy005'      	: '杭州BGP-59.111.0.1' ,
        'wy006'      	: '北京BGP-103.72.12.129' ,
        'wy007'      	: '广州BGP-114.113.196.1' ,
        'wy009'      	: '北京BGP-45.254.64.1' ,
        'wy010'      	: '杭州BGP-114.113.196.1' ,
        'wy008'      	: '杭州BGP-223.252.192.1' ,
	'001'     	: '广东-广州-113.108.208.170',
	'002'      	: '广东-广州-61.144.2.18',
	'003'      	: '广东-广州-183.60.187.43',
	'004'      	: '广东-广州-14.18.236.1',
	'005'      	: '广东-佛山-119.38.130.1',
	'006'      	: '广东-骨干-202.97.25.181',
	'007'      	: '广东-睿江-121.201.121.140',
	'008'      	: '广东-睿江-121.201.121.141',
	'009'     	: '广东-惠州-14.112.17.80',
	'010'      	: '广东-梅州-116.16.13.17',
	'011'      	: '广东-中山-14.114.34.255',
	'012'      	: '广东-湛江-183.0.16.1',
	'013'      	: '广东-深圳-58.60.0.25',
	'014'      	: '广东-清远-183.57.61.137',
	'015'      	: '广东-汕尾-119.134.250.3',
	'016'      	: '广东-珠海-61.145.231.164',
	'017'      	: '广东-东莞-119.128.50.1',
	'018'      	: '广东-韶关-14.144.27.254',
	'019'      	: '广东-河源-59.32.29.1',
	'020'      	: '广东-汕头-218.16.205.146',
	'021'      	: '广东-肇庆-14.148.126.54',
	'022'      	: '广东-江门-119.146.173.154',
	'023'      	: '广东-茂名-14.148.97.14',
	'024'      	: '广东-阳江-125.90.104.21',
	'025'      	: '广东-清远-183.57.61.66',
	'026'      	: '广东-潮州-183.7.190.29',
	'027'      	: '广东-揭阳-183.7.189.45',
	'028'      	: '广东-云浮-14.148.111.14',
	'029'      	: '海南-文昌-218.77.141.98',
	'030'      	: '海南-电信-218.77.136.254',
	'031'      	: '广西-北海-171.104.80.1',
	'032'      	: '广西-南宁-218.65.143.154',
	'033'      	: '广西-南宁-58.59.152.1'
    } , 
    'LOG_FILE' : '/usr/local/smokeping/smoking_pushgateway.log' , 
    'prometheus_gateway' : 'http://localhost:9091' , 
    'data_dir' : '/usr/local/smokeping/data'
}

class LogHandler(object):
    def __init__(self, name):
        self.handler = logging.handlers.RotatingFileHandler(paras['LOG_FILE'] , maxBytes = 1024*1024 , backupCount = 5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        self.handler.setFormatter(formatter)
        self.logger = logging.getLogger(name)
        self.logger.addHandler(self.handler)

    def __call__(self , func , *args , **kwargs):
        if func.__name__ == 'info' :
            self.logger.setLevel(logging.INFO)
            log_record = func(*args , **kwargs)
            self.logger.info(log_record)
            self.logger.removeHandler(self.handler)


def pushMetrics(instance , ISP , key , value):
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    pushgateway = '%s/metrics/job/smokeping-collected-%s/instance/%s' % (paras['prometheus_gateway'] , ISP , instance)
    metrics = 'smokeping_%s{instance=\"%s\" , ISP=\"%s\" , IDC=\"%s\" , alias=\"%s\"} %d' % (key , instance , ISP , 'SH' , paras['province_map'].get(instance) , value)
    request_code = requests.post(pushgateway , data='{0}\n'.format(metrics) , headers=headers)
    @LogHandler(pushgateway)
    def info():
        return metrics + ' - ' + str(request_code.status_code)

def getMonitorData(rrd_file): 
    rrd_info = rrdtool.info(rrd_file)
    last_update = rrd_info['last_update'] - 60
    args = '-s ' + str(last_update) 
    results = rrdtool.fetch(rrd_file , 'AVERAGE' , args )
    lost_package_num = int(results[2][0][1])
    average_rrt = 0 if not results[2][0][2] else results[2][0][2] * 1000
    return lost_package_num , round(average_rrt , 4)


if __name__ == '__main__':
    ISP_list = ['TELCOM' , 'WY' , 'HNDQ']
    for ISP in ISP_list:
        rrd_data_dir = os.path.join(paras["data_dir"], ISP)
        for filename in os.listdir(rrd_data_dir):
            (instance , postfix) = os.path.splitext(filename)
            if postfix == '.rrd' :
                (lost_package_num , rrt) = getMonitorData(os.path.join(paras["data_dir"] , ISP , filename))
                pushMetrics(instance , ISP , 'rrt' , rrt)
                pushMetrics(instance , ISP , 'lost_package_num' , lost_package_num)
