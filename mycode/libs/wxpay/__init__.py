# -*- coding:utf-8 -*-
from .WxPayApi import WxPayApi
from .WxPayConfig import WxPayConfig
from .WxPayException import WxPayException
from .WxPayNotify import PayNotifyCallBack, JsPayNotifyCallBack
from .WxPayData import WxPayUnifiedOrder, WxPayAppOrder


class WxPayBasic(object):
    def __init__(self, *args, **kwargs):
        self.order_info = kwargs

    def _unifiedorder_get_result(self, trade_type):
        """
        统一下单基础函数
        """
        unified_order_obj = WxPayUnifiedOrder()
        unified_order_obj.set_data('out_trade_no', self.order_info.get('tn') or
                                   self.order_info.get('out_trade_no'))
        unified_order_obj.set_data('body', self.order_info.get('body'))
        unified_order_obj.set_data('total_fee', self.order_info.get('total_fee'))
        unified_order_obj.set_data('notify_url', self.order_info.get('notify_url'))
        unified_order_obj.set_data('trade_type', trade_type)
        if trade_type == 'JSAPI':
            unified_order_obj.set_data('openid', self.order_info.get('openid'))
        else:
            if 'openid' in self.order_info.keys():
                del self.order_info['openid']

        if trade_type == 'NATIVE':
            unified_order_obj.set_data('product_id', self.order_info.get('out_trade_no'))
        if self.order_info.get('goods_tag'):
            unified_order_obj.set_data('goods_tag', self.order_info.get('goods_tag'))
        if self.order_info.get('attach'):
            unified_order_obj.set_data('attach', self.order_info.get('attach'))
        if self.order_info.get('time_start'):
            unified_order_obj.set_data('time_start', self.order_info.get('time_start'))
        if self.order_info.get('time_expire'):
            unified_order_obj.set_data('time_expire', self.order_info.get('time_expire'))

        result = WxPayApi.get_unified_order_resp(unified_order_obj)
        if result.get('return_code') == 'SUCCESS':
            if result.get('result_code') == 'SUCCESS':
                return result
            else:
                raise WxPayException(result.get('err_code_des'))
        elif result.get('return_code') == 'FAIL':
            print(result)
            raise WxPayException(result.get('return_msg'))
        else:
            raise WxPayException(u'请求出错，错误码:error')

    def unifiedorder_get_code_url(self, trade_type='NATIVE'):
        result = self._unifiedorder_get_result(trade_type)
        return result.get('code_url')

    def unifiedorder_get_js_url(self, trade_type='JSAPI'):
        result = self._unifiedorder_get_result(trade_type)
        app_order_obj = WxPayAppOrder()
        prepayid = result.get('prepay_id')
        app_order_obj.set_data('package', 'prepay_id=%s' % prepayid)
        return WxPayApi.get_js_pay_url(app_order_obj)

    def unifiedorder_get_app_url(self, trade_type='APP'):
        result = self._unifiedorder_get_result(trade_type)
        app_order_obj = WxPayAppOrder()
        app_order_obj.set_data('prepayid', result.get('prepay_id'))
        return WxPayApi.get_app_pay_url(app_order_obj)
