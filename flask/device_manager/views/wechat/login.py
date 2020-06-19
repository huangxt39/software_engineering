from device_manager.utils import *
from flask import Blueprint,request
from device_manager.models import *
login=Blueprint('login',__name__)

@login.route('/hello')
def show():
    return 'login.hello'

## 收到创建信息，创建然后返回
@login.route('/login.msg',methods=["POST"])
def login_msg():
    type_list = {"老师":1,"学生":2}
    id = request.values.get("id")
    wxid = request.values.get("wxid")
    type = request.values.get("type")
    new_user = User(wxid=wxid, user_type=type_list[type], user_id=id)
    # res = db.session.query(Pre_Manager).filter_by(account=username, password = password).first()
    db.session.add(new_user)
    db.session.commit()

    return "success"

## 收到文件，文件为图片，数据库保存图片的链接。图片统一保存在cards下。
@login.route('/upload',methods=["POST"])
def img_recieve():
    type_list = {"老师":1,"学生":2}
    img = request.files.get("upload")

    print(img)
    img.save("temp.png")
    # new_user = User(wxid=wxid, user_type=type_list[type], user_id=id)
    # db.session.add(new_user)
    # db.session.commit()

    return "temp.png"