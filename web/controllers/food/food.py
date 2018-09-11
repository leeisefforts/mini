from flask import Blueprint, request, jsonify, redirect
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render, iPagination, getCurrentDate, getDictFilterField
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from common.models.food.FoodStockChangeLog import FoodStockChangeLog
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.libs.food.foodService import FoodService
from application import app, db
from sqlalchemy import or_
from decimal import Decimal

route_food = Blueprint("food_page", __name__)

@route_food.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Food.query
    if 'mix_kw' in req:
        rule = or_(Food.name.ilike("%{0}%".format(req['mix_kw'])), Food.tags.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter( rule )

    if 'status' in req and int( req['status'] ) > -1 :
        query = query.filter( Food.status == int( req['status'] ) )

    if 'cat_id' in req and int( req['cat_id'] ) > 0 :
        query = query.filter( Food.cat_id == int( req['cat_id'] ) )

    page_params = {
        'total':query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page':page,
        'display':app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page),"")
    }

    pages = iPagination( page_params )
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    list = query.order_by( Food.id.desc() ).offset( offset ).limit( app.config['PAGE_SIZE'] ).all()

    cat_mapping = getDictFilterField( FoodCat,FoodCat.id,"id",[] )
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "food/index.html",resp_data )

@route_food.route( "/info" )
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/food/index")

    if id < 1:
        return redirect( reback_url )

    info = Food.query.filter_by( id =id ).first()
    if not info:
        return redirect( reback_url )

    stock_change_list = FoodStockChangeLog.query.filter( FoodStockChangeLog.food_id == id )\
        .order_by( FoodStockChangeLog.id.desc() ).all()

    sale_change_list = FoodSaleChangeLog.query.filter( FoodSaleChangeLog.food_id == id )\
        .order_by( FoodSaleChangeLog.id.desc() ).all()

    resp_data['info'] = info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['sale_change_list'] = sale_change_list
    resp_data['current'] = 'index'
    return ops_render( "food/info.html",resp_data )

@route_food.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp = {}
        req = request.args
        cat_info = FoodCat.query.all()

        id = int(req.get("id", 0))

        info =None
        if id:
            info = Food.query.filter_by(id = id).first()

        resp['cat_info'] = cat_info
        resp['info'] = info
        return ops_render("food/set.html", resp)

    resp = {'code': 200 , 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else ''
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else 0
    main_image = req['main_image'] if 'main_image' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    stock = int(req['stock']) if 'stock' in req else 0
    tags = req['tags'] if 'tags' in req else ''

    price = Decimal(price).quantize(Decimal('0.00'))

    if cat_id < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类~~"
        return jsonify(resp)

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称~~"
        return jsonify(resp)

    if not price or  price  < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    price = Decimal(price).quantize(Decimal('0.00'))
    if  price <= 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    if main_image is None or len(main_image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图~~"
        return jsonify(resp)

    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入图书描述，并不能少于10个字符~~"
        return jsonify(resp)

    if stock < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的库存量~~"
        return jsonify(resp)

    if tags is None or len(tags) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入标签，便于搜索~~"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=id).first()
    before_stock = 0
    if food_info:
        model_food = food_info
        before_stock = model_food.stock
    else:
        model_food = Food()
        model_food.status = 1
        model_food.created_time = getCurrentDate()

    model_food.cat_id = cat_id
    model_food.name = name
    model_food.price = price
    model_food.main_image = main_image
    model_food.summary = summary
    model_food.stock = stock
    model_food.tags = tags
    model_food.updated_time = getCurrentDate()

    db.session.add(model_food)
    ret = db.session.commit()

    FoodService.setStockChangeLog(model_food.id, int(stock) - int(before_stock), "后台修改")

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


@route_food.route("/ops",methods=["POST"])
def ops():
    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in [ 'remove','recover' ]:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    food_info = Food.query.filter_by( id = id ).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "指定美食不存在~~"
        return jsonify(resp)

    if act == "remove":
        food_info.status = 0
    elif act == "recover":
        food_info.status = 1

    food_info.updated_time = getCurrentDate()
    db.session.add(food_info)
    db.session.commit()
    return jsonify( resp )
