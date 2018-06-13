from mycode.utils import network,TLS
from mycode.models.account import IM
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms.models import model_to_dict
from mycode.models.account import Account,Commond
from mycode.ball_views import tencent_im
from django.db.models import Q
from .checkuser import checkdata
import logging
from mycode.models import define
from mycode.models.serializers import AccountSerializer
import json
import sys
import importlib
importlib.reload(sys)

import random

sdkappid = 1400098651
def create_group(group_name,openid):
    usersig =  TLS.main(sdkappid,openid)
    ran = str(random.randint(1,999999999))
    url = "https://console.tim.qq.com/v4/group_open_http_svc/create_group?" \
          "usersig="+usersig.decode()+"&identifier="+openid+"&" \
          "sdkappid="+str(sdkappid)+"&random="+str(ran)+"&contenttype=json"
    values ={
        "Type": "AVChatRoom", # 群组类型：Private / Public / ChatRoom(不支持AVChatRoom和BChatRoom)（必填）
        "Name": group_name # 群名称（必填）
    }
    return network.request_post(url,values)

def sender_msg(openid):
    usersig = TLS.main(sdkappid, openid)
    ran = str(random.randint(1, 999999999))
    url = "https://console.tim.qq.com/v4/group_open_http_svc/send_group_msg?" \
          "usersig="+usersig.decode()+"&identifier="+openid+"&" \
          "sdkappid="+str(sdkappid)+"&random="+str(ran)+"&contenttype=json"
    values = {
        "GroupId": "@TGS#a72JQCIFF",
        "Random": random.randint(1, 999999999),
        "MsgBody": [ {
            "MsgType": "TIMTextElem",
            "MsgContent": {
                "Text": "red packet"
            }},
            {
            "MsgType": "TIMFaceElem",
            "MsgContent": {
                "Index": 6,
                "Data": "abc\u0000\u0001"
            }
        }]}
    return network.request_post(url, values)

def sender_image(openid):
    usersig = TLS.main(sdkappid, openid)
    ran = str(random.randint(1, 999999999))
    url = "https://console.tim.qq.com/v4/group_open_http_svc/send_group_msg?" \
          "usersig="+usersig.decode()+"&identifier="+openid+"&" \
          "sdkappid="+str(sdkappid)+"&random="+str(ran)+"&contenttype=json"
    values = {
        "GroupId": "@TGS#a72JQCIFF",
        "Random": random.randint(1, 999999999),
        "MsgBody": [ {
            "MsgType": "TIMImageElem",
            "MsgContent": {
                "UUID": "1853095_D61040894AC3DE44CDFFFB3EC7EB720F",
                "ImageFormat": 1,
                "ImageInfoArray": [
                {
                    "Type": 1,
                    "Size": 1853095,
                    "Width": 2448,
                    "Height": 3264,
                    "URL": "https://timgsa.baidu.com/timg?image&quality=80"
                           "&size=b9999_10000&sec=1529029128&di=686b2af48150493488441ea9a83c934b&imgtype=jpg"
                           "&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F016c4f5721807732f875a3992ba4d6.jpg"
                }
            ]
            },
        }]}
    return network.request_post(url, values)

def game_create_group(game):
    room = create_group('game-'+str(game.id), 'admin')
    im = IM.objects.create(
        room = room['GroupId']
    )
    im.game = game
    im.save()

def game_club_create_group(game_club):
    room = create_group('game_club-'+str(game_club.id), 'admin')
    im = IM.objects.create(
        room = room['GroupId']
    )
    im.game_club = game_club
    im.save()

def get_im_group_id(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_IM_GROUP_ID)
        if checkrequest is None:
            game_id = body['game_id']
            club_id = body['club_id']
            im = IM.objects.get(Q(game_club_id=club_id) | Q(game_id=game_id))
            data = {}
            if im is None:
                return JsonResponse(define.response("success", 0, "群组不存在"))
            else:
                data = model_to_dict(im)
                return JsonResponse(define.response("success", 0, None, request_data=data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);


