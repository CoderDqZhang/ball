#-*- coding: UTF-8 -*-
import datetime
import pytz
import time
import json
import urllib.request
import uuid
from mycode.models import errors

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

if (get_mac_address() == '00:50:56:82:19:40') :
    print(get_mac_address())
    MEDIAURL = 'https://yq.topveda.cn/media/'
else:
    print(get_mac_address())
    MEDIAURL = 'http://127.0.0.1:8000/media/'

#微信小程序app-id/secret
WEICHAT_APPID='wxc218fa7c51381f48'
WEICHAT_SECRET= 'a4d7d52fcc1fb3293c25245bdff07baf'



GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )


# CLUB_GAMES = (
#         (1, '比赛'),
#         (2, '娱乐'),
#         (0, '聚餐')
#     )

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

COMMOND_USER_INFO = ['openid','targid','content','userrank','skillrank','anonymity']

WE_CHAT_LOGIN = ['code']

GET_GAME_LIST = ['ball_id']

GET_GAME_DETAIL = ['game_id','openid']

GET_GAME_APPLEMENT = ['game_id','openid','number_count']

GET_MY_GAME_APPLEMENT = ['openid']

DELETE_GET_MY_GAME_APPLEMENT = ['game_id','openid']

CANCEL_MY_GAME_APPLEMENT = ['game_id','openid']

GET_GAME_LIST_KEYWORD = ['keyword','ball_id']

CREATE_GAME = ['game_title','game_subtitle','openid','ball_id','game_location','game_location_detail',
               'game_price','game_start_time','game_end_time','game_referee',
               'game_number','game_place_condition','number','lat','lng']


GET_CLUB_CREATE = ['openid','club_slogan','club_desc','club_title','club_post','club_grade'
                   ,'club_project','club_number','ball_id']

MY_GAME_CLUB_LIST = ['openid']

MY_GAME_CLUB_DETAIL = ['openid','club_id']

UNREAD_MESSAGE = ['openid','tag_openid','message_type']

INVETE_MESSAGE = ['club_id','tag_openid','message_type']

UNREAD_MESSAGE_CLUN_MANAGER = ['openid','club_id','message_type']

UNREAD_MESSAGE_USER = ['openid']

LEAVE_GAME_CLUB = ['openid','club_id']

DISSOLVE_GAME_CLUB = ['openid','club_id']

CHANGE_CLUB_USER = ['status','unread_id']

UPLOAD_CLUB_IMAGE = ['openid','club_id','content','file']

INVETE_GAME_CLUB_USER = ['openid','club_id','game_id','message_type']

CREATE_GAME_REPORT = ['openid','club_idA','club_idB','game_id']

GAME_CLUB_REPORT_LIST = []

GAME_CLUB_REPORT_DETAIL = ['game_report_id']
#时间戳转换
def timeStamp_to_date(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(float(timeStamp))
    dateArray = dateArray + datetime.timedelta(hours=8)
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
        data['message'] = msg
    if request_data is not None:
        data['data'] = request_data
    return data

def check_request_data(request_body,request_list):
    return

#请求验证是否成功
def request_verif(request_body,request_list):
    data = {}
    error = False
    data['errors'] = []
    if len(request_list) != 0:
        print(len(request_list))
        try:
            jsonData = json.loads(request_body.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            error = True
            data['errors'].append({"参数错误": "未传值"})
            return None,data
        except:
            return  None,data['errors'].append({"error":"error"})
    else:
        return request_body, None
    if request_body.method == 'POST':
        for p in request_list:
            if p not in jsonData:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True
            else:
                if (jsonData[p] == None):
                    data['errors'].append({'error':errors.ERRORS[p]})
                    error = True
    elif request_body.method is 'GET':
        for p in request_list:
            if p not in request_body.GET:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True

    if error:
        return None, data
    if request_body.method == 'POST':
        return json.loads(request_body.body.decode('utf-8')), None
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
