from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup, jsonify
from flask import Blueprint
from datetime import datetime, timedelta
import device_manager.utils.global_var as gol

admin_problem=Blueprint('admin_problem',__name__)

@admin_problem.route('/damage', methods=['GET'])
def damage():
    return_dict = {}
    # print( gol.get_value("debug"))
    # if gol.get_value("debug"):
    #     # print("bebug mode auto input")
    #     order = 1
    #     num = 3
    # else:
    order = int(request.values.get("order"))
    # num = request.values.get("num")
    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))

    if order == 1: #从旧往新
        order_code = Demage_devices.time
    elif order == 2: # 从新往旧
        order_code = Demage_devices.time.desc()
    else:
        #排序输入错误
        return_dict["code"] = -1
        return jsonify(return_dict)

    res = db.session.query(Demage_devices.id, Demage_devices.time, \
        Demage_devices.device_id, Device_information.device_name, \
            Demage_state.state, Demage_devices.user_id, Demage_devices.user_name, \
                Demage_devices.description, Demage_devices.methods).\
                        filter(Demage_devices.device_type_id == Device_information.type_id).\
                            filter(Demage_devices.demage_state_id == Demage_state.id).\
                                order_by(order_code).paginate(page, per_page, error_out=False)

    items = query2dict(res.items)
    exam = items[0]["methods"]
    return_dict["pages"] =  res.pages
    # return_dict["per_page"] = num # num=2
    return_dict["result"] = items
    return_dict["total"] = res.total
    if res.total:
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)


@admin_problem.route('/damage_modify', methods=['GET'])
def damage_modify():
    return_dict = {}
    damage_id = request.values.get("damage_id")
    methods = request.values.get("methods")

    res = db.session.query(Demage_devices).filter(Demage_devices.id == damage_id).all()

    if len(res) == 1:
        damage_issue = res[0]
        damage_issue.state = 1
        damage_issue.methods = methods
        return_dict["code"] = 1
    else:
        return_didc["code"] = 0



### 不知道干嘛的。。
@admin_problem.route('/accounts', methods=['GET', 'POST'])
def accounts():
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
        return jsonify({"code":2})
    ## 是否有这个人，匹配全校师生信息库
    res = db.session.query(School_information).filter_by(name=name, user_id=user_id).first()
    if res==None:
        return jsonify({"code":3})

    # 查询学号是否被注册
    res = db.session.query(Pre_Manager).filter_by(user_id = user_id).first()
    if res==None:
        return jsonify({"code":4})

    #以上都没有问题才允许注册
    new_manager = Pre_Manager(user_id = user_id, name=name, phone=phone, email=email, account=account, password=password,description=description)
    db.session.add(new_manager)
    db.session.commit()
    return jsonify({"code":1})

## 借用逾期的问题
@admin_problem.route('/due', methods=['GET', 'POST'])
def due():
    return_dict = {}

    order = int(request.values.get("order"))
    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))
    if order == 1: #从旧往新
        order_code = Borrow_record.book_return_time
    elif order == 2: # 从新往旧
        order_code = Borrow_record.book_return_time.desc()
    else:
        #排序输入错误
        return_dict["code"] = -1
        return jsonify(return_dict)

    ## 获得状态正在进行的记录(id小于2的都是正在进行的), 再进一步筛选过期的，
    res = db.session.query(Borrow_record).filter(Borrow_record.state_id < 2).\
        filter(Borrow_record.book_return_time < datetime.now()).order_by(order_code).paginate(page, per_page, error_out=False)
    
    if len(res.items) == 0:
        return jsonify({"code":0})

    items = query2dict(res.items)
    return_dict["pages"] =  res.pages
    # return_dict["per_page"] = num # num=2
    return_dict["result"] = items
    return_dict["total"] = res.total
    return jsonify(return_dict)
