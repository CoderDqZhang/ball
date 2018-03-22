# Create your views here.

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth

from mycode.models.account import Account
from .checkuser import checkdata
import logging


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
        code = request.POST.get('code')

        print(code)
        user = authenticate(username=code, password=code)
        # 登陆用户并保存 cookie
        print(user)
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
            print(user_ins.username)
            print(user_ins.password)
            account = Account.objects.create(
                user=user_ins,
                openid=code
            )
            new_user = authenticate(username=code, password=code)
            print(new_user)
            login(request, new_user)
            data['status'] = '已创建并登录'
        res = {'error': '错误'}
        data['info'] = res
        return JsonResponse(data)

    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)

def test(request):
    return JsonResponse({'success':'成功'})