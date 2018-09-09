from web.controllers.api import route_api
from flask import request, jsonify, g
from application import  app, db
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.food.Food import Food
from common.libs.cart.cartService import CartService


@route_api.route("/cart/set", methods = ["POST"])
def setCart():
    resp = {'code': 200, 'msg': "操作成功"}
    req = request.values

    food_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0

    if food_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = "添加失败 - 1"
        return jsonify(resp)

    member_info = g.member_info

    if not member_info:
        resp['code'] = -1
        resp['msg'] = "添加失败 - 2"
        return jsonify(resp)

    food_info = Food.query.filter_by(id = food_id).first()

    if not food_info:
        resp['code'] = -1
        resp['msg'] = "添加失败 - 3"
        return jsonify(resp)

    if food_info.stock < number:
        resp['code'] = -1
        resp['msg'] = "库存不足"
        return jsonify(resp)

    ret = CartService.setItems(member_id= member_info.id, food_id= food_id, number=number)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "添加失败 - 4"
        return jsonify(resp)

    return jsonify(resp)