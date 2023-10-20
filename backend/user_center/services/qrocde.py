# -*- coding: utf-8 -*-

from application import dispatch
from wechatpy import WeChatClient
import base64

# 小程序码相关
class QrcodeService():

    def __init__(self):
        self.client = WeChatClient(
            dispatch.get_system_config_values("wxpay_config.APPID"),
            dispatch.get_system_config_values("wxpay_config.SECRET"),
        )
    
    # 接口B：适用于需要的码数量极多，或仅临时使用的业务场景
    def unlimited(self, scene, width=430, auto_color=False, line_color={'b': '0', 'g': '0', 'r': '0'}, page=None, is_hyaline=False):
        res = self.client.wxa.get_wxa_code_unlimited(scene, width, auto_color, line_color, page, is_hyaline)
        # 把原始字节码编码成 base64 字节码
        base64_bytes = base64.b64encode(res.content)
        # 将 base64 字节码解码成 utf-8 格式的字符串
        base64_string = base64_bytes.decode('utf-8')
        return base64_string