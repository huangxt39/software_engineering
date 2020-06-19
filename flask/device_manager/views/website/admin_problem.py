from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, request, render_template, Markup
from flask import Blueprint
from datetime import datetime, timedelta
import device_manager.utils.global_var as gol

admin_problem=Blueprint('admin_problem',__name__)

@admin_problem.route('/damage', methods=['GET'])
def damage():
    return_dict = {}
    # print( gol.get_value("debug"))
    if gol.get_value("debug"):
        # print("bebug mode auto input")
        order = 1
        num = 3
    else:
        order = request.values.get("order")
        num = request.values.get("num")

    if order == 1: #从旧往新
        order_code = "time"
    elif order == 2: # 从新往旧
        order_code = "-time"
    else:
        #排序输入错误
        return_dict["code"] = -1
        return json.dumps(return_dict)

    res = db.session.query(Demage_devices.id, Demage_devices.time, \
        Demage_devices.device_id, Device_information.device_name, \
            Demage_state.state, Demage_devices.user_id, Demage_devices.user_name, \
                Demage_devices.description, Demage_devices.contact, \
                    Demage_devices.track_down, Demage_devices.punish).\
                        filter(Demage_devices.device_type_id == Device_information.type_id).\
                            filter(Demage_devices.demage_state_id == Demage_state.id).\
                                order_by(order_code).all()
    # res = db.session.query(Demage_devices.id, Demage_devices.time, Demage_devices.device_id, Device_information.device_name, Demage_state.state, Demage_devices.user_id, Demage_devices.user_name, Demage_devices.description, Demage_devices.contact, Demage_devices.track_down, Demage_devices.punish).order_by(order_code).all()
        # 
            
    num = min(3,len(res))
    res = res[:num]
    # res = get_dict_list_from_result(res)

    res = [dict(zip(res.keys(), res)) for res in res]
    return_dict["index"] = num # num=2
    return_dict["result"] = res
    if len(res):
        return_dict["code"] = 0
    else:
        return_dict["code"] = 1
    return json.dumps(return_dict, cls=DateEncoder, ensure_ascii=False)


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

## 借用逾期的问题
@admin_problem.route('/due', methods=['GET', 'POST'])
def due():
    return_dict = {}

    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))

    ## 获得状态正在进行的记录(id小于3的都是正在进行的), 再进一步筛选过期的，
    res = db.query(Borrow_record).filter(Borrow_record.state_id < 3).\
        fliter(Borrow_record.book_return_time < datatime.now()).paginate(page, per_page, error_out=False)
    
    if res == None:
        return jsonify({"code":0})
    
    res = query2dict(res)
    return_dict["result"] = res
    return jsonify(return_dict)


@admin_problem.route('/config', methods=['GET', 'POST'])
def config():
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

def query2dict(model_list):
    if isinstance(model_list,list):  #如果传入的参数是一个list类型的，说明是使用的all()的方式查询的
        if isinstance(model_list[0],db.Model):   # 这种方式是获得的整个对象  相当于 select * from table
            lst = []
            for model in model_list:
                dic = {}
                for col in model.__table__.columns:
                    dic[col.name] = getattr(model,col.name)
                lst.append(dic)
            return lst
        else:                           #这种方式获得了数据库中的个别字段  相当于select id,name from table
            lst = []
            for result in model_list:   #当以这种方式返回的时候，result中会有一个keys()的属性
                lst.append([dict(zip(result.keys, r)) for r in result])
            return lst