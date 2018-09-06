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
    "^/api",
    "^/upload"

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

APPID = "wx1f244139ab0c54c8"
SECRET = "6e4fab0d29a50571678ba1559e627ebc"

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'png', 'jpeg'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain':'http://127.0.0.1:5000'
}