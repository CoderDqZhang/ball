# coding=utf-8
from django.http import JsonResponse
from mycode.models import define
from mycode.models.game_report import Game_club_report
from mycode.models.game import Game
from mycode.ball_views import game
from mycode.ball_views import game_club
from mycode.models.game_club import GameClub,UnreadMessage
from mycode.models.game_report import game_club_report_images,game_club_report_commond
from mycode.models.account import Account
from django.db.models import Q
import logging
from django.forms.models import model_to_dict
from django.core.files.base import ContentFile
from mycode.utils import upload_qiniu

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
                openid = body['openid']
                data['game_report'] = get_game_club_report(Game_club_report.objects.get(id=report_id), openid=openid)

                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def upload_game_report_sorce(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.GAME_CLUB_REPORT_SORC)
            if checkrequest is None:
                data = {}
                report_id = body['game_report_id']
                openid = body['openid']
                tag_openid = body['tag_openid']
                sorce = body['sorce']
                game_report = Game_club_report.objects.get(id=report_id)
                if game_report.temp_score != "":
                    data['message'] = "比分已上传请等待对方确认"
                    return JsonResponse(define.response("success", 0, request_data=data))
                game_report.temp_score = sorce
                game_report.save()
                message = UnreadMessage.objects.create(
                    message_type=5,
                    message_type_desc='比分确认',
                    read_flag=0
                )
                user = Account.objects.get(openid=openid)
                message.user_openid.add(user)
                message.tag_user_openid.add(Account.objects.get(openid=tag_openid))
                message.unread_game_club_report.add(game_report)
                data['message'] = "上传成功"
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def upload_game_report_images(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.GAME_GAME_REPORT_IMAGES)
            if checkrequest is None:
                data = {}
                openid = body.get('openid',None)
                user = Account.objects.get(openid=body.get('openid'))
                game_club_report = Game_club_report.objects.get(id = body.get('game_report_id'))
                files = request.FILES.get("report_image", None)
                images = upload_qiniu.qiniu_upload("report_image",files)
                club_image = game_club_report_images.objects.create(
                    image = images,
                    content = body.get('content')
                )
                club_image.game_club_report.add(game_club_report)
                club_image.user.add(user)
                print(game_club_report.game_clubA.get().user)
                if user in game_club_report.game_clubA.get().user.all() \
                        or game_club_report.game_clubA.get().club_manager.all() \
                        or game_club_report.game_clubA.get().club_user.all() :
                    club_image.game_club.add(game_club_report.game_clubA.get())
                else:
                    club_image.game_club.add(game_club_report.game_clubB.get())
                data['message'] = '上传成功'
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def game_report_comment(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GAME_REPORT_COMMENT)
        if checkrequest is None:

            data = {}
            commond = game_club_report_commond.objects.create(
                content=body['content'],
                rank = body['rank'],
                skillrank=body['skillrank'],
                anonymity = body['anonymity'],
            )
            user = Account.objects.get(openid=body['openid'])
            game_report = Game_club_report.objects.get(id=body['game_report_id'])
            commond.user.add(user)
            commond.game_club_report.add(game_report)
            commond.save()
            data['content'] = body['content']
            data['anonymity'] = body['anonymity']
            data['userrank'] = body['userrank']
            data['skillrank'] = body['skillrank']
            data['game_report'] = get_game_club_report(game_report, openid=body['openid'])
            data['targuser'] = model_to_dict(user)
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def get_game_report_images(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_GAME_REPOT_INFOS)
        if checkrequest is None:
            game_report_id = body['game_report_id']
            images = game_club_report_images.objects.filter(game_club_report__exact = game_report_id)
            data = {}
            data['images'] = []
            for image in images:
                data['images'].append(model_to_dict(image,
                                                    exclude=['user', 'game_club', 'content','game_club_report', 'createTime', 'url']))
            return JsonResponse(define.response("success", 0, request_data=data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def get_game_report_conmmend(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_GAME_REPOT_INFOS)
        if checkrequest is None:
            game_report_id = body['game_report_id']
            details = game_club_report_commond.objects.filter(game_club_report__exact=game_report_id)
            print(details)
            data = {}
            data["commonds"] = []
            for x in details:
                response = model_to_dict(x, exclude=['user','game_club_report'])
                response['user'] = model_to_dict(x.user.first())
                # response['game'] = model_to_dict(x.tag_user.first())
                data["commonds"].append(response);
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def get_game_club_report(data, openid = None):
    response = {}
    response = model_to_dict(data, exclude=['game','game_clubA','game_clubB','win_club','price'])
    response['game_detail'] = game.returngame_detail(data.game.get())['game_detail']
    # response['price'] = response['game'].number * response['game'].price
    response['club_A'] = game_club.returngame_club(data.game_clubA.get())
    response['club_B'] = game_club.returngame_club(data.game_clubB.get())
    try:
        win_club = data.win_club.get()
        response['win_club'] = game_club.returngame_club(data.win_club.get())
    except:
        response['win_club'] = {}

    if openid is not None:
        response['user_status'] = 0
        user = Account.objects.get(openid=openid)
        if user is data.game_clubA.get().user or data.game_clubB.get().user :
            response['user_status'] = 1
        elif user in data.game_clubA.get().club_manager or data.game_clubB.get().club_manager \
                or data.game_clubA.get().club_user or data.game_clubB.get().club_user:
            response['user_status'] = 2
    return response

def get_game_club_commond(data):
    response = {}
