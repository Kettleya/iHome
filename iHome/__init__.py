# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
import redis
from config import config
from iHome.utils.common import RegexConverter

db = SQLAlchemy()

redis_store = None


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # db = SQLAlchemy(app)
    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)

    # 开启CSRF保护
    CSRFProtect(app)
    # 指定Session保存的位置
    Session(app)

    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图,再使用时引入
    from iHome.api_1_0 import api
    app.register_blueprint(api,url_prefix='/api/v1.0')

    from web_html import html
    app.register_blueprint(html)


    return app
