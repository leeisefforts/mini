from flask import Blueprint, redirect, jsonify
from common.libs.Helper import ops_render, iPagination , getCurrentDate
from flask import request
from application import app, db
from common.models.member.Member import Member
from sqlalchemy import or_
from common.libs.UrlManager import UrlManager

route_member = Blueprint("member_page", __name__)

@route_member.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    query = Member.query
    if 'mix_kw' in  req:
        rule = or_(Member.nickname.ilike("%{0}%".format(req['mix_kw'])), Member.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    count = query.count()
    page_params = {
        'total': count,
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset =  (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    list = query.order_by(Member.id.desc()).all()[offset: limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("member/index.html", resp_data)

@route_member.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))
    if id < 1:
        return redirect(UrlManager.buildUrl("member/index"))

    info = Member.query.filter_by(id = id).first()
    if not info:
        return redirect(UrlManager.buildUrl("member/index"))

    resp_data['info'] = info
    return ops_render("member/info.html", {'info': info})

@route_member.route("/set", methods= ["GET", "POST"])
def set():
    if request.method =="GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))

        info =None
        if id:
            info = Member.query.filter_by(id = id).first()

        resp_data['info'] = info

        return ops_render("member/set.html", resp_data)

    resp = {'code': 200 , 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '昵称填写不正确'
        return jsonify(resp)

    info = Member.query.filter_by(id=id).first()
    info.nickname = nickname
    info.updated_time = getCurrentDate()

    db.session.add(info)
    db.session.commit()

    return jsonify(resp)

@route_member.route("/ops", methods=["GET", "POST"])
def member_ops():
    resp = {
        'code': 200,
        'msg':'操作成功',
        'data': {}
    }

    req = request.values
    id = req['id'] if 'id' in req else ''
    act = req['act'] if 'act' in req else ''


    if not id:
        resp['code'] = -1
        resp['msg'] = "操作失败1"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['act'] = -1
        resp['act'] = "操作失败2"
        return jsonify(resp)

    info = Member.query.filter_by(id=id).first()

    if not info:
        resp['code'] = -1
        resp['msg'] = "操作失败3"

    if act == "remove":
        info.status = 0
    elif act == "recover":
        info.status = 1

    info.updated_time = getCurrentDate()
    db.session.add(info)
    db.session.commit()

    return jsonify(resp)


@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html")