from flask import Blueprint, render_template, request , jsonify
from common.models.User import User
from common.libs.user.UserService import UserService
route_user = Blueprint("user_page", __name__)

@route_user.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")

    result = {'code': 200, 'msg': 'Login Success'}
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

    return jsonify(result)

@route_user.route("/edit")
def edit():
    return render_template("user/edit.html")

@route_user.route("/reset-pwd")
def resetPwd():
    return render_template("user/reset_pwd.html")