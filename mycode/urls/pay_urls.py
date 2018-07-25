from django.conf.urls import url
from mycode.libs.pay import wechatConfig,WechatAPI,WechatAPI

urlpatterns = [
    # # 支付下单及请求
    # url(r'^wechatPay$', WechatAPI.as_view()),
    # # 授权请求
    # url(r'^auth/$', AuthView.as_view()),
    # # 之前的授权回调页面
    # url(r'^index$', GetInfoView.as_view()),
    # # 调起支付后返回结果的回调页面
    # url(r'^success$', views.success),
    # # 这里我省掉了我的其它页面

]