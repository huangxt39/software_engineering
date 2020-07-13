from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup
from flask import Blueprint,jsonify
import device_manager.utils.global_var as gol

admin_user=Blueprint('admin_user',__name__)

@admin_user.route('/query', methods=['GET','POST'])
def user_query():
    return_dict = {}

    query_type = request.values.get("query_type")
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
    if request.method == "GET":
        res = db.session.query(User.wxid, User_type.user_type_name,\
                 User.user_name, User.phone, User.email, User.photo,\
                     User.bor_now, User.bor_history, User.violate,\
                         User.description).\
            filter(User.user_type == User_type.user_type_id).paginate(page, per_page, error_out=False)

        return_dict["pages"] = res.pages
        return_dict["total"] = res.total
        return_dict["result"] = query2dict(res.items)
        return_dict["code"] = 1
    elif request.method == "POST":
        query_type = request.values.get("query_type")
        query_type = int(query_type)
        if(query_type == 0):  ## 用户名检索
            user_name = request.values.get("user_name")
            # user_name = "黄润辉"
            if user_name:
                res = db.session.query(User.wxid, User_type.user_type_name,\
                    User.user_name, User.phone, User.email, User.photo,\
                        User.bor_now, User.bor_history, User.violate,\
                            User.description).\
                    filter(User.user_type == User_type.user_type_id).\
                        filter(User.user_name.like("%"+user_name+"%")).paginate(page, per_page, error_out=False)
            else:
                return_dict["code"] = -4
                return_dict["info"] = "user_name呢?"
                return jsonify(return_dict)
        elif(query_type == 1):  ## 用户类型检索
            user_type = request.values.get("user_type")
            # user_type = "学生"
            if user_type:
                res = db.session.query(User.wxid, User_type.user_type_name,\
                    User.user_name, User.phone, User.email, User.photo,\
                        User.bor_now, User.bor_history, User.violate,\
                            User.description).\
                    filter(User.user_type == User_type.user_type_id).\
                        filter(User_type.user_type_name == user_type).paginate(page, per_page, error_out=False)
            else:
                return_dict["code"] = -3
                return_dict["info"] = "user_type呢?"
                return jsonify(return_dict)
        elif(query_type == 2):  ## 用户id检索
            user_id = request.values.get("user_id")
            # user_id = "17363031"
            if user_id:
                res = db.session.query(User.wxid, User_type.user_type_name,\
                    User.user_name, User.phone, User.email, User.photo,\
                        User.bor_now, User.bor_history, User.violate,\
                            User.description, User.money).\
                    filter(User.user_type == User_type.user_type_id).\
                        filter(User.user_id.like(user_id+"%")).paginate(page, per_page, error_out=False)
            else:
                return_dict["code"] = -2
                return_dict["info"] = "user_id呢?"
                return jsonify(return_dict)
        else:
            return_dict["code"] = -1
            return_dict["info"] = "排序id呢?"
            return jsonify(return_dict)
        return_dict["pages"] = res.pages
        return_dict["total"] = res.total
        return_dict["result"] = query2dict(res.items)
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0

    return jsonify(return_dict)

@admin_user.route('/delete_account',methods=["GET","POST"])
def delete_account():
    return_dict = {}
    user_id = request.values.get("user_id")
    if user_id:
        res = db.session.query(User).filter(User.user_id == user_id).all()
        if len(res) == 1:
            db.session.delete(res[0])
            db.session.commit()
            return_dict["code"] = 1
        else:
            return_dict["code"] = -1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)