from django.http import JsonResponse
from mycode.models import define
import logging
from django.forms.models import model_to_dict
from mycode.models.account import Ball,Game,Account
from django.core import serializers

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
        checkrequest = define.request_verif(request, define.GET_GAME_LIST)
        if checkrequest is None:
            game_id = request.POST.get('ball_id')
            games = Game.objects.all().filter(game_detail=Ball.objects.filter(id=game_id))
            data = {}
            data["game_list"] = []
            for x in games:
                response = model_to_dict(x, exclude=['game_create_user',
                                                                   'game_detail','game_user_list'])
                response['user'] = model_to_dict(x.game_create_user.first())
                response['ball'] = model_to_dict(x.game_detail.first())
                data["game_list"].append(response)
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def game_create(request):
    if request.method == 'POST':
        try:
            openid = request.POST.get('openid')
            ball_id = request.POST.get('ball_id')

            user = Account.objects.get(openid=openid)
            ball = Ball.objects.get(id=ball_id)

            checkrequest = define.request_verif(request, define.CREATE_GAME)
            if checkrequest is None:
                data = {}

                if request.POST.get('game_referee') == 0:
                    game_referee = False
                else:
                    game_referee = True
                game = Game.objects.create(
                    game_createTime = request.POST.get('game_createTime'),
                    game_location=request.POST.get('game_location'),
                    game_location_detail=request.POST.get('game_location_detail'),
                    game_price=request.POST.get('game_price'),
                    game_start_time= define.timeStamp_to_date(request.POST.get('game_start_time')),
                    game_end_time=define.timeStamp_to_date(request.POST.get('game_end_time')),
                    game_referee= game_referee,
                    game_number=request.POST.get('game_number'),
                    game_place_condition=request.POST.get('game_place_condition'),
                )
                response = model_to_dict(game, exclude=['game_create_user',
                                                                   'game_detail','game_user_list'])

                game.game_create_user.add(user)
                game.game_detail.add(ball)
                game.game_user_list.add(user)

                response['user'] = model_to_dict(user)
                response['ball'] = model_to_dict(ball)
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