# coding=utf-8
from django.http import JsonResponse
from mycode.models import define
import logging
from django.forms.models import model_to_dict
from mycode.models.account import Account
from mycode.models.game_club import GameClub
from mycode.models.game import Ball,Game,Apointment
from django.core import serializers
import json
from django.utils import timezone
import datetime
import sys
import importlib
importlib.reload(sys)
from django.db.models import Q
from mycode.ball_views import tencent_im
from django.db.models.aggregates import Count
from mycode.ball_views import order
from django.db.models import Sum

logger = logging.getLogger(__name__)  # 刚才在setting.py中配置的logger

def ball_list(request):
    balls = Ball.objects.all().values()
    if balls is None:
        data = define.response("success",0)
        data["data"] = []
        return JsonResponse(data)
    else:
        data = define.response("success",0)
        data["data"] = []
        for x in balls:
            x['image'] = define.MEDIAURL + x['image']
            list = Game.objects.filter(game_detail__exact=x['id'],game_end_time__gte=timezone.now())
            x['count'] = list.count()
            data["data"].append(x)
            print(x)
    return JsonResponse(data)

def game_list(request):
    if request.method == 'POST':
        body,checkrequest = define.request_verif(request, define.GET_GAME_LIST)
        if checkrequest is None:
            ball_id = body['ball_id']
            #1.0.1版本中增加俱乐部权限
            try:
                print(body['open_id'])
                games = Game.objects.filter(game_detail__exact=ball_id).order_by('-game_createTime') \
                    .filter((Q(game_club_create=0)) |
                            (Q(game_club_create=1) & Q(game_club_out=0)) |
                            (Q(game_club_create=1) & Q(game_club_out=1) &
                            (Q(game_club__user__openid__exact=body['open_id']) |
                            Q(game_club__club_manager__openid__exact=body['open_id']) |
                            Q(game_club__club_user__openid__exact=body['open_id']))))
            except:
                games = Game.objects.filter(game_detail__exact=ball_id).order_by('-game_createTime')
            data = {}

            data["game_list"] = []
            for x in games:
                response = model_to_dict(x, exclude=['game_create_user','game_club','game_detail','game_user_list',
                                                     ])
                user = x.game_create_user.first()
                if timezone.now() > x.game_end_time:
                    response['game_status'] = 0 # time done
                else:
                    response['game_status'] = 1 # doing

                response['user'] = model_to_dict(x.game_create_user.first())
                data["game_list"].append(response);
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def game_detail(request):
    if request.method == 'POST':
        body,checkrequest = define.request_verif(request, define.GET_GAME_DETAIL)
        if checkrequest is None:
            game_id = body['game_id']
            openid = body['openid']
            detail = Game.objects.get(id=game_id)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                data = returngame_detail(detail, openid)
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def game_create(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.CREATE_GAME)

            if checkrequest is None:
                openid = body['openid']
                ball_id = body['ball_id']

                user = Account.objects.get(openid=openid)
                ball = Ball.objects.get(id=ball_id)
                data = {}
                if request.POST.get('game_referee') == 0:
                    game_referee = False
                else:
                    game_referee = True

                game = Game.objects.create(
                    game_title = body['game_title'],
                    game_subtitle = body['game_subtitle'],
                    game_location=body['game_location'],
                    game_latitude = body['lat'],
                    game_longitude = body['lng'],
                    game_location_detail=body['game_location_detail'],
                    game_price=body['game_price'],
                    game_start_time= define.timeStamp_to_date(body['game_start_time']),
                    game_end_time=define.timeStamp_to_date(body['game_end_time']),
                    game_referee= game_referee,
                    game_number=body['game_number'],
                    game_place_condition=body['game_place_condition'],

                )

                if 'club_create' in body:
                    game.game_club_create = body['club_create']
                    game.game_club_out = body['club_out']
                    game.game_club.add(GameClub.objects.get(id=body['club_id']))
                    game.save()
                response = model_to_dict(game, exclude=['game_create_user','game_club',
                                                                   'game_detail','game_user_list'])

                apointment = Apointment.objects.create(
                    number = 1,
                )
                apointment.user.add(user)

                game.game_create_user.add(user)
                game.game_detail.add(ball)
                game.game_user_list.add(apointment)
                response['user'] = model_to_dict(user)
                response['ball'] = model_to_dict(ball,exclude='image')
                response['ball']['image'] = ball.image.name
                data['game'] = response
                tencent_im.game_create_group(game)
                return JsonResponse(define.response("success", 0, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
        except  Ball.DoesNotExist:
            return JsonResponse(define.response("success", 0, "球约不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求",None))
    return JsonResponse(data);

def game_appointment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_GAME_APPLEMENT)
        if checkrequest is None:
            game_id = body['game_id']
            openid = body['openid']
            number = body['number_count']
            detail = Game.objects.get(id=game_id)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                if detail.game_user_list.all().filter(user__openid__exact=openid):
                    data['message'] = "已经赴约了"
                    print(detail)
                    return JsonResponse(define.response("success", 0, None, data))
                else:
                    appoint_number = detail.game_user_list.all().values('number').annotate(appointment_number=Sum('number'))
                    appoint_numbers = 0
                    for num in appoint_number:
                        appoint_numbers = appoint_numbers + int(num['number'])

                    if appoint_numbers + number > detail.game_number:
                        data['message'] = "球约人数已满"
                        return JsonResponse(define.response("success", 0, None, data))

                user = Account.objects.get(openid=openid)
                if user.balance > detail.game_price:
                    user.balance = user.balance - detail.game_price
                    user.save()
                    data['order'] = 'success'
                else:
                    data['order'] = order.get_pay_dic_info(openid=openid, total_fee=1)
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);


