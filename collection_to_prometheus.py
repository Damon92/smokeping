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
	'033'      	: '广西-南宁-58.59.152.1',
	'HBDQ-CTCC1'           : '河北-衡水-27.129.32.1',
'HBDQ-CTCC2'           : '河北-石家庄-27.128.190.1',
'HBDQ-CTCC3'           : '河北-邯郸市-27.128.214.131',
'HBDQ-CTCC4'           : '河北-张家口-106.8.128.69',
'HBDQ-CTCC5'           : '河北-承德市-106.112.38.8',
'HBDQ-CTCC6'           : '河北-秦皇岛-106.8.0.1',
'HBDQ-CTCC7'           : '河北-唐山市-27.128.173.15',
'HBDQ-CTCC8'           : '河北-廊坊市-27.189.0.1',
'HBDQ-CTCC9'           : '河北-保定-27.128.179.1',
'HBDQ-CTCC10'           : '河北-沧州-27.128.175.2',
'HBDQ-CTCC11'           : '河北-邢台市-111.226.160.1',
'HBDQ-CTCC12'           : '北京-1.119.204.3',
'HBDQ-CTCC13'           : '北京-1.202.0.5',
'HBDQ-CTCC14'           : '北京-36.110.36.6',
'HBDQ-CTCC15'           : '北京-45.116.152.6',
'HBDQ-CTCC16'           : '北京-49.7.0.11',
'HBDQ-CTCC17'           : '北京-106.0.4.10',
'HBDQ-CTCC18'           : '北京-43.248.112.19',
'HBDQ-CTCC19'           : '天津-36.106.2.1',
'HBDQ-CTCC20'           : '天津-42.122.0.1',
'HBDQ-CTCC21'           : '天津-42.81.181.11',
'HBDQ-CTCC22'           : '天津-115.168.33.129',
'HBDQ-CTCC23'           : '天津-221.238.2.1',
'HBDQ-CTCC24'           : '天津-219.150.66.25',
'HBDQ-CTCC25'           : '山西-临汾市-59.48.116.1',
'HBDQ-CTCC26'           : '山西-吕梁市-59.48.246.2',
'HBDQ-CTCC27'           : '山西-运城市-1.69.128.1',
'HBDQ-CTCC28'           : '山西-晋中市-1.69.0.1',
'HBDQ-CTCC29'           : '山西-太原市-59.49.3.121',
'HBDQ-CTCC30'           : '山西-大同市-113.24.216.13',
'HBDQ-CUCC1'           : '河北-衡水-60.9.44.1',
'HBDQ-CUCC2'           : '河北-石家庄-110.240.129.1',
'HBDQ-CUCC3'           : '河北-邯郸市-120.9.93.5',
'HBDQ-CUCC4'           : '河北-张家口-61.182.130.134',
'HBDQ-CUCC5'           : '河北-承德市-61.55.123.1',
'HBDQ-CUCC6'           : '河北-秦皇岛-60.7.0.1',
'HBDQ-CUCC7'           : '河北-唐山市-60.2.0.117',
'HBDQ-CUCC8'           : '河北-廊坊市-60.10.0.1',
'HBDQ-CUCC9'           : '河北-保定-60.4.3.1',
'HBDQ-CUCC10'           : '河北-沧州-61.55.71.2',
'HBDQ-CUCC11'           : '河北-邢台市-60.6.197.1',
'HBDQ-CUCC12'           : '北京-1.119.192.45',
'HBDQ-CUCC13'           : '北京-43.250.236.3',
'HBDQ-CUCC14'           : '北京-61.48.0.1',
'HBDQ-CUCC15'           : '北京-61.148.10.1',
'HBDQ-CUCC16'           : '北京-61.148.75.14',
'HBDQ-CUCC17'           : '北京-219.158.4.154',
'HBDQ-CUCC18'           : '天津-202.99.116.141',
'HBDQ-CUCC19'           : '天津-27.112.0.1',
'HBDQ-CUCC20'           : '天津-43.247.4.1',
'HBDQ-CUCC21'           : '天津-60.24.0.1',
'HBDQ-CUCC22'           : '天津-60.28.54.39',
'HBDQ-CUCC23'           : '天津-103.24.228.1',
'HBDQ-CUCC24'           : '天津-117.8.0.1',
'HBDQ-CUCC25'           : '天津-218.67.129.1',
'HBDQ-CUCC26'           : '天津-60.30.2.17',
'HBDQ-CUCC27'           : '山西-临汾市-60.221.0.2',
'HBDQ-CUCC28'           : '山西-吕梁市-118.77.154.1',
'HBDQ-CUCC29'           : '山西-运城市-60.222.0.1',
'HBDQ-CUCC30'           : '山西-太原市-61.134.198.1',
'HBDQ-CUCC31'           : '山西-大同市-121.30.44.1',
'HBDQ-CUCC32'           : '山西-太原市-43.249.236.1',
'HBDQ-CMCC1'           : '河北-衡水-39.134.192.1',
'HBDQ-CMCC2'           : '河北-石家庄-111.11.85.65',
'HBDQ-CMCC3'           : '河北-邯郸市-39.134.192.193',
'HBDQ-CMCC4'           : '河北-张家口-39.134.192.1',
'HBDQ-CMCC5'           : '河北-承德市-39.134.192.34',
'HBDQ-CMCC6'           : '河北-秦皇岛-39.134.195.1',
'HBDQ-CMCC7'           : '河北-唐山市-111.11.92.1',
'HBDQ-CMCC8'           : '河北-廊坊市-39.144.49.48',
'HBDQ-CMCC9'           : '河北-保定-39.134.194.1',
'HBDQ-CMCC10'           : '河北-沧州-39.137.95.177',
'HBDQ-CMCC11'           : '河北-邢台市-39.134.190.242',
'HBDQ-CMCC12'           : '北京-36.132.0.5',
'HBDQ-CMCC13'           : '北京-39.134.133.1',
'HBDQ-CMCC14'           : '北京-111.13.0.185',
'HBDQ-CMCC15'           : '北京-42.83.201.1',
'HBDQ-CMCC16'           : '北京-39.156.118.1',
'HBDQ-CMCC17'           : '北京-223.71.37.1',
'HBDQ-CMCC18'           : '北京-223.70.163.10',
'HBDQ-CMCC19'           : '天津-39.134.140.1',
'HBDQ-CMCC20'           : '天津-111.30.0.15',
'HBDQ-CMCC21'           : '天津-111.161.120.1',
'HBDQ-CMCC22'           : '天津-117.131.129.1',
'HBDQ-CMCC23'           : '天津-211.103.81.57',
'HBDQ-CMCC24'           : '山西-临汾市-39.134.27.1',
'HBDQ-CMCC25'           : '山西-吕梁市-39.137.20.16',
'HBDQ-CMCC26'           : '山西-运城市-211.142.95.65',
'HBDQ-CMCC27'           : '山西-太原市-211.138.99.14',
'HBDQ-CMCC28'           : '山西-大同市-111.53.0.1'
	
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
#    ISP_list = ['TELCOM' , 'WY' , 'HNDQ']
    ISP_list = ['TELCOM' , 'UNICOM' , 'CMCC' ,'WY' , 'HNDQ','HBDQ-CTCC','HBDQ-CUCC','HBDQ-CMCC']
    for ISP in ISP_list:
        rrd_data_dir = os.path.join(paras["data_dir"], ISP)
        for filename in os.listdir(rrd_data_dir):
            (instance , postfix) = os.path.splitext(filename)
            if postfix == '.rrd' :
                (lost_package_num , rrt) = getMonitorData(os.path.join(paras["data_dir"] , ISP , filename))
                pushMetrics(instance , ISP , 'rrt' , rrt)
                pushMetrics(instance , ISP , 'lost_package_num' , lost_package_num)
