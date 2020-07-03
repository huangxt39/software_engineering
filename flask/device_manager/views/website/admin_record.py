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
    record_list = db.session.query(Borrow_record.book_borrow_time, Borrow_record.actual_return_time, Borrow_record.num).\
        filter(Borrow_record.device_type == type_id).\
        filter(Borrow_record.actual_return_time > datetime.now() - timedelta(days = time))
    time_lists = query2dict(record_list.all())
    # print(time_lists)
    ## 预计时间还没到的时候，空闲数目是增加的
    add = [ sum([ time_lists[j]["num"] for j in range(len(time_lists)) if (time_lists[j]["book_borrow_time"]> datetime.now() - timedelta(days=i)) ]) for i in range(time)]
    
    # 预计时间已经到的时候，空闲数目是减小的。
    minus = [ sum([ time_lists[j]["num"] for j in range(len(time_lists)) if (time_lists[j]["actual_return_time"]> datetime.now() - timedelta(days=i)) ]) for i in range(time)]
    add = np.array(add)
    minus = np.array(minus)

    device_use_rate = 1 - (base_avail_num + add - minus)/total
    return_dict["result"] = list(np.flipud(device_use_rate))  
    return jsonify(return_dict)

