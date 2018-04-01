# Create your views here.

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms.models import model_to_dict
from mycode.models.account import Account
from .checkuser import checkdata
import logging
from mycode.models import define
from mycode.models.serializers import AccountSerializer
import json

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

logger = logging.getLogger(__name__)  # 刚才在setting.py中配置的logger


def verify_user(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}

        # 获取小程序数据
        code = json.loads(request.body.decode('utf-8'))['code']
        user = authenticate(username=code, password=code)
        # 登陆用户并保存 cookie
        if user:
            login(request, user)
            query_user = Account.objects.get(openid=code)
            query_user.save()
            data['status'] = '已登录'
        # 新建用户
        else:
            user_ins = User.objects.create(
                username=code,
                password=code
            )
            user_ins.save()
            user_ins.is_active = True
            account = Account.objects.create(
                user=user_ins,
                openid=code
            )
            new_user = authenticate(username=code, password=code)
            login(request, new_user)
            data['status'] = '已创建并登录'
        res = {'error': '错误'}
        data['info'] = res
        return JsonResponse(data)
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
                user.gender = body['gender']
                user.weight = body['weight']
                user.height = body['height']
                user.game_age = body['ball_age']
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
    if request.method == 'GET':
        openid = request.GET.get('openid')
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
        return JsonResponse(define.response("success", 0, "请使用GET方式请求"))
    return JsonResponse(data)


def get_user_info(request):
    if request.method == 'GET':
        openid = request.GET.get('openid')
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
        return JsonResponse(define.response("success", 0, "请使用GET方式请求"))
    return JsonResponse(data)

def test(request):
    return JsonResponse({'success':'成功'})