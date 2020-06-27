from device_manager.models import *
from device_manager.utils import *
from flask import Flask, Response, request, jsonify
from flask import Blueprint
import os
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
    res = db.session.query(Device_information).filter(Device_information.type_id == type_id).all()

    if len(res) != 1:
        return jsonify({"code" : -1})
    return_dict["code"] = 1
    return_dict["result"] = query2dict(res[0])
    return jsonify(return_dict)