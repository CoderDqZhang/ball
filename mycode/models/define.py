#-*- coding: UTF-8 -*-
import datetime
import pytz
import time
import json
import urllib.request

# MEDIAURL = 'https://yq.topveda.cn/media/'
MEDIAURL = 'http://127.0.0.1:8000/media/'

WEICHAT_APPID='wxc218fa7c51381f48'
WEICHAT_SECRET= 'a4d7d52fcc1fb3293c25245bdff07baf'

GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

GAME_STATUS = (
        (0, '过期'), #时间结束
        (1, '进行中'),
        (2, '失效'), #人数未满
        (3, '失败'), #人数未满
    )

UPDATA_USER_INFO = ['openid','nickname','age','gender',
                    'weight','height','game_age','phone',
                    'province','city','avatar','good_point',
                    'sign']

GET_USER_INFO = ['openid']

GET_USER_COMMOND = ['openid']

COMMOND_USER_INFO = ['openid','targid','content','userrank','skillrank']

WE_CHAT_LOGIN = ['code']

GET_GAME_LIST = ['ball_id']

GET_GAME_DETAIL = ['game_id','openid']

GET_GAME_APPLEMENT = ['game_id','openid','number_count']

GET_MY_GAME_APPLEMENT = ['openid']

CANCEL_MY_GAME_APPLEMENT = ['game_id','openid']

GET_GAME_LIST_KEYWORD = ['keyword','ball_id']

CREATE_GAME = ['game_title','game_subtitle','openid','ball_id','game_location','game_location_detail',
               'game_price','game_start_time','game_end_time','game_referee',
               'game_number','game_place_condition','number']

#时间戳转换
def timeStamp_to_date(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(float(timeStamp))
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime

def date_to_timeStamp(date):
    dtime = datetime.datetime.now()
    ans_time = time.mktime(dtime.timetuple())
    return ans_time

#请求返回数据整合
def response(status,code,msg = None,request_data = None):
    data = {}
    data['status'] = status
    data['code'] = code
    if msg is not None:
        data['msg'] = msg
    if request_data is not None:
        data['data'] = request_data
    return data

#请求验证是否成功
def request_verif(request_body,request_list):
    data = {}
    error = False
    data['errors'] = []
    jsonData = json.loads(request_body.body.decode('utf-8'))
    if request_body.method == 'POST':
        for p in request_list:
            print(p)
            if p not in jsonData:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True
    elif request_body.method == 'GET':
        for p in request_list:
            if p not in request_body.GET:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True

    if request_body.method == 'POST':
        return json.loads(request_body.body.decode('utf-8')), None
    if error:
        return None, data
    return request_body.GET, None

# def as_dict(models):
	    # dict = {}
	    # #exclude ManyToOneRel, which backwards to ForeignKey
	    # field_names = [field.name for field in models._meta.get_fields() if 'ImageField' not in str(field)]
	    # for name in field_names:
		 #    field_instance = getattr(self, name)
        # if field_instance.__class__.__name__ == 'ManyRelatedManager':
		 #    dict[name] = field_instance.all()
		 #    continue
        # dict[name] = field_instance
	    # return dict

def getaddress(address):
    address = urllib.request.quote(address)
    str = 'http://api.map.baidu.com/geocoder/v2/' \
          '?address='+ address +'&output=json&' \
          'ak=fBTBbXkPXNGR2jVxhLnGNpr94ZMw5zmc&callback=showLocation'
    data = urllib.request.urlopen(str)
    data1 = data.read()
    data2 = data1.decode("utf-8")
    data3 = data2.split(')')
    data4 = data3[0].split('(')
    JSON_DATA = json.loads(data4[1])
    print(JSON_DATA['result']['location'])
    return JSON_DATA['result']['location']


def getopenid(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?' \
          'appid='+WEICHAT_APPID+'&secret='+WEICHAT_SECRET+'&js_code='+code+'&grant_type=authorization_code'
    data = urllib.request.urlopen(url)
    data1 = data.read()
    JSON_DATA = json.loads(str(data1).replace("'","").replace('b',""))
    return JSON_DATA['openid']
