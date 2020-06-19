from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup
from flask import Blueprint

admin_signup=Blueprint('admin_signup',__name__)

@admin_signup.route('/signup', methods=['GET', 'POST'])
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
    if res==None: # 查询为空，代表账号未被注册
        return json.dumps({"code":2})
    ## 是否有这个人，匹配全校师生信息库
    res = db.session.query(School_information).filter_by(name=name, user_id=user_id).first()
    if res==None:
        return json.dumps({"code":3})

    # 查询学号是否被注册
    res = db.session.query(Pre_Manager).filter_by(user_id = user_id).first()
    if res==None:
        return json.dumps({"code":4})

    #以上都没有问题才允许注册
    new_manager = Pre_Manager(user_id = user_id, name=name, phone=phone, email=email, account=account, password=password,description=description)
    db.session.add(new_manager)
    db.session.commit()
    return json.dumps({"code":1})


# @admin_signup.route('/login', methods=['GET', 'POST'])
# def demo1():
#   if request.method == 'GET':
#     return render_template('pratice/Login/login.html', input_text = '', res_text = '')
#   else:
#     inputText = request.form.get("input_text")
#     print(inputText)
#     resText = Markup(formatRes(reverseText(inputText)))
#     return render_template('login.html', input_text = inputText, res_text = resText)
