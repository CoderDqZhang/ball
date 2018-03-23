#-*- coding: UTF-8 -*-
import datetime
import pytz

GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

UPDATA_USER_INFO = ['openid','nickname','age','gender',
                    'weight','height','ball_age','phone',
                    'province','city','avatar']

GET_USER_INFO = ['openid']

GET_GAME_LIST = ['ball_id']

CREATE_GAME = ['openid','ball_id','game_location','game_location_detail',
               'game_price','game_start_time','game_end_time','game_referee',
               'game_number','game_place_condition']

#时间戳转换
def timeStamp_to_date(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(float(timeStamp))
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")

    return otherStyleTime

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

    if request_body.method == 'POST':
        for p in request_list:
            if p not in request_body.POST:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True
    elif request_body.method == 'GET':
        for p in request_list:
            if p not in request_body.GET:
                data['errors'].append({"参数错误":p+"未传值"})
                error = True
    if error:
        return data
    return
