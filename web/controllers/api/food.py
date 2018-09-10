from web.controllers.api import route_api
from flask import request, jsonify, g
from application import  app, db
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from common.models.member.MemberCart import MemberCart


@route_api.route("/food/index")
def foodIndex():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    cat_list = FoodCat.query.filter_by(status = 1).order_by(FoodCat.weight.desc())
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': '全部'
    })
    if cat_list:
        for item in cat_list:
            tmp_data = {
                'id':item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)

    food_list = Food.query.filter_by(status = 1).order_by(Food.total_count.desc(), Food.id.desc()).limit(3).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id':item.id,
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp['data']['banner_list'] = data_food_list
    resp['data']['cat_list'] = data_cat_list
    return jsonify(resp)

@route_api.route("/food/search")
def foodSearch():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    p = int(req['p']) if 'p' in req else 1
    if p < 1:
        p = 1
    mixkw = str(req['mix_kw']) if 'mix_kw' in req else ''

    query = Food.query.filter_by(status = 1)
    page_size = 10
    offset = (p - 1) * page_size
    if  cat_id > 0 :
        query = query.filter( Food.cat_id == int( req['cat_id'] ) )

    if mixkw:
        rule = or_(Food.name.ilike("%{0}%".format(mixkw)), Food.tags.ilike("%{0}%".format(mixkw)))
        query = query.filter( rule )

    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).offset(offset).limit(page_size).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)

@route_api.route("/food/info")
def foodInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = int(req['id']) if 'id' in req else 0
    food_info = Food.query.filter_by(id=id).first()

    if not food_info or not food_info.status:
        resp['code'] = -1
        resp['msg'] = "商品已下架"
        return jsonify(resp)
    member_info = g.member_info

    cart_number = 0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id = member_info.id).count()

    resp['data']['info'] = {
        'id': food_info.id,
        'name': food_info.name,
        'summary': food_info.summary,
        'total_count': food_info.total_count,
        'comment_count': food_info.comment_count,
        'main_image': UrlManager.buildImageUrl(food_info.main_image),
        'price': str(food_info.price),
        'stock': food_info.stock,
        'pics': [ UrlManager.buildImageUrl(food_info.main_image)]

    }
    resp['data']['cart_number'] = cart_number

    return jsonify(resp)