# -*- coding:utf-8 -*-
# 验证码的提供：图片验证码和短信验证码
from flask import abort
from flask import make_response
from flask import request, jsonify

from iHome import constants
from iHome.utils.response_code import RET
from . import api
from iHome import redis_store
from iHome.utils.captcha.captcha import captcha


@api.route("/image_code")
def get_image_code():
    """
    图片验证码的视图函数
    1. 取到图片编码
    2. 生成图片验证码
    3. 将图片验证码内容通过图片编码保存到redis中
    4. 返回图片

    :return:
    """

    # 1. 取到图片编码
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    if not cur_id:
        abort(403)

    # 2. 生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 3. 将图片验证码内容通过图片编码保存到redis中
    try:
        redis_store.set("ImageCode:" + cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete("ImageCode:" + pre_id)
    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR, errmsg="保存验证码数据失败")

    # 返回图片验证码的图片
    response = make_response(image)
    # 设置响应的内容类型
    response.headers["Content-Type"] = "image/jpg"
    # 进行返回
    return response
