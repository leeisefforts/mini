from flask import Blueprint, request , jsonify, make_response, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from application import app, db
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render

import json
route_user = Blueprint("user_page", __name__)

@route_user.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return ops_render("user/login.html")

    result = {'code': 200, 'msg': '操作成功'}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        return jsonify(result)

    if login_pwd is None or len(login_pwd) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        return jsonify(result)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        result['code'] = -1
        result['msg'] = '账号错误'
        return jsonify(result)

    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        result['code'] = -1
        result['msg'] = '密码错误'
        return jsonify(result)

    if user_info.status == -1:
        result['code'] = -1
        result['msg'] = '账号失效'
        return jsonify(result)

    response = make_response(json.dumps(result))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))


    return response

@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html",  {'current': 'edit'})

    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    resq = {
        'code': 200,
        'msg': '操作成功',
        'data': {}
    }

    if nickname is None or len(nickname) < 1:
        resq['code'] = -1
        resq['msg'] = '操作失败'
        return jsonify(resq)

    if email is None or len(email) < 1:
        resq['code'] = -1
        resq['msg'] = '操作失败'
        return jsonify(resq)

    user_info = g.current_user

    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()

    return jsonify(resq)


@route_user.route("/reset_pwd", methods = ["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html", {'current': 'reset'})

    resq = {
        'code': 200,
        'msg': '操作成功',
        'data': {}
    }

    rep = request.values

    oldpassword = rep['old_password'] if 'old_password' in rep else ''
    newpassword = rep['new_password'] if 'new_password' in rep else ''

    if oldpassword is None or len(oldpassword) < 1:
        resq['code'] = -1
        resq['msg'] = '操作失败'
        return jsonify(resq)

    if newpassword is None or len(newpassword) < 1:
        resq['code'] = -1
        resq['msg'] = '操作失败'
        return jsonify(resq)

    if oldpassword == newpassword:
        resq['code'] = -1
        resq['msg'] = '新旧密码重复'
        return jsonify(resq)



    user_info = g.current_user

    if user_info.login_pwd != UserService.genePwd(oldpassword, user_info.login_salt):
        resq['code'] = -1
        resq['msg'] = '原密码错误'
        return jsonify(resq)

    user_info.login_pwd = UserService.genePwd(newpassword, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()

    # 刷新cookie
    response = make_response(json.dumps(resq))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))


    return jsonify(resq)

@route_user.route("/logout")
def logout():
    response = make_response(redirect((UrlManager.buildUrl("/user/login"))))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response