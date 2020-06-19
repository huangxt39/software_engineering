from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup
from flask import Blueprint

test=Blueprint('test',__name__)

@test.route('/', methods=['GET', 'POST'])
def demo():
    return render_template('index.html', input_text = '', res_text = '')
    
def formatRes(textList):
  return '<p>' + '</p><p>'.join(textList) + '</p>'

# A sample
def reverseText(text):
  res = []
  res.append('Original text: %s' %(text))
  res.append('Converted text: %s' %(''.join(reversed(list(text)))))
  return res

@test.route('/login', methods=['GET', 'POST'])
def demo1():
  if request.method == 'GET':
    return render_template('pratice/Login/login.html', input_text = '', res_text = '')
  else:
    inputText = request.form.get("input_text")
    print(inputText)
    resText = Markup(formatRes(reverseText(inputText)))
    return render_template('login.html', input_text = inputText, res_text = resText)

@test.route('/login/index', methods=['GET', 'POST'])
def demo2():
  if request.method == 'GET':
    print("GET")
    return json.dumps({"code":-1})
    # return render_template('pratice/Login/index.html', input_text = '', res_text = '')
  else:
    print("POST")
    username = request.form.get("loginusername")
    password = request.form.get("loginpassword")
    # qyname = request.form.get("qyname")
    # qyusername = request.form.get("qyusername")
    res = db.session.query(Manager).filter_by(account=username, password = password).first()
    # res = db.session.query.filter_by(id='17363031').with_entities(School_information.id,School_information.type,School_information.name).all()
    print(username)
    print(password)
    print(res)
    if res==None:
        return json.dumps({"code":0})
    else:
        # res_json = list_dict_to_json(res)
        # print(res_json)
        return json.dumps({"code":1})
    # print(qyname)
    # print(qyusername)
    # resText = Markup(formatRes(reverseText(inputText)))
    # resText = Markup(formatRes(reverseText(inputText)))
    # resText = Markup(formatRes(reverseText(inputText)))
    # return 1
    # return render_template('pratice/Login/index.html', input_text = inputText, res_text = resText)