def add_game_appointment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_GAME_APPLEMENT)
        if checkrequest is None:
            game_id = body['game_id']
            openid = body['openid']
            number = body['number_count']
            detail = Game.objects.get(id=game_id)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                if detail.game_user_list.all().filter(user__openid__exact=openid):
                    data['message'] = "已经赴约了"
                    return JsonResponse(define.response("success", 0, None, data))
                else:
                    appoint_number = detail.game_user_list.all().values('number').annotate(appointment_number=Sum('number'))
                    appoint_numbers = 0
                    for num in appoint_number:
                        appoint_numbers = appoint_numbers + int(num['number'])
                    if appoint_numbers + number > detail.game_number:
                        data['message'] = "球约人数已满"
                        return JsonResponse(define.response("success", 0, None, data))
                add_user = Account.objects.get(openid=openid)
                list = Apointment()
                list = Apointment.objects.create(
                    number = number
                )
                list.user.add(add_user)
                detail.game_user_list.add(list)
                data = returngame_detail(detail, openid)
                taguser = Account.objects.get(openid=detail.game_create_user.get().openid)
                taguser.balance = taguser.balance + detail.game_price
                taguser.save()
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def cancel_game_appointment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.CANCEL_MY_GAME_APPLEMENT)
        if checkrequest is None:
            game_id = body['game_id']
            openid = body['openid']
            detail = Game.objects.get(id=game_id)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                detail.game_user_list.remove(Account.objects.get(openid=openid))
                data = returngame_detail(detail,openid)
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def my_game_appointment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_MY_GAME_APPLEMENT)
        if checkrequest is None:
            openid = body['openid']
            detail = Game.objects.filter(Q(game_user_list__user__openid=openid)|Q(game_create_user__openid=openid))\
                .order_by('-game_end_time')
            data = {}
            data["game_list"] = []
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                for model in detail:
                    response = model_to_dict(model,
                                             exclude=['game_create_user', 'game_club', 'game_detail', 'game_user_list',
                                                      ])
                    user = model.game_create_user.first()
                    if timezone.now() > model.game_end_time:
                        response['game_status'] = 0  # time done
                    else:
                        response['game_status'] = 1  # doing

                    response['user'] = model_to_dict(model.game_create_user.first())
                    data["game_list"].append(response)
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);


