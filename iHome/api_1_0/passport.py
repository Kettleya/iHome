# -*- coding:utf-8 -*-

from flask import current_app, jsonify
from flask import request

from iHome import redis_store, db
from iHome.models import User
from iHome.utils.response_code import RET
from . import api


@api.route('/users', methods=['POST'])
def register():
    """
    1.获取json参数,并转换为python字典,并校验参数
    2.取到真实的短信验证码
    3.对比短信验证码是否与真实验证码匹配
    4.初始化user,保存相关数据
    5.将数据存储到数据库
    6.给出响应
    :return:
    """
    # 1.获取json参数
    data_dict = request.json
    mobile = data_dict.get('mobile')
    phonecode = data_dict.get('phonecode')
    password = data_dict.get('password')

    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2.取到真实的短信验证码
    try:
        real_phonecode = redis_store.get(mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查询短信验证码失败')

    if not real_phonecode:
        return jsonify(errno=RET.NODATA,errmsg='短信验证码已经过期')

    # 3.进行短信验证码的对比
    if real_phonecode != phonecode:
        return jsonify(errno=RET.DATAERR,errmsg='短信验证码输入错误')

    # 4.初始化User,保存相关数据
    user = User()
    user.mobile = mobile
    user.name = mobile
    # 保存密码
    user.password = password

    # 5.将数据存入数据库中
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存用户数据失败')

    # 6.给出响应
    return jsonify(errno=RET.OK,errmsg='注册成功')