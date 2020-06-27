from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, Markup, jsonify
from flask import Blueprint

admin_login=Blueprint('admin_login',__name__)


@admin_login.route('/', methods=['GET'])
def demo1():
    return render_template('pratice/Login/login.html', input_text = '', res_text = '')


@admin_login.route('/login', methods=['GET', 'POST'])
def login():
  # print('请求头:%s' % request.headers)
  if request.method == 'GET':
    return json.dumps({"code":0})
  else:
    account = request.values.get("account")
    password = request.values.get("password")

    res = db.session.query(Manager).filter_by(account=account, password = password).first()
    if res==None:
        return jsonify({"code":0})
    else:
        return jsonify({"code":1})

@admin_login.route('/signup', methods=['GET', 'POST'])
def signup():
    account = request.form.get("email")
    password = request.form.get("password")
    user_id = request.form.get("user_id")
    email = account
    # email = request.form.get("email")
    photo = request.form.get("photo")
    description = request.form.get("description")

    ## 账号有没有被注册
    res = db.session.query(Pre_Manager).filter_by(account=account).first()
    if res is not None: # 查询为空，代表账号未被注册
        return json.dumps({"code":2})
    ## 是否有这个人，匹配全校师生信息库
    res = db.session.query(School_information).filter_by(name=name, user_id=user_id).first()
    if res is not None:
        return json.dumps({"code":3})

    # 查询学号是否被注册
    res = db.session.query(Pre_Manager).filter_by(user_id = user_id).first()
    if res is not None:
        return json.dumps({"code":4})

    #以上都没有问题才允许注册
    new_manager = Pre_Manager(user_id = user_id, name=name, phone=phone, email=email, account=account, password=password,description=description)
    db.session.add(new_manager)
    db.session.commit()
    return json.dumps({"code":1})


# @admin_login.route('/login/index', methods=['GET', 'POST'])
# def demo2():
#   if request.method == 'GET':
#     print("GET")
#     return json.dumps({"code":-1})
#     # return render_template('pratice/Login/index.html', input_text = '', res_text = '')
#   else:
#     print("POST")
#     username = request.form.get("loginusername")
#     password = request.form.get("loginpassword")
#     # qyname = request.form.get("qyname")
#     # qyusername = request.form.get("qyusername")
#     res = db.session.query(Manager).filter_by(account=username, password = password).first()
#     # res = db.session.query.filter_by(id='17363031').with_entities(School_information.id,School_information.type,School_information.name).all()
#     print(username)
#     print(password)
#     print(res)
#     if res==None:
#         return json.dumps({"code":0})
#     else:
#         # res_json = list_dict_to_json(res)
#         # print(res_json)
#         return json.dumps({"code":1})


# def formatRes(textList):
#   return '<p>' + '</p><p>'.join(textList) + '</p>'

# # A sample
# def reverseText(text):
#   res = []
#   res.append('Original text: %s' %(text))
#   res.append('Converted text: %s' %(''.join(reversed(list(text)))))
#   return res