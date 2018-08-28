from django.http import JsonResponse
from mycode.models import define
from mycode.utils import TLS


def verify_sign(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}
        # 获取小程序数据
        body, checkrequest = define.request_verif(request, define.USER_SIGN_TLS)
        if checkrequest is None:
            openid = body['openid']
            appid = body['appid']
            sign = TLS.main(appid,openid)
            print(sign.decode())
            data['userSig'] = sign.decode()
            return JsonResponse(define.response("success", 0, request_data = data))
        else:
            return JsonResponse(define.response("success", 0, checkrequest))
    else:
        return JsonResponse(define.response("success",0,"请使用POST方式请求"))
    return JsonResponse(data)