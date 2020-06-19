from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
import device_manager.utils.global_var as gol
from PIL import Image
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

    # if gol.get_value("debug"):
    #     print("bebug mode auto input user_query")
    #     # order = 1
    #     type_id = "00003"
    #     device_name = "测试用设备"
    #     description = "我就测试一下"
    #     total_num = "15"
    #     available_num = "15"
    #     student_limit_time = "15"
    #     student_limit = "1"
    #     teacher_limit_time = "15"
    #     teacher_limit = "2"
    #     # image = "./Idontknow.jpg"
    # else:
    # order = request.values.get("order")
    type_id = request.form.get("type_id")
    device_name = request.form.get("device_name")
    description = request.form.get("description")
    total_num = request.form.get("total_num")
    available_num = request.form.get("available_num")
    student_limit_time = request.form.get("student_limit_time")
    student_limit = request.form.get("student_limit")
    teacher_limit_time = request.form.get("teacher_limit_time")
    teacher_limit = request.form.get("teacher_limit")
    # image = request.form.get("image")

    if request.method == "POST":
        if type_id is not None:
            new_device = db.session.query(Device_information).filter(Device_information.type_id==type_id).first()
        else:
            new_device = Device_information()
        # new_device.type_id = type_id
        new_device.device_name = device_name
        new_device.description = description
        new_device.total_num=total_num
        new_device.available_num=available_num
        new_device.student_limit_time=student_limit_time
        new_device.student_limit=student_limit
        new_device.teacher_limit=teacher_limit
        new_device.teacher_limit_time=teacher_limit_time
        if type_id is None:
            db.session.add(new_device)
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
    query_type = request.values.get("query_type")
    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))
    print(name)
    print(type_id)
    print(query_type)
    print(type(query_type))
    # data = request.get_json()
    # print(data)
    if request.method == "GET":
        if query_type == "0":
            res = db.session.query(Device_information).filter(Device_information.device_name.like("%"+name+"%")).paginate(page, per_page, error_out=False)
        elif query_type == "1":
            res = db.session.query(Device_information).filter(Device_information.type_id == type_id).first()
        else:
            return_dict["code"] = -1
            return jsonify(return_dict)
        print(res)
        res = query2dict(res)
        print(res)
        return_dict["result"] = res
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)
    # return json.dumps(return_dict, cls=DateEncoder, ensure_ascii=False)


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