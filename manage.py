# -*- coding:utf-8 -*-
from iHome import create_app, db
from flask_migrate import Migrate, MigrateCommand, Manager

app = create_app('development')

manager = Manager(app)

Migrate(app, db)

manager.add_command('db', MigrateCommand)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis,因为是测试代码,暂时注释
    # redis_store.set('redis','test')

    return '月薪上万'


if __name__ == '__main__':
    manager.run()
