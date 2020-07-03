from device_manager.models import *
from device_manager.utils import *
from flask import Flask, Response, request, jsonify
from flask import Blueprint
from datetime import datetime, timedelta
import os
import numpy as np 
wx_device=Blueprint('wx_device',__name__)

@wx_device.route('/')
def show():
    return 'record.hello'


@wx_device.route('/get_img', methods=['GET','POST'])
def get_image():
    return_dict = {}
    path = request.values.get('path')
    print(path)
    if os.path.isfile(path):
        img_stream = return_img_stream(path)
    else:
        return_dict["code"] = -1
    return img_stream

@wx_device.route('/device_type', methods=['GET'])
def device_big_type():
    return_dict = {}
    res = db.session.query(Device_big_type).all()
    return_dict["code"] = 1
    return_dict["result"] = query2dict(res)
    return jsonify(return_dict)

@wx_device.route('/type_name', methods=['GET','POST'])
def type_name():
    return_dict = {}
    big_type = request.values.get("big_type_id")
    res = db.session.query(Device_information.type_id,Device_information.device_name, Device_information.image).\
        filter(Device_information.big_type_id == big_type).all()
    return_dict["code"] = 1
    return_dict["result"] = query2dict(res)
    return jsonify(return_dict)

@wx_device.route('/get_device', methods=['GET','POST'])
def get_device():
    return_dict = {}

    type_id = request.values.get("type_id")
    type_id = int(type_id)
    # res = db.session.query(Device_information).filter(Device_information.type_id == type_id).all()
    res = db.session.query(Device_information.type_id, Device_information.device_name, Device_information.total_num, Device_information.available_num,\
        Device_information.description, Device_information.image, Device_information.real_cost, Device_information.cost, Device_information.index1, Device_information.index2, \
            Device_information.student_limit, Device_information.student_limit_time, Device_information.teacher_limit, Device_information.teacher_limit_time,\
                Device_big_type.big_type_name).filter(Device_information.big_type_id == Device_big_type.big_type_id).\
                    filter(Device_information.type_id == type_id).all()

    if len(res) != 1:
        return jsonify({"code" : 0})
    device = query2dict(res[0])

    feature_real_cost, feature_available = get_device_cost_available(device)

    return_dict["code"] = 1
    return_dict["result"] = device
    return_dict["real_cost"] = feature_real_cost
    return_dict["available"] = feature_available

    return jsonify(return_dict)



def get_device_cost_available(device):
    return_dict = {}
    time = 60
    
    num = device["total_num"]
    base_avail = device["available_num"]
    cost = device["cost"]
    index1 = device["index1"]
    index2 = device["index2"]

    record_list = db.session.query(Borrow_record.book_borrow_time, Borrow_record.book_return_time, Borrow_record.num).\
        filter(Borrow_record.device_type == device["type_id"]).\
        filter(Borrow_record.state_id < 2).\
        filter(Borrow_record.book_return_time < datetime.now() + timedelta(days = time)).all()
    print(record_list)
    if record_list:
        time_lists = query2dict(record_list)

        # 已经过了预计归还的时候，空闲数目是增大的的。
        add = [ sum([ time_lists[j]["num"] for j in range(len(time_lists)) if (time_lists[j]["book_return_time"] < datetime.now() + timedelta(days=i)) ]) for i in range(time)]
        # 已经过了预计借出的时候，空闲数目是减小的。
        minus = [ sum([ time_lists[j]["num"] for j in range(len(time_lists)) if (time_lists[j]["book_borrow_time"] < datetime.now() + timedelta(days=i)) ]) for i in range(time)]
        add = np.array(add).astype("float64")
        minus = np.array(minus).astype("float64")

        feature_avail = base_avail + add - minus
        device_use_rate = 1 - feature_avail/num
        feature_real_cost = cost + device_use_rate * float(index1) * float(index2)
    else:
        feature_avail = [int(device["available_num"])] * time
        feature_real_cost = [cost] * time

    return list(feature_real_cost), list(feature_avail)
