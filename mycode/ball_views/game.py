from django.http import JsonResponse
from mycode.models import define
import logging
from django.forms.models import model_to_dict
from mycode.models.account import Ball,Game
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
        game_id = request.POST.get('gameId')
        if game_id is None:
            return JsonResponse(define.response("success", 0, "gameId不能为空"))
        games = Game.objects.all().filter(id=game_id)
        if games is None:
            data = define.response("success", 0)
            data["data"] = []
            return JsonResponse(data)
        else:
            data = define.response("success", 0)
            data["data"] = []
            for x in games:
                print(x)
                data["data"].append(model_to_dict(x))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);