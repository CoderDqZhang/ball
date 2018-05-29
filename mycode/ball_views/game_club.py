# coding=utf-8
from django.http import JsonResponse
from mycode.models import define
import logging
from django.forms.models import model_to_dict
from mycode.models.account import Account,GameClub,Ball,UnreadMessage
from django.core import serializers
import json
from django.utils import timezone
import datetime
from django.db.models import Q
import sys
import importlib
importlib.reload(sys)
from django.core.files.base import ContentFile

# def upload_image(request):

## message_type == 0 申请入群   message_type == 1 申请成为管理员 message_type == 2 邀请入群

def create_game_club(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.GET_CLUB_CREATE)
            if checkrequest is None:
                openid = body.get('openid')
                ball_id = body.get('club_ball')
                print(body)
                user = Account.objects.get(openid=openid)
                ball = Ball.objects.get(id=ball_id)
                data = {}
                club_post = request.FILES.get("club_post", None)
                file_content = ContentFile(request.FILES.get('club_post').read())
                game_club = GameClub.objects.create(
                    club_number = body.get('club_number'),
                    club_project = body.get('club_project'),
                    club_grade=body.get('club_grade'),
                    club_title = body.get('club_title'),
                    club_desc=body.get('club_desc'),
                    club_slogan=body.get('club_slogan'),
                )
                game_club.club_ball.add(ball)
                game_club.club_post.save(request.FILES.get('club_post').name,file_content)
                print(request.FILES.get('club_post').name)
                response = model_to_dict(game_club, exclude=['user',
                                                                   'club_manager','club_user','club_post'])
                game_club.user.add(user)
                game_club.club_manager.add(user)
                response['club_post'] =  define.MEDIAURL + request.FILES.get('club_post').name
                response['create_user'] = model_to_dict(user)
                data['game_club'] = response
                return JsonResponse(define.response("success", 0, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def club_game_detail(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.MY_GAME_CLUB_DETAIL)
            if checkrequest is None:
                club_id = body['club_id']
                data = {}
                response = {}
                club = GameClub.objects.get(id=club_id)
                data['club'] = returngame_club(club,body['openid'])
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def my_game_club_list(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.MY_GAME_CLUB_LIST)
            if checkrequest is None:
                openid = body['openid']
                user = Account.objects.get(openid=openid)
                data = {}
                response = {}
                data['club_list'] = []
                club_list = GameClub.objects.all().filter(Q(user__openid__exact=openid)|
                                                          Q(club_manager__openid__exact=openid)|
                                                          Q(club_user__openid__exact=openid))
                for x in club_list:
                    data['club_list'].append(returngame_club(x))
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def invate_club(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.INVETE_MESSAGE)
            if checkrequest is None:
                club_id = body['club_id']
                tag_openid = body['tag_openid']
                message_type = body['message_type']
                tag_user = Account.objects.get(openid=tag_openid)
                clubs = GameClub.objects.get(id=club_id)
                user = Account.objects.get(openid=clubs.user.first().openid)
                tag_user = Account.objects.get(openid=tag_openid)
                data = {}
                response = {}
                unread = UnreadMessage.objects.create(
                    message_type=body['message_type'],
                    message_type_desc='邀请入群',
                    read_flag=0
                )
                unread.user_openid.add(user)
                unread.tag_user_openid.add(tag_user)
                unread.unread_club.add(clubs)
                data["message"] = "邀请成功"
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

#申请入群
def apply_club(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.UNREAD_MESSAGE)
            if checkrequest is None:
                openid = body['openid']
                tag_openid = body['tag_openid']
                message_type = body['message_type']
                unread_club = body['unread_club']

                tag_user = Account.objects.get(openid=tag_openid)
                user = Account.objects.get(openid=openid)

                data = {}
                response = {}
                unread = UnreadMessage.objects.create(
                    message_type=body['message_type'],
                    message_type_desc='申请入群',
                    read_flag=0
                )
                print(unread_club)
                unread.user_openid.add(user)
                unread.tag_user_openid.add(tag_user)
                print(GameClub.objects.get(id=unread_club))
                unread.unread_club.add(GameClub.objects.get(id = unread_club))
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

#申请成为管理员
def apply_club_manager(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.UNREAD_MESSAGE_CLUN_MANAGER)
            if checkrequest is None:
                openid = body['openid']
                message_type = body['message_type']
                club_id = body['club_id']
                clubs = GameClub.objects.get(id=club_id)
                user = Account.objects.get(openid=openid)
                tag_user = Account.objects.get(openid=clubs.user.first().openid)
                data = {}
                response = {}
                unread = UnreadMessage.objects.create(
                    message_type=body['message_type'],
                    message_type_desc='申请成为管理员',
                    read_flag=0
                )
                unread.user_openid.add(user)
                unread.tag_user_openid.add(tag_user)
                unread.unread_club.add(clubs)
                data["message"] = "申请成功"
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

#退出俱乐部
def leave_game_club(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.LEAVE_GAME_CLUB)
            if checkrequest is None:
                openid = body['openid']
                club_id = body['club_id']
                clubs = GameClub.objects.get(id=club_id)
                clubs.club_manager.filter(openid__exact=openid).delete()
                clubs.club_user.filter(openid__exact=openid).delete()
                data = {}
                response = {}
                data["message"] = "退出成功"
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

#解散俱乐部
def dissolve_game_club(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.LEAVE_GAME_CLUB)
            if checkrequest is None:
                data = {}
                response = {}
                openid = body['openid']
                club_id = body['club_id']
                clubs = GameClub.objects.get(id=club_id)
                ret = clubs.club_user.filter(openid__exact=openid)
                if ret.count() > 0:
                    data["message"] = "解散成功"
                    clubs.delete()
                    return JsonResponse(define.response("success", 0, request_data=data))
                data["message"] = "解散失败"
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def club_status(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.CHANGE_CLUB_USER)
            if checkrequest is None:
                unread_id = body['unread_id']
                status = body['status']
                data = {}
                response = {}
                unread = UnreadMessage.objects.get(id=unread_id)
                #申请目标
                tag_user = Account.objects.get(openid=unread.tag_user_openid.first().openid)
                #申请人
                user = Account.objects.get(openid=unread.user_openid.first().openid)
                unread.read_flag = 1
                unread.save()
                if status == 1:
                    #申请加入俱乐部
                    if unread.message_type == 0:
                        club = GameClub.objects.get(id=unread.unread_club.first().id)
                        club.club_user.add(user)
                        data['message'] = '加入成功'
                    elif unread.message_type == 1:
                        club = GameClub.objects.get(id=unread.unread_club.first().id)
                        club.club_manager.add(user)
                        data['message'] = '加入成功'
                    elif unread.message_type == 2:
                        club = GameClub.objects.get(id=unread.unread_club.first().id)
                        club.club_user.add(tag_user)
                        data['message'] = '加入成功'
                    return JsonResponse(define.response("success", 0, request_data=data))
                else:
                    data["message"] = '拒绝入群'
                    return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def unread_message(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.UNREAD_MESSAGE_USER)
            if checkrequest is None:
                openid = body['openid']
                data = {}
                data['unread_message'] = []
                unread = UnreadMessage.objects.filter(Q(tag_user_openid__exact=openid) & Q(read_flag__exact=0))
                print(unread)
                for x in unread:
                    response = model_to_dict(x, exclude=['user_openid', 'tag_user_openid', 'unread_club',
                                                         'unread_game'])
                    if x.user_openid.all().count() == 0:
                        data['message'] = '出现错误'
                        return JsonResponse(define.response("success", 0, request_data=data))
                    print(x.user_openid.all())
                    response['user'] = model_to_dict(Account.objects.get(openid=x.user_openid.first().openid))
                    response['tag_user'] = model_to_dict(Account.objects.get(openid=openid))
                    print(x.unread_club)
                    if x.message_type == 0 or x.message_type == 1 or x.message_type == 2:
                        response['unread_club'] = returngame_club(x.unread_club.first())
                    elif x.message_type == 2:
                        response['unread_game'] = model_to_dict(x.unread_game.first(),exclude=['game_create_user','game_detail',
                                                                                    'game_user_list'])
                    data['unread_message'].append(response)
                return JsonResponse(define.response("success", 0, request_data = data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);



def returngame_club(data,openid = None):
    response = model_to_dict(data, exclude=['user', 'club_manager', 'club_user', 'club_post'
        , 'club_ball'])
    response['user'] = model_to_dict(Account.objects.get(openid=data.user.first().openid))
    # response['ball'] = model_to_dict(x.club_ball,exclude='image')
    # response['ball']['image'] = define.MEDIAURL + x.club_ball.name
    if openid != None:
        response['user_flag'] = 'none'
        if model_to_dict(Account.objects.get(openid=data.user.first().openid))['openid'] == openid:
            response['user_flag'] = 'create'
    response['club_manager'] = []
    for manager in data.club_manager.all():
        response['club_manager'].append(model_to_dict(manager))
        if openid != None:
            if model_to_dict(manager)['openid'] == openid:
                response['user_flag'] = 'manager'
    response['club_user'] = []
    for users in data.club_user.all():
        response['club_user'].append(model_to_dict(users))
        if openid != None:
            if model_to_dict(users)['openid'] == openid:
                response['user_flag'] = 'user'
    response['club_post'] = define.MEDIAURL + data.club_post.name
    return response