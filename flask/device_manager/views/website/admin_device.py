from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
import device_manager.utils.global_var as gol
from PIL import Image
import uuid
admin_device=Blueprint('admin_device',__name__)

@admin_device.route('/upload_img', methods=['GET','POST'])
def upload_img():
    return_dict = {}
    #获取图片文件 name = upload
    # if gol.get_value("debug"):
    #     img = Image.open("./device_manager/static/img/device/F550.jpg")
    # else:
    img = request.files.get('upload')
    if img is not None:
        new_device = Device_information()
        db.session.add(new_device)
        db.session.commit()
        img_name = "%s.jpg"%new_device.type_id
        path = "./device_manager/static/img/device/"
        url = os.path.join(path,img_name)
        img.save(url)
        # img.convert("RGB").save(url)
        new_device.image = url
        db.session.commit()
        return_dict["url"] = url
        return_dict["type_id"] = new_device.type_id
        return_dict["code"] = 1
    else:
        return_dict["code"] = -1
    return jsonify(return_dict)

@admin_device.route('/get_img', methods=['GET','POST'])
def get_image():
    return_dict = {}
    #获取图片文件 name = upload
    # if gol.get_value("debug"):
    #     path = "./device_manager/static/img/device/F550.jpg" 
    # else:
    path = request.values.get('path')
    print(path)
    if os.path.isfile(path):
        img_stream = return_img_stream(path)
        # img = Response(img_stream, mimetype="image/jpeg")
        # return_dict["code"] = 1
        # return_dict["img"] = img_stream
    else:
        return_dict["code"] = -1
    # return jsonify(return_dict)
    return img_stream

@admin_device.route('/add', methods=['GET','POST'])
def add():
    return_dict = {}

    type_id = request.values.get("type_id")
    # print(type_id)
    # type_id = '%05'%(int(type_id))
    type_id = int(type_id)
    # print(type_id)
    device_name = request.values.get("device_name")
    description = request.values.get("description")
    total_num = request.values.get("total_num")
    available_num = request.values.get("available_num")
    student_limit_time = request.values.get("student_limit_time")
    student_limit = request.values.get("student_limit")
    teacher_limit_time = request.values.get("teacher_limit_time")
    teacher_limit = request.values.get("teacher_limit")
    image = request.values.get("image")
    big_type_id = request.values.get("big_type_id")
    position = request.values.get("position")


    if request.method == "POST":
        if type_id is not None:
            new_device = db.session.query(Device_information).filter(Device_information.type_id==type_id).first()
        else:
            new_device = Device_information()
        new_device.type_id = int(type_id)
        new_device.device_name = device_name
        new_device.description = description
        new_device.total_num=int(total_num)
        new_device.available_num=int(available_num)
        new_device.student_limit_time=int(student_limit_time)
        new_device.student_limit=int(student_limit)
        new_device.teacher_limit=int(teacher_limit)
        new_device.teacher_limit_time=int(teacher_limit_time)
        new_device.big_type_id=int(big_type_id)
        if image is not None:
            new_device.image=image 
        if type_id is None:
            db.session.add(new_device)
        new_single_devices = []

        exist_devices_num = db.session.query(Signal_device).filter(Signal_device.type_id==type_id).count()
        
        for i in range(new_device.total_num - exist_devices_num):
            new_single_device = Signal_device()
            uid = str(uuid.uuid1())
            uid = uid[4:8] + uid[19:21]
            new_single_device.device_id = uid + "%03d"%new_device.big_type_id + "%05d"%new_device.type_id 
            new_single_device.type_id = new_device.type_id
            new_single_device.state_id = 0  #空闲
            new_single_device.position = position
            new_single_devices.append(new_single_device)
        db.session.add_all(new_single_devices)
        # db.add(new_device)
        db.session.commit()
        return_dict["code"] = 1
        return_dict["type_id"] = new_device.type_id
    elif request.method == "GET":
        return_dict["code"] = 2
    else:
        return_dict["code"] = -1

    return jsonify(return_dict)
    # return json.dumps(return_dict, cls=DateEncoder, ensure_ascii=False)

@admin_device.route('/query', methods=['GET','POST'])
def query():
    return_dict = {}

    # if gol.get_value("debug"):
    #     print("bebug mode auto input user_query")
    #     # order = 1
    #     name = "00003"
    #     type_id = 1
    #     query_type = 1
    # else:
    name = request.values.get("name")
    type_id = request.values.get("type_id")
    query_type = int(request.values.get("query_type"))
    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))
    # print(name)
    # print(type_id)
    # print(query_type)
    # print(type(query_type))
    # data = request.get_json()
    # print(data)
    if request.method == "GET":
        if query_type == 0:
            res = db.session.query(Device_information).filter(Device_information.device_name.like("%"+name+"%")).paginate(page, per_page, error_out=False)
            return_dict["pages"] =  res.pages
            return_dict["total"] = res.total
            items = res.items
            return_dict["result"] = query2dict(items)
            return_dict["code"] = 1
        elif query_type == 1:
            res = db.session.query(Device_information).filter(Device_information.type_id == type_id).first()
            return_dict["result"] = query2dict(res)
            return_dict["code"] = 1
        else:
            return_dict["code"] = 0
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)


@admin_device.route('/delete', methods=['GET','POST'])
def delete():
    return_dict = {}

    # if gol.get_value("debug"):
    #     print("bebug mode auto input user_query")
    #     # order = 1
    #     name = "00003"
    #     type_id = 1
    #     query_type = 1
    # else:
    name = request.values.get("name")
    type_id = request.values.get("type_id")  # 使用str或者int都能查得到？建议使用5位补0
    query_type = request.values.get("query_type")
    query_type = int(query_type)
    if request.method == "GET":
        if query_type == 0:
            res = db.session.query(Device_information).filter(Device_information.device_name == name).first()
        elif query_type == 1:
            res = db.session.query(Device_information).filter(Device_information.type_id == type_id).first()
        if res is None:
            return_dict["code"] = 2
        else:
            db.session.delete(res)
            db.session.commit()
            return_dict["code"] = 1
            return_dict["result"] = query2dict(res)
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)
    # return json.dumps(return_dict, cls=DateEncoder, ensure_ascii=False)