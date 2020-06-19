from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
import device_manager.utils.global_var as gol
admin_record=Blueprint('admin_record',__name__)

## 设备占用率图
@admin_record.route('/figure', methods=['GET','POST'])
def figure():
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