from device_manager.utils import *
from flask import Blueprint,request, jsonify
from device_manager.models import *
import requests
from device_manager.views.wechat.utils import WXBizDataCrypt


wx_login=Blueprint('wx_login',__name__)

@wx_login.route('/hello')
def show():
    return 'login.hello'

# ## 收到创建信息，创建然后返回
# @wx_login.route('/login',methods=["POST"])
# def login():
#     type_list = {"老师":1,"学生":2}
#     id = request.values.get("id")
#     wxid = request.values.get("wxid")
#     type = request.values.get("type")
#     new_user = User(wxid=wxid, user_type=type_list[type], user_id=id)
#     # res = db.session.query(Pre_Manager).filter_by(account=username, password = password).first()
#     db.session.add(new_user)
#     db.session.commit()

#     return "success"

@wx_login.route('/login',methods=["GET","POST"])
def login():
    return_dict = {}
    # print('请求头:%s' % request.headers)

    data = json.loads(request.get_data().decode("utf-8")) # 将前端Json数据转为字典
    # appID = "appID" # 开发者关于微信小程序的appID
    # appID = "wx5f653ad720e96dac" # 开发者关于微信小程序的appID
    # appSecret = "42190f18e8d326651f41c0041944e479" # 开发者关于微信小程序的appSecret
    # code = data["platCode"] # 前端POST过来的微信临时登录凭证code
    # encryptedData = data["platUserInfoMap"]["encryptedData"]
    # iv = data["platUserInfoMap"]["iv"]
    # req_params = {
    #     "appid": appID,
    #     "secret": appSecret,
    #     "js_code": code,
    #     "grant_type": "authorization_code"
    # }
    # wx_login_api = "https://api.weixin.qq.com/sns/jscode2session"
    # response_data = requests.get(wx_login_api, params=req_params) # 向API发起GET请求
    # resData = response_data.json()
    # print(resData)
    # openid = resData ["openid"] # 得到用户关于当前小程序的OpenID
    # session_key = resData ["session_key"] # 得到用户关于当前小程序的会话密钥session_key
    openid, session_key, userinfo = get_userinfo(data["platCode"], data["platUserInfoMap"])
    # pc = WXBizDataCrypt(appID, session_key) #对用户信息进行解密
    # userinfo = pc.decrypt(encryptedData, iv) #获得用户信息
    # print(userinfo)
    res =  db.session.query(User.wxid, User_type.user_type_name,\
        User.user_id, User.user_name, User.phone, User.email, User.photo).\
            filter(User.wxid == openid).\
            filter(User.user_type == User_type.user_type_id).all()
    if len(res) != 1:
        return_dict["code"]=0
    return_dict["result"] = query2dict(res[0])
    return_dict["userinfo"] = userinfo
    return_dict["code"]=1

    return jsonify(return_dict)

@wx_login.route('/signup',methods=["POST"])
def signup():
    return_dict = {}
    type_list = {"老师":1,"学生":2}

    user_type = request.values.get("user_type")
    name = request.values.get("name")
    user_id = request.values.get("user_id")
    email = request.values.get("phont")
    photo = request.values.get("photo")

    platCode = request.values.get("platCode")
    platUserInfoMap = request.values.get("platUserInfoMap")

    try:
        openid, session_key, userinfo = get_userinfo(platCode, platUserInfoMap)
    except:
        openid = "testopenid"
    ## 有没有这个人
    res = db.session.query(School_information).filter_by(name=name, id=user_id).first()
    if res is not None:
        return json.dumps({"code":2})

    ## 账号有没有被注册
    res = db.session.query(User).filter_by(user_id = user_id).first()
    if res is not None: # 查询为空，代表账号未被注册
        return json.dumps({"code":3})
        

    res = db.session.query(User).filter_by(wxid = openid).first()
    if res is not None: # 查询为空，代表账号未被注册
        return json.dumps({"code":3})

    new_user = User()

    new_user.user_type = user_type 
    new_user.name = name 
    new_user.user_id =user_id
    new_user.email = email
    new_user.photo = photo 
    new_user.wxid = openid 
    db.session.add(new_user)
    db.session.commit()

    return json.dumps({"code":1, "openid":openid})

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



def get_userinfo(platCode, platUserInfoMap):
    appID = "wx5f653ad720e96dac" # 开发者关于微信小程序的appID
    appSecret = "42190f18e8d326651f41c0041944e479" # 开发者关于微信小程序的appSecret
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
    openid = resData["openid"] # 得到用户关于当前小程序的OpenID
    session_key = resData ["session_key"] # 得到用户关于当前小程序的会话密钥session_key
    encryptedData = platUserInfoMap["encryptedData"]
    iv = platUserInfoMap["iv"]
    pc = WXBizDataCrypt(appID, session_key) #对用户信息进行解密
    userinfo = pc.decrypt(encryptedData, iv) #获得用户信息
    return openid, session_key, userinfo