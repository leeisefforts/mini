DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wechat_db_u:aTalent2018!@52.80.48.214/mina'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"
SQLALCHEMY_BINDS = {
    'mina': "mysql+pymysql://wechat_db_u:aTalent2018!@52.80.48.214/mina"
}

AUTH_COOKIE_NAME = "UserCookie"

## 过滤url
IGNORE_URLS = [
    "^/user/login",
    "^/upload"

]


API_IGNORE_URLS = [
    "^/api"
]


IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

PAGE_SIZE = 20
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "删除"
}

MINA_APP = {
    'appid':'wx1f244139ab0c54c8',
    'appkey':'6e4fab0d29a50571678ba1559e627ebc',
    'paykey':'TM8KwVFRlp0hsTWMQTxLplfFIzmk7csr',
    'mch_id':'1513434041',
    'callback_url':'/api/order/callback'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'png', 'jpeg'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain':'http://127.0.0.1:5000'
}

PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}