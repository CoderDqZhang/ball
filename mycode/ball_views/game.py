# coding=utf-8
from django.http import JsonResponse
from mycode.models import define
import logging
from django.forms.models import model_to_dict
from mycode.models.account import Ball,Game,Account,Apointment
from django.core import serializers
import json

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
            data["data"].append(x)
    return JsonResponse(data)

def game_list(request):
    if request.method == 'POST':
        body,checkrequest = define.request_verif(request, define.GET_GAME_LIST)
        if checkrequest is None:
            ball_id = body['ball_id']
            games = Game.objects.filter(game_detail__exact=ball_id)
            print(games)
            data = {}
            print(games)
            data["game_list"] = []
            for x in games:
                response = model_to_dict(x, exclude=['game_create_user','game_detail','game_user_list',
                                                     ])
                user = x.game_create_user.first()
                response['user'] = model_to_dict(x.game_create_user.first())
                # response['ball'].append(x.game_detail.values())
                print(response);
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
            detail = Game.objects.get(id=game_id)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:

                data["game_detail"] = model_to_dict(detail, exclude=['game_create_user','game_detail','game_user_list',
                                                  ])
                user = detail.game_create_user.first()
                data["game_detail"]['user'] = model_to_dict(detail.game_create_user.first())
                image = detail.game_detail.first().image
                data["game_detail"]['ball'] = model_to_dict(detail.game_detail.first(), exclude='image')
                user_list = detail.game_user_list.all()
                data["game_detail"]['user_list'] = []
                print(detail.game_user_list)
                for x in user_list:
                    reponse = {}
                    reponse['number_count'] = model_to_dict(x,exclude='user')
                    #这个有问题
                    reponse['user'] = model_to_dict(detail.game_create_user.first())
                    data["game_detail"]['user_list'].append(reponse)
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
            print(body)
            openid = body['openid']
            ball_id = body['ball_id']

            user = Account.objects.get(openid=openid)
            ball = Ball.objects.get(id=ball_id)

            if checkrequest is None:
                data = {}

                if request.POST.get('game_referee') == 0:
                    game_referee = False
                else:
                    game_referee = True
                game = Game.objects.create(
                    game_title = body['game_title'],
                    game_subtitle = body['game_subtitle'],
                    game_location=body['game_location'],
                    game_location_detail=body['game_location_detail'],
                    game_price=body['game_price'],
                    game_start_time= define.timeStamp_to_date(body['game_start_time']),
                    game_end_time=define.timeStamp_to_date(body['game_end_time']),
                    game_referee= game_referee,
                    game_number=body['game_number'],
                    game_place_condition=body['game_place_condition'],

                )
                response = model_to_dict(game, exclude=['game_create_user',
                                                                   'game_detail','game_user_list'])

                # apointment = Apointment(
                #     number = 1,
                #     user = user
                # )


                game.game_create_user.add(user)
                game.game_detail.add(ball)
                # game.game_user_list.add(apointment)

                response['user'] = model_to_dict(user)
                response['ball'] = model_to_dict(ball,exclude='image')
                data['game'] = response
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
                add_user = Account.objects.get(openid=openid)
                print(add_user)
                list = Apointment()
                list = Apointment.objects.create(
                    number = number
                )
                list.user.add(add_user)
                detail.game_user_list.add(list)
                data["game_detail"] = model_to_dict(detail,
                                                    exclude=['game_create_user', 'game_detail', 'game_user_list',
                                                             ])
                user = detail.game_create_user.first()

                data["game_detail"]['user'] = model_to_dict(detail.game_create_user.first())
                image = detail.game_detail.first().image
                data["game_detail"]['ball'] = model_to_dict(detail.game_detail.first(), exclude='image')
                user_list = detail.game_user_list.all()
                data["game_detail"]['user_list'] = []

                data["game_detail"]['user_list'].append(model_to_dict(list,exclude='user'))
                for x in user_list:
                    data["game_detail"]['user_list'].append(model_to_dict(x,exclude='user'))
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);


def my_game_appointment(request):
    if request.method == 'GET':
        body, checkrequest = define.request_verif(request, define.GET_MY_GAME_APPLEMENT)
        if checkrequest is None:
            openid = body['openid']
            detail = Game.objects.all().filter(game_create_user=Account.objects.filter(openid=openid))
            print(detail)
            data = {}
            if detail is None:
                return JsonResponse(define.response("success", 0, "球约不存在"))
            else:
                data["game_list"] = []
                for x in detail:
                    response = model_to_dict(x, exclude=['game_create_user', 'game_detail', 'game_user_list',
                                                    ])
                    user = x.game_create_user.first()
                    print(response)
                    response['user'] = model_to_dict(x.game_create_user.first())
                    image = x.game_detail.first().image
                    response['ball'] = model_to_dict(x.game_detail.first(), exclude='image')
                    # response['ball']['image'] = image
                    data["game_list"].append(response)
                return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);