from flask import Blueprint, request, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from application import app, db
from sqlalchemy import or_

route_food = Blueprint("food_page", __name__)

@route_food.route("/index")
def index():
    return ops_render("food/index.html")

@route_food.route("/info")
def info():
    return ops_render("food/info.html")

@route_food.route("/set")
def set():
    return ops_render("food/set.html")

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

@route_food.route("/cat-set")
def cat_set():
    return ops_render("food/cat_set.html")