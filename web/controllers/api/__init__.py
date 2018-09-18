from flask import  Blueprint

route_api = Blueprint('api_page', __name__)
from web.controllers.api.memeber import *
from web.controllers.api.food import *
from web.controllers.api.cart import *
from web.controllers.api.order import *
from web.controllers.api.my import *
from web.controllers.api.address import *
from web.controllers.api.dx import *

@route_api.route("/")
def index():
    return "Mina Api"