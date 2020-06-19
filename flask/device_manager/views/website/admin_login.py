from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup, jsonify
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