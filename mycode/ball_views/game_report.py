# coding=utf-8
from django.http import JsonResponse
from mycode.models import define
from mycode.models.game_report import Game_club_report
from mycode.models.game import Game
from mycode.ball_views import game
from mycode.ball_views import game_club
from mycode.models.game_club import GameClub,UnreadMessage
from mycode.models.account import Account
import logging
from django.forms.models import model_to_dict

#创建俱乐部
def create_game_report(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.CREATE_GAME_REPORT)
            if checkrequest is None:
                print(checkrequest)
                data = {}
                openid = body['openid']
                club_idA = body['club_idA']
                club_idB = body['club_idB']
                game_id = body['game_id']
                game = Game.objects.get(id=game_id)
                clubA = GameClub.objects.get(id=club_idA)
                clubB = GameClub.objects.get(id=club_idB)
                game_report = Game_club_report.objects.create(
                    price=game.game_price * game.game_number,
                    score=0,
                    award='',
                    success=1,
                    desc='未接受'
                )
                game_report.game_clubA.add(club_idA)
                game_report.game_clubB.add(club_idB)
                game_report.game.add(game)

                #发送俱乐部对抗赛邀请
                unread = game_club.UnreadMessage.objects.create(
                    message_type=4,
                    message_type_desc='俱乐部对抗赛邀请',
                    read_flag=0
                )
                user = Account.objects.get(openid=openid)
                unread.user_openid.add(user)
                unread.tag_user_openid.add(Account.objects.get(openid=clubB.user.first().openid))
                unread.unread_game_club_report.add(game_report)
                data['game_club'] = get_game_club_report(game_report)
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def get_game_club_report_list(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.GAME_CLUB_REPORT_LIST)
            if checkrequest is None:
                data = {}
                game_reports = Game_club_report.objects.all()
                data['game_reports'] = []
                print(len(game_reports))
                for game_report in game_reports:
                    data['game_reports'].append(get_game_club_report(game_report))
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def get_game_club_detail(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.GAME_CLUB_REPORT_DETAIL)
            if checkrequest is None:
                data = {}
                report_id = body['game_report_id']
                data['game_report'] = get_game_club_report(Game_club_report.objects.get(id=report_id))

                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def get_game_club_report(data):
    response = {}
    response = model_to_dict(data, exclude=['game','game_clubA','game_clubB','win_club','price'])
    response['game'] = game.returngame_detail(data.game.get())
    # response['price'] = response['game'].number * response['game'].price
    response['club_A'] = game_club.returngame_club(data.game_clubA.get())
    response['club_B'] = game_club.returngame_club(data.game_clubB.get())
    try:
        win_club = data.win_club.get()
        response['win_club'] = game_club.returngame_club(data.win_club.get())
    except:
        response['win_club'] = {}
    return response

def get_game_club_commond(data):
    response = {}
