# -*- coding:utf-8 -*-

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)

class Config(object):
    SECRET_KEY = 'UL39UKjl9ol/GDSvjG3mp1nbt/Reaf4pzOgSO8enxvMXP/lCKQwKcnuOiE0mEOQB'
    """设置配置"""
    DEBUG = True
    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis的配置
    REDIS_HOST = '192.168.80.128' # 上传时记得修改成服务器的127.0.0.1
    REDIS_PORT = 6379

    # 设置session保存参数
    SESSION_TYPE = 'redis'
    # 设置和保存session的相关配置信息
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 开启session签名
    SESSION_USER_SIGNER = True
    # 设置Session生命周期
    PERMANENT_SESSION_LIFETIME = 172800



app.config.from_object(Config)

db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 开启csrf保护
CSRFProtect(app)
# 指定Session保存的位置
Session(app)

manager = Manager(app)

Migrate(app,db)

manager.add_command('db',MigrateCommand)


@app.route('/',methods=['GET','POST'])
def index():
    # 测试redis,因为是测试代码,暂时注释
    # redis_store.set('redis','test')

    return '月薪上万'

if __name__ == '__main__':
    manager.run()