# -*- coding:utf-8 -*-
import json
import hashlib
import xml
from mycode.libs.wxpay import WxPayException
from mycode.libs.wxpay  import WxPayConfig


class WxPayDataBase(object):
    def __init__(self):
        self._values = {}

    def to_xml(self):
        if (not isinstance(self._values, dict)) or (self._values == {}):
            raise WxPayException(u'数组数据异常！')

        xml = '<xml>'
        for key, value in self._values.items():
            if isinstance(value, basestring):
                xml = '%s<%s><![CDATA[%s]]></%s>' % (xml, key, value, key,)
            else:
                xml = '%s<%s>%s</%s>' % (xml, key, value, key,)
        xml = '%s</xml>' % xml
        return xml

    def from_xml(self, xml):
        if not xml:
            raise WxPayException(u'xml数据异常！')
        try:
            self._values = json.loads(json.dumps(xmltodict.parse(xml)['xml']))
        except Exception as e:
            print(e)
            self._values = {}
        return self._values

    def make_sign(self):
        params_str = self.to_url_params()
        partner_key = WxPayConfig.KEY
        params_str = '%(params_str)s&key=%(partner_key)s' % {'params_str': params_str, 'partner_key': partner_key}
        params_str = hashlib.md5((params_str).encode('utf-8')).hexdigest()
        sign = params_str.upper()
        return sign

    def to_url_params(self):
        return '&'.join(map(lambda _: '%s=%s' % (_, self._values[_]), filter(
            lambda key: key and key not in ['sign'] and self._values.get(key), sorted(self._values.keys()))))

    def set_data(self, key, value=None):
        if key == 'sign':
            value = self.make_sign()
        self._values[key] = value

    def get_data(self, key):
        return self._values.get(key)

    def get_values(self):
        return self._values


class WxPayResults(WxPayDataBase):
    def check_sign(self):
        if self.get_data('sign') and self.get_data('sign') == self.make_sign():
            return True
        raise WxPayException(u'签名错误！')

    @classmethod
    def proc_xml_resp(cls, xml):
        obj = cls()
        obj.from_xml(xml)
        if obj._values.get('return_code') != 'SUCCESS':
            return obj.get_values()
        obj.check_sign()
        return obj.get_values()


class WxPayNotifyReply(WxPayDataBase):
    pass


class WxPayUnifiedOrder(WxPayDataBase):
    pass


class WxPayAppOrder(WxPayDataBase):
    pass


class WxPayOrderQuery(WxPayDataBase):
    pass
