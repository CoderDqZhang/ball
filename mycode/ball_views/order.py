from django.http import JsonResponse
from mycode.models import define
from mycode.models.account import Account
from mycode.models.game import Game
from mycode.models.game_report import Game_club_report
from mycode.ball_views import game_club,game_report,game
from mycode.models.game_club import GameClub
from mycode.models.order import Order
import datetime
from django.forms.models import model_to_dict
from mycode.ball_views import wechat_web_pay
from mycode.libs.pay import WechatAPI
import uuid

#order_type 1=充值 2，提现 3，球约，4，俱乐部对抗赛 5俱乐部，
#status = 0 创建未付款 1，等待付款
def create_order(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.CREATE_ORDER)
            if checkrequest is None:
                print(checkrequest)
                data = {}
                openid = body['openid']
                user = Account.objects.get(openid=openid)
                order_id = str(uuid.uuid1()).replace("-","")
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
                            status = 1
                        )
                        order.game.add(game)
                        order.user.add(user)
                        order.price = game.game_price
                        order.save()
                        data['order'] = get_order_info(order)
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
                            status = 1
                        )
                        order.user.add(user)
                        order.game_report.add(game_report)
                        order.price = game_report.game.get().game_price
                        order.save()
                        data['order'] = get_order_info(order)
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
                            status = 1
                        )
                        order.user.add(user)
                        order.game_club.add(game_club)
                        order.price = game_club.club_price
                        order.save()
                        data['order'] = get_order_info(order)
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
                user = Account.objects.get(openid=openid)
                order_id = str(uuid.uuid1()).replace("-", "")
                order = Order.objects.create(
                    order_id=order_id,
                    order_title='充值',
                    order_desc='充值',
                    order_type=1,
                    status=1
                )
                order.user.add(user)
                order.price = body['price']
                order.save()
                data['order'] = get_order_info(order)
                print(user.balance)
                user.balance = user.balance + body['price']
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
                user = Account.objects.get(openid=openid)
                order_id = str(uuid.uuid1()).replace("-", "")
                order = Order.objects.create(
                    order_id=order_id,
                    order_title='提现',
                    order_desc='提现',
                    order_type=2,
                    status=1
                )
                order.user.add(user)
                order.price = body['price']
                order.save()
                data['order'] = get_order_info(order)
                user.balance = user.balance - body['price']
                user.save()
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def get_order_detail(request):
    if request.method == 'POST':
        try:
            body, checkrequest = define.request_verif(request, define.ORDER_INFO)
            if checkrequest is None:
                data = {}
                orderid = body['orderid']
                order = Order.objects.get(order_id=orderid)
                data['order'] = get_order_info(order)
                return JsonResponse(define.response("success", 0, request_data=data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except  Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data);


def get_order_info(data):
    response = {}
    response = model_to_dict(data,exclude=['user','game_report','game_club','game'])
    response['user'] = model_to_dict(data.user.get())
    if response['order_type'] == 3:
        response['game'] = game.returngame_detail(data.game.get())
    elif response['order_type'] == 4:
        response['game_report'] = game_report.get_game_club_report(data.game_report.get())
    elif response['order_type'] == 5:
        response['game_club'] = game_club.returngame_club(data.game_club.get())
    return response

#'owfcA5f3YCeZlTkXamyvq_AVqk6g'
def get_pay_dic_info(openid,total_fee):
    prepay_id = WechatAPI.WechatOrder(body='TEST', trade_type='JSAPI',
                                      out_trade_no='1415659990',
                                      total_fee=total_fee,
                                      spbill_create_ip='127.0.0.1',
                                      notify_url='http://127.0.0.1:8000/order/payback',
                                      openid=openid)
    prepay_id1 = prepay_id.order_post()[0]['prepay_id']
    pay = WechatAPI.WechatPayAPI(package=str(prepay_id1))
    return pay.get_dic()


def payback(request):
    msg = request.body.decode('utf-8')
    print(msg)
    return JsonResponse(define.response("success", 0, "请使用POST方式请求"))