def search(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_GAME_LIST_KEYWORD)
        if checkrequest is None:
            keyword = body['keyword']
            ball_id = body['ball_id']
            try:
                print(body['open_id'])
                games = Game.objects.filter(
                    Q(game_title__icontains=keyword) | Q(game_create_user__nickname__icontains=keyword) \
                    | Q(game_location_detail__icontains=keyword) | Q(game_subtitle__contains=keyword)
                    , game_detail__exact=ball_id).filter((Q(game_club_create=0)) |
                        (Q(game_club_create=1) & Q(game_club_out=0)) |
                        (Q(game_club_create=1) & Q(game_club_out=1) &
                         (Q(game_club__user__openid__exact=body['open_id']) |
                          Q(game_club__club_manager__openid__exact=body['open_id']) |
                          Q(game_club__club_user__openid__exact=body['open_id']))))
            except:
                games = Game.objects.filter(Q(game_title__icontains=keyword)|Q(game_create_user__nickname__icontains=keyword)\
                                        |Q(game_location_detail__icontains=keyword)|Q(game_subtitle__contains=keyword)
                                        ,game_detail__exact=ball_id)
            data = {}
            data["game_list"] = []
            for x in games:
                response = returngame_detail(x)
                data["game_list"].append(response)
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def delete_my_game_appointment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.DELETE_GET_MY_GAME_APPLEMENT)
        if checkrequest is None:
            game_id = body['game_id']
            openid = body['openid']
            try:
                detail = Game.objects.get(id=game_id)
                data = {}
                if detail is None:
                    return JsonResponse(define.response("success", 0, "球约不存在"))
                else:
                    user_list = detail.game_user_list.all()
                    print(detail.game_user_list)
                    if openid==detail.game_create_user.all().first().openid:
                        if user_list.count() > 1:
                            return JsonResponse(define.response("success", 0, "无法删除"))
                        else:
                            ret = Game.objects.get(id=game_id).delete()
                            return JsonResponse(define.response("success", 0, None, data))
                    else:
                        return JsonResponse(define.response("success", 0, "无法删除"))
            except  Game.DoesNotExist:
                return JsonResponse(define.response("success", 0, "球约不存在"))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def returngame_detail(detail,openid = None):
    data = {}
    data["game_detail"] = model_to_dict(detail, exclude=['game_create_user','game_club', 'game_detail', 'game_user_list',
                                                         ])
    try:
        user = detail.game_create_user.get()
        data["game_detail"]['user'] = model_to_dict(detail.game_create_user.first())
        print(user)
    except:
        print("非用户创建")
    image = define.MEDIAURL + detail.game_detail.get().image.name
    data["game_detail"]['ball'] = model_to_dict(detail.game_detail.get(), exclude='image')
    data["game_detail"]['ball']['image'] = image
    user_list = detail.game_user_list.all()
    data["game_detail"]['user_list'] = []
    data["game_detail"]['appoint_ment'] = False
    if timezone.now() > detail.game_end_time:
        data["game_detail"]['game_status'] = 0  # time done
    else:
        data["game_detail"]['game_status'] = 1  # doing
    for x in user_list:
        reponse = {}
        reponse['number_count'] = model_to_dict(x, exclude='user')
        try:
            openid = x.user.all().first().openid
            reponse['user'] = model_to_dict(Account.objects.get(openid=openid))
            data["game_detail"]['user_list'].append(reponse)
            reponse['user']['appointment_count'] = Game.objects.all().filter(
                Q(game_user_list__user__openid__exact=x.user.all().first().openid)
                | Q(game_create_user__openid=x.user.all().first().openid)).count()
            if reponse['user']['openid'] == openid:
                data["game_detail"]['appoint_ment'] = True
        except:
            print("出现错误")
    return data