import hashlib,base64, random, string,json
from application import app
from flask import jsonify, request
import requests
class MemberService():


    @staticmethod
    def geneAuthCode(member_info):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod
    def geneSalt(length = 16):
        keylist = [(random.choice(string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))



    @staticmethod
    def getOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
            app.config['APPID'], app.config['SECRET'], code)

        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid']
        return openid
