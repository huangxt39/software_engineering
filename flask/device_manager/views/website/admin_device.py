from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
import device_manager.utils.global_var as gol
import uuid
admin_device=Blueprint('admin_device',__name__)

@admin_device.route('/upload_img', methods=['GET','POST'])
def upload_img():
    return_dict = {}
    #获取图片文件 name = upload
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
        return img_stream
    else:
        return jsonify({"code":0})
    # return jsonify(return_dict)

@admin_device.route('/add_big_type', methods=['GET','POST'])
def add_big_type():
    return_dict = {}

    big_type_name = request.values.get("big_type_name")
    if big_type_name:
        new_big_type = Device_big_type()
        new_big_type.big_type_name = big_type_name
        db.session.add(new_big_type)
        db.session.commit()
        return_dict["big_type_id"] = new_big_type.big_type_id
        return_dict["code"] = 1
    else:
        return_dict["code"] = 0
    return jsonify(return_dict)

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
    cost = request.values.get("cost")
    index1 = request.values.get("index1")
    index2 = request.values.get("index2")
    appendix = request.values.get("appendix")

    if cost:
        cost = int(cost)
    else:
        cost = 50
    if index1:
        index1 = float(index1)
    else:
        index1 = 0.25
    if index2:
        index2 = float(index2)
    else:
        index2 = 50
    total_num = int(total_num)
    available_num = int(available_num)
    real_cost = cost + (total_num - available_num)/total_num * index1 * index2


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
        new_device.student_limit_time=student_limit_time
        new_device.student_limit=student_limit
        new_device.teacher_limit=teacher_limit
        new_device.teacher_limit_time=teacher_limit_time
        new_device.cost=cost
        new_device.index1=index1
        new_device.index2=index2
        new_device.real_cost=real_cost
        new_device.appendix = appendix
        if image is not None:
            new_device.image=image 
        if type_id is None:
            db.session.add(new_device)
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
    
    name = request.values.get("name")
    type_id = request.values.get("type_id")
    query_type = request.values.get("query_type")
    page = request.values.get("page")
    per_page = request.values.get("per_page")
    if query_type is None:
        query_type = 0
    else:
        query_type = int(query_type)
    if page is None:
        page = 0
    else:
        page = int(page)
    if per_page is None:
        per_page = 5
    else:
        per_page = int(per_page)

    if request.method == "GET":
        if query_type == 0:
            res = db.session.query(Device_information.type_id, Device_information.device_name, Device_information.total_num, Device_information.available_num,\
                Device_information.description, Device_information.image, Device_information.real_cost, Device_information.cost, Device_information.index1, Device_information.index2, \
                    Device_information.student_limit, Device_information.student_limit_time, Device_information.teacher_limit, Device_information.teacher_limit_time,\
                        Device_big_type.big_type_name).filter(Device_information.big_type_id == Device_big_type.big_type_id).paginate(page, per_page, error_out=False)
            return_dict["pages"] =  res.pages
            return_dict["total"] = res.total
            items = res.items
            return_dict["result"] = query2dict(items)
            return_dict["code"] = 1

        elif query_type == 1:
            res = db.session.query(Device_information.type_id, Device_information.device_name, Device_information.total_num, Device_information.available_num,\
                Device_information.description, Device_information.image, Device_information.real_cost, Device_information.cost, Device_information.index1, Device_information.index2, \
                    Device_information.student_limit, Device_information.student_limit_time, Device_information.teacher_limit, Device_information.teacher_limit_time,\
                        Device_big_type.big_type_name).filter(Device_information.big_type_id == Device_big_type.big_type_id).\
                            filter(Device_information.device_name.like("%"+name+"%")).paginate(page, per_page, error_out=False)
            return_dict["pages"] = res.pages
            return_dict["total"] = res.total
            items = res.items
            return_dict["result"] = query2dict(items)
            return_dict["code"] = 1
        
        elif query_type == 2:
            if type_id:
                res = db.session.query(Device_information.type_id, Device_information.device_name, Device_information.total_num, Device_information.available_num,\
                    Device_information.description, Device_information.image, Device_information.real_cost, Device_information.cost, Device_information.index1, Device_information.index2, \
                        Device_information.student_limit, Device_information.student_limit_time, Device_information.teacher_limit, Device_information.teacher_limit_time,\
                            Device_big_type.big_type_name).filter(Device_information.big_type_id == Device_big_type.big_type_id).\
                                filter(Device_information.type_id == type_id).all()

                if len(res) == 1:
                    return_dict["result"] = query2dict(res)
                    return_dict["code"] = 1
                else:
                    return_dict["code"] = -1
                    return_dict["info"] = "type_id找不到这个设备"
            else:
                return_dict["code"] = -1
                return_dict["info"] = "type_id找不到这个设备"
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