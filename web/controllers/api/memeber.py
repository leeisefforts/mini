from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import requests, json

from common.libs.Helper import getCurrentDate
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.food.WxShareHistory import WxShareHistory
from common.libs.member.memberService import MemberService


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': "操作成功"}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = MemberService.getOpenId(code)

    nickname = req['nickName'] if 'nickName' in req else ''
    gender = req['gender'] if 'gender' in req else ''
    avatarUrl = req['avatarUrl'] if 'avatarUrl' in req else ''

    '''
        判断是否注册过
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = gender
        model_member.avatar = avatarUrl
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = getCurrentDate()
        model_member.created_time = getCurrentDate()

        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.created_time = getCurrentDate()
        model_bind.updated_time = getCurrentDate()

        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}

    return jsonify(resp)


@route_api.route("/member/check-reg", methods=["GET", "POST"])
def check_reg():
    resp = {'code': 200, 'msg': "操作成功"}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = MemberService.getOpenId(code)
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '未查询到绑定粉丝'
        return jsonify(resp)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)
