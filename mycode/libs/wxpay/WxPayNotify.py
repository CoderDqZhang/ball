# -*- coding:utf-8 -*-
from WxPayData import WxPayNotifyReply, WxPayOrderQuery
from WxPayApi import WxPayApi


class WxPayNotify(WxPayNotifyReply):
    """
    回调基础类
    """

    def handle(self, xml, need_sign=True):
        """
        回调入口
        @param  xml string
        @param  need_sign bool 是否需要签名输出
        """
        msg = {'msg': "OK"}
        # 当返回false的时候，表示notify中调用notify_callback回调失败获取签名校验失败，此时直接回复失败
        result = WxPayApi.notify(xml, self.notify_callback, msg)
        if not result:
            self.set_data('return_code', "FAIL")
            self.set_data('return_msg', msg['msg'])
            return self._reply_notify(False)
        else:
            # 该分支在成功回调到notify_callback方法，处理完成之后流程
            self.set_data('return_code', "SUCCESS")
            self.set_data('return_msg', "OK")

        return self._reply_notify(need_sign)

    def notify_process(self, data, msg):
        """
        回调方法入口，子类可重写该方法
        注意：
        1、微信回调超时时间为2s，建议用户使用异步处理流程，确认成功之后立刻回复微信服务器
        2、微信服务器在调用失败或者接到回包为非确认包的时候，会发起重试，需确保你的回调是可以重入
        @param  data array 回调解释出的参数
        @param  msg string 如果回调处理失败，可以将错误信息输出到该方法
        @return true回调出来完成不需要继续回调，false回调处理未完成需要继续回调
        """
        # TODO 用户基础该类之后需要重写该方法，成功的时候返回true，失败返回false
        return True

    def notify_callback(self, data):
        """
        notify回调方法，该方法中需要赋值需要输出的参数,不可重写
        @param  data array
        @return true回调出来完成不需要继续回调，false回调处理未完成需要继续回调
        """
        msg = {'msg': "OK"}
        result = self.notify_process(data, msg)

        if result:
            self.set_data('return_code', "SUCCESS")
            self.set_data('return_msg', "OK")
        else:
            self.set_data('return_code', "FAIL")
            self.set_data('return_msg', msg['msg'])

        return result

    def _reply_notify(self, need_sign=True):
        """
        回复通知
        @param  needSign  bool 是否需要签名输出
        """
        # 如果需要签名
        if need_sign and (self.get_data('return_code') == "SUCCESS"):
            self.set_data('sign')
        return WxPayApi.reply_notify(self.to_xml())


class PayNotifyCallBack(WxPayNotify):
    """
    支付回调实现类
    @author minkedong
    """

    def query_order(self, transaction_id):
        """
        查询订单
        """
        order_query_obj = WxPayOrderQuery()
        order_query_obj.set_data('transaction_id', transaction_id)
        result = WxPayApi.order_query(order_query_obj)
        if (result.get('return_code') == 'SUCCESS') and (result.get('result_code') == 'SUCCESS'):
            return True
        return False

    def notify_process(self, data, msg):
        """
        重写回调处理函数
        """
        if 'transaction_id' not in data:
            msg['msg'] = u'输入参数不正确'
            return False

        # 查询订单，判断订单真实性
        if not self.query_order(data.get('transaction_id')):
            msg['msg'] = u'订单查询失败'
            return False
        return True


class JsPayNotifyCallBack(PayNotifyCallBack):
    """
    支付回调实现类
    @author minkedong
    """

    def query_order(self, transaction_id):
        """
        查询订单
        """
        order_query_obj = WxPayOrderQuery()
        order_query_obj.set_data('transaction_id', transaction_id)
        result = WxPayApi.order_query(order_query_obj, js=True)
        if (result.get('return_code') == 'SUCCESS') and (result.get('result_code') == 'SUCCESS'):
            return True
        return False
