from flask import Flask
from werkzeug.utils import import_string
from device_manager.models import db
bps = {
        "borrow":'device_manager.views.borrow:borrow',
        "device":'device_manager.views.record:record',
        "login":'device_manager.views.login:login',
}

def create_app():
    # 配置额外连接的数据库

    SQLALCHEMY_BINDS = {
        'device':      'mysql://root:123456@mysql:3306/设备信息?charset=utf8',
        'record':      'mysql://root:123456@mysql:3306/借用记录?charset=utf8',
        'school':      'mysql://root:123456@mysql:3306/全院师生信息?charset=utf8',
        'user':        'mysql://root:123456@mysql:3306/用户账户数据?charset=utf8'
    }

    # 配置flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@mysql:3306/用户账户数据?charset=utf8'  #连接的数据库
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 自动commit #2.0之后被下面的配置代替了
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True  # 每次请求结束时自动commit数据库修改
    app.config["SQLALCHEMY_ECHO"] = False   # 如果设置成 True，SQLAlchemy将会记录所有发到标准输出(stderr)的语句,这对调试很有帮助.
    app.config["SQLALCHEMY_RECORD_QUERIES"] = None  # 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。
    app.config["SQLALCHEMY_POOL_SIZE"] = 5  # 数据库连接池的大小。默认是数据库引擎的默认值(通常是 5)。
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 10  # 指定数据库连接池的超时时间。默认是 10。
    app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS # 额外连接的数据库
    
    db.init_app(app) # 注册数据库
    db.reflect(app=app)  # 映射已有数据库

    for module  in bps:
        bp = import_string(bps[module])
        app.register_blueprint(bp,url_prefix='/%s'%module)
    return app
    