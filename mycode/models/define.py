#-*- coding: UTF-8 -*-

GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

def response(status,code,msg = None):
    data = {}
    data['status'] = status
    data['code'] = code
    if msg is not None:
        data['msg'] = msg
    return data