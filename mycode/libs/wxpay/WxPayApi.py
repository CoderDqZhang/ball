# -*- coding:utf-8 -*-
import string
import time
import random
import requests

from WxPayException import WxPayException
from WxPayConfig import WxPayConfig
from WxPayData import WxPayResults


class WxPayApi(object):
    """
    接口访问类，包含所有微信支付API列表的封装，类中方法为class方法，
    每个接口有默认超时时间（除提交被扫支付为10s，上报超时时间为1s外，其他均为6s）
    @author minkedong
    """

    @classmethod
    def get_unified_order_resp(cls, unified_order_obj, timeout=6):
        """
        统一下单，WxPayUnifiedOrder中out_trade_no、body、total_fee、trade_type必填
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param  unified_order_obj WxPayUnifiedOrder
        @param  timeout int
        @throws WxPayException
        @return 成功时返回，其他抛异常
        """
        # 检测必填参数
        if not unified_order_obj.get_data('out_trade_no'):
            raise WxPayException(u'缺少统一支付接口必填参数out_trade_no！')
        elif not unified_order_obj.get_data('body'):
            raise WxPayException(u'缺少统一支付接口必填参数body！')
        elif not unified_order_obj.get_data('total_fee'):
            raise WxPayException(u'缺少统一支付接口必填参数total_fee！')
        elif not unified_order_obj.get_data('trade_type'):
            raise WxPayException(u'缺少统一支付接口必填参数trade_type！')

        # 关联参数
        if unified_order_obj.get_data('trade_type') == 'JSAPI' and (not unified_order_obj.get_data('openid')):
            raise WxPayException(u'统一支付接口中，缺少必填参数openid！trade_type为JSAPI时，openid为必填参数！')
        if unified_order_obj.get_data('trade_type') == 'NATIVE' and (not unified_order_obj.get_data('product_id')):
            raise WxPayException(u'统一支付接口中，缺少必填参数product_id！trade_type为NATIVE时，product_id为必填参数！')

        # 异步通知url未设置，则使用配置文件中的url
        if not unified_order_obj.get_data('notify_url'):
            unified_order_obj.set_data('notify_url', WxPayConfig.NOTIFY_URL)
        if unified_order_obj.get_data('trade_type') == 'JSAPI':
            unified_order_obj.set_data('appid', WxPayConfig.APPID1)  # 公众账号ID
        else:
            unified_order_obj.set_data('appid', WxPayConfig.APPID)  # 公众账号ID

        unified_order_obj.set_data('mch_id', WxPayConfig.MCHID)  # 商户号
        unified_order_obj.set_data('spbill_create_ip', '127.0.0.1')  # 终端ip
        unified_order_obj.set_data('nonce_str', cls.get_nonce_str())  # 随机字符串

        # 签名
        unified_order_obj.set_data('sign')
        xml = unified_order_obj.to_xml()

        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        response = cls.post_xml_curl(url, xml, False, timeout)
        result = WxPayResults.proc_xml_resp(response)
        return result

    @classmethod
    def get_nonce_str(cls, length=32):
        return ''.join(random.sample(string.ascii_letters + string.digits, length))

    @classmethod
    def post_xml_curl(cls, url, xml, use_cert=False, timeout=30):
        """
        以post方式提交xml到对应的接口url
        
        @param  xml string 需要post的xml数据
        @param  url string
        @param  use_cert bool 是否需要证书，默认不需要
        @param  timeout int  url执行超时时间，默认30s
        @throws WxPayException
        """
        kwargs_post = {
            'url': url,
            'headers': {'content-type': 'text/xml'},
            'data': xml.encode('utf-8'),
            'timeout': timeout
        }
        try:
            res = requests.post(**kwargs_post)
            if res.status_code == requests.codes.ok:
                return res.content
            else:
                raise WxPayException(u'请求出错，错误码:error')
        except :
            raise WxPayException(u'请求超时')
        # except requests.exceptions.Timeout, e:
        #
        # except Exception, e:
        #     raise WxPayException(u'请求出错，错误码:error')

    @classmethod
    def notify(cls, xml, callback, msg):
        """
        支付结果通用通知
        @param callback function
        直接回调函数使用方法: notify(you_function)
        回调类成员函数方法:notify(array(this, you_function))
        callback  原型为：function function_name(data){}
        """
        try:
            result = WxPayResults.proc_xml_resp(xml)
        except:
            msg['msg'] = "出错"
            return False
        return callback(result)

    @classmethod
    def reply_notify(cls, xml):
        return xml

    @classmethod
    def order_query(cls, order_query_obj, timeout=6, js=False):
        """
        查询订单，WxPayOrderQuery中out_trade_no、transaction_id至少填一个
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param  order_query_obj WxPayOrderQuery
        @param  timeout int
        @throws WxPayException
        @js 是不是 js 回调
        @return 成功时返回，其他抛异常

        """
        url = "https://api.mch.weixin.qq.com/pay/orderquery"
        # 检测必填参数
        if (not order_query_obj.get_data('out_trade_no')) and (not order_query_obj.get_data('transaction_id')):
            raise WxPayException(u'订单查询接口中，out_trade_no、transaction_id至少填一个！')
        if not js:
            order_query_obj.set_data('appid', WxPayConfig.APPID)  # 公众账号ID
        else:
            order_query_obj.set_data('appid', WxPayConfig.APPID1)  # 公众账号ID
        order_query_obj.set_data('mch_id', WxPayConfig.MCHID)  # 商户号
        order_query_obj.set_data('nonce_str', cls.get_nonce_str())  # 随机字符串

        order_query_obj.set_data('sign')  # 签名
        xml = order_query_obj.to_xml()

        response = cls.post_xml_curl(url, xml, False, timeout)
        result = WxPayResults.proc_xml_resp(response)
        return result

    @classmethod
    def get_app_pay_url(cls, app_order_obj):
        app_order_obj.set_data('appid', WxPayConfig.APPID)  # 应用ID
        app_order_obj.set_data('partnerid', WxPayConfig.MCHID)  # 商户号
        app_order_obj.set_data('package', 'Sign=WXPay')
        app_order_obj.set_data('noncestr', cls.get_nonce_str())  # 随机字符串
        app_order_obj.set_data('timestamp', str(int(time.time())))  # 时间戳
        app_order_obj.set_data('sign')  # 签名
        return app_order_obj.get_values()

    @classmethod
    def get_js_pay_url(cls, app_order_obj):
        app_order_obj.set_data('appId', WxPayConfig.APPID1)  # 应用ID
        app_order_obj.set_data('timeStamp', str(int(time.time())))  # 时间戳
        app_order_obj.set_data('nonceStr', cls.get_nonce_str())  # 随机字符串
        app_order_obj.set_data('signType', 'MD5')  # 时间戳
        app_order_obj.set_data('sign')  # 签名
        return app_order_obj.get_values()
