from flask import Flask
from werkzeug.utils import import_string
from device_manager.models import db
import device_manager.utils.global_var as gol
from flask_cors import *

root = "mysql"
root = "108.166.209.115"

bps = {
        "wx_borrow":'device_manager.views.wechat.wx_borrow:wx_borrow',
        "wx_device":'device_manager.views.wechat.wx_device:wx_device',
        "wx_login":'device_manager.views.wechat.wx_login:wx_login',
        "wx_record":'device_manager.views.wechat.wx_record:wx_record',
        "wx_user":'device_manager.views.wechat.wx_user:wx_user',
        "test":'device_manager.views.test:test',
        "admin_login":'device_manager.views.website.admin_login:admin_login',
        # "admin_signup":'device_manager.views.website.admin_signup:admin_signup',
        "admin_problem":'device_manager.views.website.admin_problem:admin_problem',
        "admin_user":'device_manager.views.website.admin_user:admin_user',
        "admin_device":'device_manager.views.website.admin_device:admin_device',
        "admin_record":'device_manager.views.website.admin_record:admin_record',
}

def create_app():
    # 配置额外连接的数据库
    
    SQLALCHEMY_BINDS = {
        'manager':      'mysql://root:123456@%s:3306/设备管理?charset=utf8'%root,
        'device':      'mysql://root:123456@%s:3306/设备信息?charset=utf8'%root,
        'record':      'mysql://root:123456@%s:3306/借用记录?charset=utf8'%root,
        'school':      'mysql://root:123456@%s:3306/全院师生信息?charset=utf8'%root,
        'user':        'mysql://root:123456@%s:3306/用户账户数据?charset=utf8'%root
    }

    # 配置flask
    app = Flask(__name__)
    
    CORS(app, supports_credentials=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@108.166.209.115:3306/设备管理?charset=utf8'  #连接的数据库
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 自动commit #2.0之后被下面的配置代替了
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True  # 每次请求结束时自动commit数据库修改
    app.config["SQLALCHEMY_ECHO"] = False   # 如果设置成 True，SQLAlchemy将会记录所有发到标准输出(stderr)的语句,这对调试很有帮助.
    app.config["SQLALCHEMY_RECORD_QUERIES"] = None  # 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。
    app.config["SQLALCHEMY_POOL_SIZE"] = 5  # 数据库连接池的大小。默认是数据库引擎的默认值(通常是 5)。
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 10  # 指定数据库连接池的超时时间。默认是 10。
    app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS # 额外连接的数据库

    app.config['JSON_AS_ASCII'] = False # json.jsonify支持中文解析
    
    app.debug = True # 开启debug模式

    db.init_app(app) # 注册数据库
    db.reflect(app=app)  # 映射已有数据库

    for module  in bps:
        bp = import_string(bps[module])
        app.register_blueprint(bp,url_prefix='/%s'%module)
    if(app.debug): gol.set_value("debug",1)
    return app
    