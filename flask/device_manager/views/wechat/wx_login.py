from device_manager.utils import *
from flask import Blueprint,request, jsonify
from device_manager.models import *
import requests
from device_manager.views.wechat.utils import WXBizDataCrypt


wx_login=Blueprint('wx_login',__name__)

@wx_login.route('/hello')
def show():
    return 'login.hello'

@wx_login.route('/login',methods=["GET","POST"])
def login():
    return_dict = {}

    platCode = request.values.get("platCode")
    platUserInfoMap = request.values.get("platUserInfoMap")
    try:
        openid, session_key, userinfo = get_userinfo(platCode, platUserInfoMap)
    except:
        return jsonify({"code":-1,"info":"解码错误"})
    res =  db.session.query(User.wxid, User_type.user_type_name,\
        User.user_id, User.user_name, User.phone, User.email, User.photo,\
        User.money, User.violate, User.bor_now, User.bor_history, User.description).\
            filter(User.wxid == openid).\
            filter(User.user_type == User_type.user_type_id).all()
    if len(res) == 1:
        return_dict["result"] = query2dict(res)
        # return_dict["userinfo"] = userinfo
        return_dict["code"]=1
    else:
        return_dict["code"]=0
    return jsonify(return_dict)

@wx_login.route('/signup',methods=["POST"])
def signup():
    return_dict = {}
    type_list = {"老师":1,"学生":2}

    user_type = request.values.get("user_type")
    name = request.values.get("name")
    user_id = request.values.get("user_id")
    email = request.values.get("email")
    photo = request.values.get("photo")
    phone = request.values.get("phone")
    description = request.values.get("description")
    platCode = request.values.get("platCode")
    platUserInfoMap = request.values.get("platUserInfoMap")

    # try:
    openid, session_key, userinfo = get_userinfo(platCode, platUserInfoMap)
    if openid == '出现错误':
        return jsonify({'info':userinfo, "code": -1 })
    # except:
    #     return jsonify({"code":-1,"info":"解码错误"})
    #     openid = "testopenid"
    ## 有没有这个人
    res = db.session.query(School_information).filter_by(name=name, id=user_id).all()
    if len(res)!=1:
        return jsonify({"code":2, "info":"这个人不存在,学校竟然有多个人"})

    ## 账号有没有被注册
    res = db.session.query(User).filter_by(user_id = user_id).all()
    if len(res) > 0: # user_id重复，代表账号已注册
        return jsonify({"code":3, "info":"user_id重复，代表账号已注册"})
        
    res = db.session.query(User).filter_by(wxid = openid).all()
    if len(res) > 0: # openid重复，代表账号已注册
        return jsonify({"code":4, "info":"openid重复，代表账号已注册"})

    type_info = db.session.query(User_type).filter(User_type.user_type_name == user_type).first()

    new_user = User()

    new_user.user_type = type_info.user_type_id
    new_user.user_name = name 
    new_user.user_id =user_id
    new_user.email = email
    new_user.photo = photo 
    new_user.phone = phone 
    new_user.wxid = openid 
    new_user.money = type_info.wages
    new_user.bor_now = 0
    new_user.bor_history = 0
    new_user.violate = 0
    new_user.description = description
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"code":1, "openid":openid})

## 收到文件，文件为图片，数据库保存图片的链接。图片统一保存在cards下。
@wx_login.route('/upload',methods=["POST"])
def img_recieve():
    type_list = {"老师":1,"学生":2}
    img = request.files.get("upload")

    print(img)
    img.save("temp.png")
    # new_user = User(wxid=wxid, user_type=type_list[type], user_id=id)
    # db.session.add(new_user)
    # db.session.commit()

    return "temp.png"

@wx_login.route('/delete_account',methods=["GET","POST"])
def delete_account():
    return_dict = {}
    user_id = request.values.get("user_id")
    res = db.session.query(User).filter(User.user_id == user_id).all()
    if len(res) == 1:
        db.session.delete(res[0])
        db.session.commit()
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)



def get_userinfo(platCode, platUserInfoMap):
    ## hrh 测试用
    # appID = "wx5f653ad720e96dac" # 开发者关于微信小程序的appID
    # appSecret = "42190f18e8d326651f41c0041944e479" # 开发者关于微信小程序的appSecret
    
    ## hxt 实际用
    appID = "wx80549443a9478a48" # 开发者关于微信小程序的appID
    appSecret = "a0f3a4b2f7b0e5efbdf039bea64f88c2" # 开发者关于微信小程序的appSecret
    req_params = {
        "appid": appID,
        "secret": appSecret,
        "js_code": platCode,
        "grant_type": "authorization_code"
    }
    wx_login_api = "https://api.weixin.qq.com/sns/jscode2session"
    response_data = requests.get(wx_login_api, params=req_params) # 向API发起GET请求
    resData = response_data.json()
    # print(resData)
    try:
        openid = resData["openid"] # 得到用户关于当前小程序的OpenID
        session_key = resData ["session_key"] # 得到用户关于当前小程序的会话密钥session_key
        # encryptedData = platUserInfoMap["encryptedData"]
        # iv = platUserInfoMap["iv"]
        # pc = WXBizDataCrypt(appID, session_key) #对用户信息进行解密
        # userinfo = pc.decrypt(encryptedData, iv) #获得用户信息
        userinfo = None
    except:
        openid = '出现错误'
        session_key = '出现错误'
        userinfo = resData
    return openid, session_key, userinfo