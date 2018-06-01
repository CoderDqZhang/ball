#! /usr/bin/python
# coding:utf-8

__author__ = "tls@tencent.com"
__date__ = "$Mar 3, 2016 03:00:43 PM"

import OpenSSL
import base64
import zlib
import json
import time

ecdsa_pri_key = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgzAKnuEw6FXrRYQFJ
GNGh9OFPyeSwMQGZiDytR7rBNE+hRANCAASQ2eeeoj47RFnuLGYoHY/gAvyPxKRX
6CIbqU1RIgZgGsT0ma6qAFVPGvlEwEmumFXd6GNB9rHltP7Fk7QI4R0V
-----END PRIVATE KEY-----
"""


def list_all_curves():
    list = OpenSSL.crypto.get_elliptic_curves()
    for element in list:
        print(element)


def get_secp256k1():
    print(OpenSSL.crypto.get_elliptic_curve('secp256k1'));


def base64_encode_url(data):
    base64_data = base64.b64encode(data)
    # base64_data = base64_data.replace('+', '*')
    # base64_data = base64_data.replace('/', '-')
    # base64_data = base64_data.replace('=', '_')
    return base64_data


def base64_decode_url(base64_data):
    base64_data = base64_data.replace('*', '+')
    base64_data = base64_data.replace('-', '/')
    base64_data = base64_data.replace('_', '=')
    raw_data = base64.b64decode(base64_data)
    return raw_data


class TLSSigAPI:
    """"""
    __acctype = 0
    __identifier = ""
    __appid3rd = ""
    __sdkappid = 0
    __version = 20151204
    __expire = 3600 * 24 * 30  # 默认一个月，需要调整请自行修改
    __pri_key = ""
    __pub_key = ""
    _err_msg = "ok"

    def __get_pri_key(self):
        return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, self.__pri_key);

    def __init__(self, sdkappid, pri_key):
        self.__sdkappid = sdkappid
        self.__pri_key = pri_key

    def __create_dict(self):
        m = {}
        m["TLS.account_type"] = "%d" % self.__acctype
        m["TLS.identifier"] = "%s" % self.__identifier
        m["TLS.appid_at_3rd"] = "%s" % self.__appid3rd
        m["TLS.sdk_appid"] = "%d" % self.__sdkappid
        m["TLS.expire_after"] = "%d" % self.__expire
        m["TLS.version"] = "%d" % self.__version
        m["TLS.time"] = "%d" % time.time()
        return m

    def __encode_to_fix_str(self, m):
        fix_str = "TLS.appid_at_3rd:" + m["TLS.appid_at_3rd"] + "\n" \
                  + "TLS.account_type:" + m["TLS.account_type"] + "\n" \
                  + "TLS.identifier:" + m["TLS.identifier"] + "\n" \
                  + "TLS.sdk_appid:" + m["TLS.sdk_appid"] + "\n" \
                  + "TLS.time:" + m["TLS.time"] + "\n" \
                  + "TLS.expire_after:" + m["TLS.expire_after"] + "\n"
        return fix_str

    def tls_gen_sig(self, identifier):
        self.__identifier = identifier

        m = self.__create_dict()
        fix_str = self.__encode_to_fix_str(m)
        pk_loaded = self.__get_pri_key()
        sig_field = OpenSSL.crypto.sign(pk_loaded, fix_str, "sha256");
        sig_field_base64 = base64.b64encode(sig_field).decode()
        m["TLS.sig"] = sig_field_base64
        json_str = json.dumps(m)
        sig_cmpressed = zlib.compress(json_str.encode())
        base64_sig = base64_encode_url(sig_cmpressed)
        return base64_sig

    def gzip_compress(raw_data):
        buf = StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(raw_data)
        finally:
            f.close()
        return buf.getvalue()

    def gzip_uncompress(c_data):
        buf = StringIO(c_data)
        f = gzip.GzipFile(mode='rb', fileobj=buf)
        try:
            r_data = f.read()
        finally:
            f.close()
        return r_data


def main(appid,user):
    api = TLSSigAPI(appid, ecdsa_pri_key)
    sig = api.tls_gen_sig(user)
    print(sig)
    return sig