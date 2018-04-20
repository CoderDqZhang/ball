#-*- coding: UTF-8 -*-
import datetime
import pytz
import time
import json

MEDIAURL = 'http://127.0.0.1:8000/media/'

GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

UPDATA_USER_INFO = ['openid','nickname','age','gender',
                    'weight','height','game_age','phone',
                    'province','city','avatar','good_point']

GET_USER_INFO = ['openid']

GET_USER_COMMOND = ['openid']

COMMOND_USER_INFO = ['openid','targid','content','rank']

GET_GAME_LIST = ['ball_id']

GET_GAME_DETAIL = ['game_id']

GET_GAME_APPLEMENT = ['game_id','openid','number_count']

GET_MY_GAME_APPLEMENT = ['openid']

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
