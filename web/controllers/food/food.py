from flask import Blueprint, request, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from application import app, db
from sqlalchemy import or_

route_food = Blueprint("food_page", __name__)

@route_food.route("/index")
def index():
    resp = {}

    cat_info = FoodCat.query.order_by(FoodCat.id.desc()).all()
    resp['cat_info'] = cat_info
    return ops_render("food/index.html", resp)

@route_food.route("/info")
def info():
    return ops_render("food/info.html")

@route_food.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp = {}
        cat_info = FoodCat.query.order_by(FoodCat.id.desc()).all()
        resp['cat_info'] = cat_info
        return ops_render("food/set.html", resp)

    resp = {'code': 200 , 'msg': '操作成功', 'data': {}}
    req = request.values
    return jsonify(resp)

@route_food.route("/cat")
def cat():
    resq = {}
    req = request.values
    query = FoodCat.query
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in  req:
        rule = or_(FoodCat.name.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == int(req['status']))

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
    list = query.order_by(FoodCat.id.desc()).all()[offset: limit]
    resq['list'] = list
    resq['pages'] = pages
    resq['search_con'] = req
    resq['status_mapping'] = app.config['STATUS_MAPPING']

    return ops_render("food/cat.html", resq)

@route_food.route("/cat-set", methods=["GET","POST"])
def cat_set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))

        cat_info =None
        if id:
            cat_info = FoodCat.query.filter_by(id = id).first()

        resp_data['info'] = cat_info

        return ops_render("food/cat_set.html", resp_data)

    resp = {'code': 200 , 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else ''
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if 'weight' in req else 0

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = '分类名称填写不正确'
        return jsonify(resp)

    if weight is None or weight < 1:
        resp['code'] = -1
        resp['msg'] = '权重填写不正确'
        return jsonify(resp)

    food_info = FoodCat.query.filter_by(id = id).first()
    if food_info:
        model_food = food_info
    else:
        model_food = FoodCat()

    model_food.name = name
    model_food.weight = weight
    model_food.updated_time = getCurrentDate()
    model_food.created_time = getCurrentDate()

    db.session.add(model_food)
    db.session.commit()

    return jsonify(resp)


@route_food.route("/cat-ops", methods=["POST"])
def cat_ops():
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

    info = FoodCat.query.filter_by(id=id).first()

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