from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
from datetime import datetime, timedelta
import device_manager.utils.global_var as gol
import numpy as np
admin_record=Blueprint('admin_record',__name__)

## 设备占用率图
### 算法，是不是要搞个记录好点。。
@admin_record.route('/figure', methods=['GET','POST'])
def figure():
    return_dict = {}
    type_id = request.values.get("type_id")
    time = request.values.get("time") # 默认30天
    if time is None:
        time = 30
    else:
        time = int(time)

    base = db.session.query(Device_information).filter(Device_information.type_id == type_id).first()
    if base is None:
        return jsonify({"code":0})
    base = query2dict(base)
    total = base["total_num"]
    base_avail_num = base["available_num"]
    record_list = db.session.query(Borrow_record.book_borrow_time, Borrow_record.actual_return_time).\
        filter(Borrow_record.actual_return_time > datetime.now() - timedelta(days = time))
    time_lists = query2dict(record_list.all())
    add = [ sum([1 for j in range(len(time_lists)) if (time_lists[j]["book_borrow_time"]> datetime.now() - timedelta(days=i))]) for i in range(time)]
    minus = [ sum([1 for j in range(len(time_lists)) if (time_lists[j]["actual_return_time"]> datetime.now() - timedelta(days=i))]) for i in range(time)]
    add = np.array(add)
    minus = np.array(minus)

    device_use_rate = 1 - (base_avail_num + add - minus)/total
    return_dict["result"] = list(np.flipud(device_use_rate))  
    return jsonify(return_dict)

def count(x):
    return 1 if len(x["book_borrow_time"]) > datetime.now() - timedelta(days=i) else 0