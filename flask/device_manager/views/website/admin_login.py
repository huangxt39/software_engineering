from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, Markup, jsonify
from flask import Blueprint

admin_login=Blueprint('admin_login',__name__)


# @admin_login.route('/', methods=['GET'])
# def demo1():
#     return render_template('pratice/Login/login.html', input_text = '', res_text = '')


@admin_login.route('/login', methods=['GET', 'POST'])
def login():
  # print('请求头:%s' % request.headers)
    account = request.values.get("account")
    password = request.values.get("password")

    res = db.session.query(Manager).filter_by(account=account, password = password).first()
    if res==None:
        return jsonify({"code":0})
    else:
        return jsonify({"code":1})

@admin_login.route('/signup', methods=['GET', 'POST'])
def signup():
    account = request.values.get("email")
    password = request.values.get("password")
    user_id = request.values.get("user_id")
    name = request.values.get("name")
    email = account
    # email = request.form.get("email")
    phone = request.values.get("phone")
    description = request.values.get("description")

    ## 账号有没有被注册
    res = db.session.query(Pre_Manager).filter_by(account=account).first()
    if res is not None: # 查询为空，代表账号未被注册
        return jsonify({"code":0})
    ## 是否有这个人，匹配全校师生信息库
    res = db.session.query(School_information).filter(School_information.name ==name).\
        filter(School_information.id == user_id).all()
    if len(res) != 1: #没这个人
        return jsonify({"code":-1, "info": "全校师生表中没这个人"})

    # 查询学号是否被注册
    res = db.session.query(Pre_Manager).filter(Pre_Manager.user_id == user_id).all()
    if len(res):
        return jsonify({"code":-2, "info": "待注册的管理员表有这个人了"})

    # 查询学号是否被注册
    res = db.session.query(Manager).filter(Manager.user_id == user_id).all()
    if len(res):
        return jsonify({"code":-3, "info": "管理员表有这个人了"})

    #以上都没有问题才允许注册
    new_manager = Pre_Manager()
    new_manager.user_id = user_id
    new_manager.name=name
    new_manager.phone=phone
    new_manager.email=email
    new_manager.account=account
    new_manager.password=password
    new_manager.description=description
    db.session.add(new_manager)
    db.session.commit()
    return json.dumps({"code":1})

@admin_login.route('/read_signup', methods=['GET', 'POST'])
def read_signup():
    return_dict = {}

    page = request.values.get("page")
    per_page = request.values.get("per_page")

    if page is None:
        page = 0
    else:
        page = int(page)
    if per_page is None:
        per_page = 5
    else:
        per_page = int(per_page)

    ## 账号有没有被注册
    res = db.session.query(Pre_Manager).paginate(page, per_page, error_out=False)
    
    if res.items:
        items = query2dict(res.items)
        return_dict["pages"] =  res.pages
        # return_dict["per_page"] = num # num=2
        return_dict["result"] = items
        return_dict["total"] = res.total
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)


@admin_login.route('/check_signup', methods=['GET', 'POST'])
def check_signup():
    return_dict = {}
    account = request.values.get("account")
    
    ## 账号有没有被注册
    res = db.session.query(Pre_Manager).filter(Pre_Manager.account==account).all()
    if len(res) == 1: # 查询为空，代表账号未被注册
        pre_manager = res[0]
        new_manager = Manager()
        new_manager.user_id = pre_manager.user_id
        new_manager.name = pre_manager.name
        new_manager.phone = pre_manager.phone
        new_manager.email = pre_manager.email
        new_manager.account = pre_manager.account
        new_manager.password = pre_manager.password 
        new_manager.description  = pre_manager.description
        db.session.add(new_manager)
        db.session.delete(pre_manager)
        db.session.commit()
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)