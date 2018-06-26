from django.http import JsonResponse
from mycode.models import define
from mycode.models.account import Account
from mycode.models.game import Game
from mycode.models.game_report import Game_club_report
from mycode.models.game_club import GameClub
from mycode.models.order import Order
import datetime

#order_type 1=充值 2，提现 3，球约，4，俱乐部对抗赛 5俱乐部，
#status = 0 创建未付款 1，等待付款
def create_order(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.CREATE_GAME_REPORT)
            if checkrequest is None:
                print(checkrequest)
                data = {}
                openid = body['openid']
                user = Account.objects.get(openid=openid)
                order_id = define.date_to_timeStamp(date=datetime.time)
                print(order_id)
                if 'game_id' in body:
                    game_id = body['game_id']
                    game = Game.objects.get(id=game_id)
                    if game.game_price > user.balance :
                        data['message'] = '余额不足'
                    else:
                        order = Order.objects.create(
                            order_id = order_id,
                            order_title = '球约',
                            order_desc = '球约付款',
                            order_type = 3,
                            order_status = 1
                        )
                        order.game.add(game)
                        order.price = game.game_price
                        order.save()
                elif 'game_report_id' in body:
                    game_report_id = body['game_report_id']
                    game_report = Game_club_report.objects.get(id=game_report_id)
                    if game_report.game.get().game_price > user.balance :
                        data['message'] = '余额不足'
                    else:
                        order = Order.objects.create(
                            order_id = order_id,
                            order_title = '俱乐部球赛',
                            order_desc = '俱乐部球赛付款',
                            order_type = 4,
                            order_status = 1
                        )
                        order.game_report.add(game_report)
                        order.price = game_report.game.get().game_price
                        order.save()
                elif 'game_club_id' in body:
                    game_club_id = body['game_club_id']
                    game_club = GameClub.objects.get(id=game_club_id)
                    if game_club.club_price > user.balance :
                        data['message'] = '余额不足'
                    else:
                        order = Order.objects.create(
                            order_id = order_id,
                            order_title = '俱乐部',
                            order_desc = '会费',
                            order_type = 5,
                            order_status = 1
                        )
                        order.game_club.add(game_club)
                        order.price = game_club.club_price
                        order.save()
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def topup(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.TOP_UP)
            if checkrequest is None:
                data = {}
                openid = body['openid']
                pay_type = body['pay_type']
                price = body['price']
                user = Account.objects.get(openid=openid)
                user['balance'] = user['balance'] + price
                user.save()
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);

def withdraw(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.TOP_UP)
            if checkrequest is None:
                data = {}
                openid = body['openid']
                pay_type = body['pay_type']
                price = body['price']
                user = Account.objects.get(openid=openid)
                user['balance'] = user['balance'] + price
                user.save()
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);