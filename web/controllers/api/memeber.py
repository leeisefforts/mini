from web.controllers.api import route_api
from flask import request, jsonify
from application import  app, db
import requests, json

from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind

@route_api.route("/member/login", methods =["GET", "POST"])
def login():
    resp = {'code': 200 , 'msg': "操作成功"}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) <1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(app.config['APPID'], app.config['SECRET'], code)

    r = requests.get(url)
    res = json.loads(r.text)
    openid = res['openid']


    return jsonify(resp)