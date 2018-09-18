from flask import Flask, jsonify
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

# 短信应用SDK AppID
appid = 1400138188  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = "eade28744ae7ba5809f8c4ba63f25cc2"

# 需要发送短信的手机号码
phone_numbers = ["18616396821", "18873221767"]

# 短信模板ID，需要在短信应用中申请
template_id = 192051  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
# templateId 7839 对应的内容是"您的验证码是: {1}"
# 签名
sms_sign = "Honey"


class JobTask():
    def __init__(self):
        pass

    def run(self, params):
        ssender = SmsSingleSender(appid, appkey)
        params = ["钥匙手机充电器记得带!~",
                  "2"]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
        try:
            for i in phone_numbers:
                result = ssender.send_with_param(86, i,
                                                 template_id, params, sign=sms_sign, extend="",
                                                 ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信

        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
