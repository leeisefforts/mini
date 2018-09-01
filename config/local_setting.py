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
    "^/user/login"
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