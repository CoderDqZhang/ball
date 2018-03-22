#-*- coding: UTF-8 -*-

GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

UPDATA_USER_INFO = ['openid','nickname','age','gender',
                    'weight','height','ball_age','phone',
                    'province','city','avatar']

def response(status,code,msg = None,request_data = None):
    data = {}
    data['status'] = status
    data['code'] = code
    if msg is not None:
        data['msg'] = msg
    if data is not None:
        data['data'] = request_data
    return data

def request_verif(request_body,request_list):
    data = {}
    error = False
    data['errors'] = []
    for p in request_list:
        if p not in request_body.POST:
            data['errors'].append({"参数错误":p+"未传值"})
            error = True
    if error:
        return data
    return
