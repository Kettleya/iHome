# -*- coding:utf-8 -*-

from flask import Blueprint,current_app

html = Blueprint('html',__name__)


@html.route('/<re(".*"):file_name>')
def get_html_file(file_name):
    if not file_name:
        file_name = 'index.html'

    # 判断是否是图标,如果不是图标,拼接url
    if file_name != 'favicon.ico':
        file_name = 'html/'+file_name
    # send_static_file: 通过指令找到指定的static文件并封装成响应
    return current_app.send_static_file(file_name)

