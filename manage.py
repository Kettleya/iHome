# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '月薪上万'

if __name__ == '__main__':
    app.run(debug=True,host='192.168.80.128')