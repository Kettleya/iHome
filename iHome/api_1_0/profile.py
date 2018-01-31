# -*- coding:utf-8 -*-
from flask import current_app, jsonify
from flask import g

from iHome.api_1_0 import api
from iHome.models import User
from iHome.utils.common import login_required
from iHome.utils.response_code import RET


@api.route('/user')
@login_required
def get_user_info():
    """
    1.取到当前用户的id
    2.查询指定的用户信息
    3.组织数据,进行返回
    :return:
    """

    # 1.取到当前用户的id
    user_id = g.user_id

    # 2.查询指定的用户信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 3.组织数据,进行返回
    return jsonify(errno=RET.OK, errmsg='OK',data=user.to_dict())