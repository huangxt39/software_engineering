from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup
from flask import Blueprint
import device_manager.utils.global_var as gol

admin_user=Blueprint('admin_user',__name__)

@admin_user.route('/query', methods=['GET','POST'])
def user_query():
    return_dict = {}

    if gol.get_value("debug"):
        print("bebug mode auto input user_query")
        # order = 1
        num = 5
    else:
        # order = request.values.get("order")
        query_type = request.values.get("query_type")
        num = request.values.get("num")

    if request.method == "GET":
        res = db.session.query(User.wxid, User_type.user_type_name, User.user_name, User.phone, User.email, User.photo).\
            filter(User.user_type == User_type.user_type_id).all()
        num = min(3,len(res))
        res = res[:num]
        # print(res)        
        # print(type(res[0]))
        # print(type(res[0][0]))
        res = query2dict(res)
        return_dict["index"] = num # num=2
        return_dict["result"] = res
        return_dict["code"] = 1
    elif request.method == "POST":
        if gol.get_value("debug"):
            print("bebug mode auto input user_query")
            # order = 1
            num = 3
            query_type = 2
        else:
            query_type = request.values.get("query_type")
            num = request.values.get("num")
        if(query_type == 0):  ## 用户名检索
            user_name = request.values.get("user_name")
            # user_name = "黄润辉"
            res = db.session.query(User.wxid, User_type.user_type_name, User.user_name, User.phone, User.email, User.photo).\
                filter(User.user_type == User_type.user_type_id).\
                    filter(User.user_name.like("%"+user_name+"%")).all()
        elif(query_type == 1):  ## 用户类型检索
            user_type = request.values.get("user_type")
            # user_type = "学生"
            res = db.session.query(User.wxid, User_type.user_type_name, User.user_name, User.phone, User.email, User.photo).\
                filter(User.user_type == User_type.user_type_id).\
                    filter(User_type.user_type_name == user_type).all()
        elif(query_type == 2):  ## 用户id检索
            user_id = request.values.get("user_id")
            # user_id = "17363031"
            res = db.session.query(User.wxid, User_type.user_type_name, User.user_name, User.phone, User.email, User.photo).\
                filter(User.user_type == User_type.user_type_id).\
                    filter(User.user_id == user_id).all()
        else:
            user_id = request.values.get("user_id")
            res = db.session.query(User.wxid, User_type.user_type_name, User.user_name, User.phone, User.email, User.photo).\
                filter(User.user_type == User_type.user_type_id).\
                    filter(User.user_id == user_id).all()
        num = min(3,len(res))
        res = res[:num]
        # print(res)
        res = query2dict(res)
        return_dict["index"] = num # num=2
        return_dict["result"] = res
        return_dict["code"] = 2
    else:
        return_dict["code"] = -1

    return json.dumps(return_dict, cls=DateEncoder, ensure_ascii=False)

