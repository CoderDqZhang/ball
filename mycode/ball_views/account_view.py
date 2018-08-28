# Create your views here.
# coding=utf-8
import importlib
import json
import sys
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from mycode.ball_views import tencent_im
from mycode.libs.pay import WechatAPI
from mycode.models import define
from mycode.models.account import Account,Commond

importlib.reload(sys)

# def verify_user(request):
#     if request.method == 'POST':
#         # print(request.POST)
#         # 初始化返回的字典
#         data = {}
#
#         # 获取小程序数据
#         code = request.POST.get('code')
#         encrypteddata = request.POST.get('encrypteddata')
#         iv = request.POST.get('iv')
#
#         # 检查用户
#         res = checkdata(code, encrypteddata, iv)
#         print('解码信息',res)
#         # 检查不通过
#         errorinfo = res.get('error', None)
#         if errorinfo:
#             return JsonResponse(res)
#
#         openid = res['openId']
#
#         user = authenticate(username=openid, password=openid)
#         # 登陆用户并保存 cookie
#         if user:
#             login(request, user)
#             query_user = account.objects.get(openid=openid)
#             query_user.cookie = res['cookie']
#             query_user.save()
#
#             data['status'] = '已登录'
#         # 新建用户
#         else:
#             user_ins = account.objects.create_user(
#                 username=openid,
#                 password=openid
#             )
#             profile = account.objects.create(
#                 user=user_ins,
#                 openid=openid,
#                 cookie=res['cookie'],
#                 nickname=res['nickName'],
#                 city=res['city'],
#                 province=res['province'],
#                 gender=res['gender']
#
#             )
#
#             new_user = authenticate(openid=openid)
#             login(request, new_user)
#             data['dirs'] = ['默认']
#             data['status'] = '已创建并登录'
#
#         data['info'] = res
#         # print('最终返回信息',data)
#
#         return JsonResponse(data)
#
#     data = {'error': '仅接受POST请求'}
#     return JsonResponse(data)
#
# logger = logging.getLogger(__name__)  # 刚才在setting.py中配置的logger

def verify_user(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.WE_CHAT_LOGIN)
        if checkrequest is None:
            code = body['code']
            openid = define.getopenid(code)
            print(openid)
            try:
                user = Account.objects.get(openid=openid)
                print(user)
                data['user'] = model_to_dict(user)
                return JsonResponse(define.response("success", 0, None, data))
            except Account.DoesNotExist:
                try:
                    user_ins =  User.objects.get(username=openid)
                except :
                    user_ins = User.objects.create_user(
                        username=openid,
                        password=openid
                    )
                    user_ins.save()
                    user_ins.is_active = True
                print(body['avatar'])

                account = Account.objects.create(
                    user=user_ins,
                    openid=openid
                )
                data['user'] = model_to_dict(Account.objects.get(openid=openid))
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)

def update_user_info(request):
    if request.method == 'POST':
        openid = json.loads(request.body.decode('utf-8'))['openid']
        try:
            user = Account.objects.get(openid=openid)
            body, checkrequest = define.request_verif(request,define.UPDATA_USER_INFO)
            if checkrequest is None:
                user.nickname = body['nickname']
                user.age = body['age']
                user.sign = body['sign']
                user.gender = body['gender']
                user.weight = body['weight']
                user.height = body['height']
                user.game_age = body['game_age']
                user.phone = body['phone']
                user.province = body['province']
                user.city = body['city']
                user.avatar = body['avatar']
                user.good_point = body['good_point']
                user.save()
                data = {}
                data['user'] = model_to_dict(user)
                return JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在"))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data)


def get_user_info(request):
    if request.method == 'POST':
        openid = json.loads(request.body.decode('utf-8'))['openid']
        try:
            user = Account.objects.get(openid=openid)
            body, checkrequest = define.request_verif(request,define.GET_USER_INFO)
            if checkrequest is None:
                data = {}
                # return  AccountSerializer
                data['user'] = model_to_dict(user)
                return  JsonResponse(define.response("success", 0, None, data))
            else:
                return JsonResponse(define.response("success", 0, checkrequest))
        except Account.DoesNotExist:
            return JsonResponse(define.response("success", 0, "用户不存在",None))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data)

def conmmend_user(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.COMMOND_USER_INFO)
        if checkrequest is None:

            data = {}
            commond = Commond.objects.create(
                content=body['content'],
                userrank = body['userrank'],
                skillrank=body['skillrank'],
                anonymity = body['anonymity'],
            )
            user = Account.objects.all().get(openid=body['openid'])
            targuser = Account.objects.all().get(openid=body['targid'])
            commond.user.add(user)
            commond.tag_user.add(targuser)
            commond.save()
            data['content'] = body['content']
            data['anonymity'] = body['anonymity']
            data['userrank'] = body['userrank']
            data['skillrank'] = body['skillrank']
            data['user'] = model_to_dict(targuser)
            data['targuser'] = model_to_dict(user)
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def get_user_conmmend(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_USER_COMMOND)
        if checkrequest is None:
            openid = body['openid']
            details = Commond.objects.filter(user__exact=openid)
            print(details)
            data = {}
            data["commonds"] = []
            for x in details:
                response = model_to_dict(x, exclude=['user','tag_user'])
                response['user'] = model_to_dict(x.user.first())
                response['tag_user'] = model_to_dict(x.tag_user.first())
                data["commonds"].append(response);
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def get_user_other_conmmend(request):
    if request.method == 'POST':
        body, checkrequest = define.request_verif(request, define.GET_USER_COMMOND)
        if checkrequest is None:
            openid = body['openid']
            details = Commond.objects.filter(tag_user__exact=openid)
            data = {}
            data["commonds"] = []
            for x in details:
                response = model_to_dict(x, exclude=['user','tag_user'])
                response['user'] = model_to_dict(x.user.first())
                response['tag_user'] = model_to_dict(x.tag_user.first())
                data["commonds"].append(response);
            return JsonResponse(define.response("success", 0, None, data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success", 0, "请使用POST方式请求"))
    return JsonResponse(data);

def create_Im(request):
    prepay_id = WechatAPI.WechatOrder(body='TEST',trade_type='JSAPI',
                                      out_trade_no='1415659990',
                                      total_fee="122",
                                      spbill_create_ip='127.0.0.1',
                                      notify_url='http://www.weixin.qq.com/wxpay/pay.php',
                                      openid='owfcA5f3YCeZlTkXamyvq_AVqk6g')
    prepay_id1 = prepay_id.order_post()[0]['prepay_id']
    pay = WechatAPI.WechatPayAPI(package=str(prepay_id1))
    print(pay.get_dic())
    return JsonResponse({'success':'成功'})

def testsend_msg(request):
    print(tencent_im.sender_image('admin'))
    # print(tencent_im.sender_msg('admin'))
    return JsonResponse({'success':'成功'})