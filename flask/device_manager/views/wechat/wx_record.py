from device_manager.utils import *
from flask import Blueprint,request, jsonify
from device_manager.models import *
from datetime import datetime, timedelta
import uuid

wx_record=Blueprint('wx_record',__name__)


@wx_record.route('/get_record', methods=['GET','POST'])
def get_record():    
    return_dict = {}
    
    user_id = request.values.get('user_id')
    
    if user_id is not None:
        is_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(is_user) == 1:
            # record_lists = db.session.query(Borrow_record).filter(Borrow_record.user_id == user_id).all()
            record_lists = db.session.query(Borrow_record.id, Device_information.device_name, \
                Record_state.state).filter(Borrow_record.user_id == user_id).\
                filter(Borrow_record.state_id == Record_state.id).\
                filter(Borrow_record.device_type == Device_information.type_id).all()
            records = query2dict(record_lists)
            return_dict["result"] = records
            return_dict["code"] = 1
        else:
            return_dict["code"] = -1 # 这个人没注册？ 或者这个人竟然有多个（出大问题
    else:
        return_dict["code"] = 0 # 没传user_id过来
    # 生成的数据

    return jsonify(return_dict)



@wx_record.route('/add', methods=['GET','POST'])
def add():
    return_dict = {}
    user_id = request.values.get("user_id")
    device_type_id = request.values.get("device_type_id")
    num = request.values.get("num")
    borrow_reason = request.values.get("borrow_reason")
    book_borrow_time = request.values.get("book_borrow_time")

    num = int(num)
    if user_id is not None:
        is_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(is_user) == 1:
            is_device = db.session.query(Device_information).filter(Device_information.type_id == device_type_id).all()
            if len(is_device) == 1:
                device_type= is_device[0]
                if device_type.available_num > num:
                    ## 有足够的空闲设备，则开始创建记录信息

                    device_type.available_num = device_type.available_num - num
                    
                    submit_time = datetime.now()
                    
                    book_borrow_time = datetime.strptime(book_borrow_time + str(submit_time)[10:19],'%Y-%m-%d %H:%M:%S')
                    book_return_time = book_borrow_time + timedelta(days=30)
                    
                    uid = str(uuid.uuid1())
                    uid = uid[:8] + uid[19:21]
                    record_id = str(submit_time)[:10].replace("-","") + uid
                    new_record = Borrow_record()
                    new_record.id = record_id
                    new_record.submit_time = submit_time
                    new_record.book_borrow_time = book_borrow_time
                    new_record.book_return_time = book_return_time
                    new_record.user_id = user_id
                    new_record.borrow_reason = borrow_reason
                    new_record.state_id = 0
                    new_record.device_type = device_type_id
                    ## 搜索空闲设备
                    new_record_devices = []
                    devices = db.session.query(Signal_device).filter(Signal_device.type_id == device_type_id).filter(Signal_device.state_id == 0).all()
                    for i in range(num):    
                        devices[i].state_id = 2  # 已借出状态， 若是1则是预约状态。
                        new_record_device = Record_Single_devices()
                        new_record_device.id = record_id
                        new_record_device.device_id = devices[i].device_id
                        new_record_device.state = 2  # 跟上面是一致的。
                        new_record_devices.append(new_record_device)

                    # 由于一个订单只能借一个设备类型，所以并不需要借用设备表来记录。
                    # new_record_device_type = Record_devices()
                    # new_record_device_type.id = record_id
                    # new_record_device_type.device_type = device_type_id

                    db.session.add_all([new_record] + new_record_devices)
                    db.session.commit()
                    return_dict["record_id"] = record_id
                    return_dict["code"] = 1  #成功
                else:
                    return_dict["code"] = -3 # 设备不足以借出
            else:
                return_dict["code"]  = -2 # 没这个设备，或设备id查询出来多个结果（出大问题
        else:
            return_dict["code"] = -1 # 没这个人，或者这个人竟然有多个（出大问题
    else:
        return_dict["code"] = 0 # 传了用户数据过来。没有就完了。
    # 生成的数据
    return jsonify(return_dict)



@wx_record.route('/return', methods=['GET','POST'])
def record_return():    
    return_dict = {}
    record_id = request.values.get("record_id")

    if record_id:
        record_list = db.session.query(Borrow_record).filter(Borrow_record.id == record_id).all()
        if len(record_list) == 1:
            record = record_list[0]
            devices_lists = db.session.query(Record_Single_devices).filter(Record_Single_devices.id == record_id).all()
            if len(devices_lists):
                
                device_type = db.session.query(Device_information).filter(Device_information.type_id == record.device_type).first()
                available_sum = device_type.available_num + len(devices_lists)
                if device_type.total_num >= available_sum:
                    record.state_id = 3
                    record.actual_return_time = datetime.now()
                    device_type.available_num = available_sum
                    for i in range(len(devices_lists)):
                        devices_lists[i].state = 0 # 标记为空闲
                    return_dict["code"] = 1 # 没问题
                else:
                    return_dict["code"] = -3 # 统计空闲数量出错
                db.session.commit()
            else:
                return_dict["code"] = -2 # 找不到设备啊
        else:
            return_dict["code"] = -1 # 出大问题，订单不唯一
    else:
        return_dict["code"] = 0 # 老哥，你为什么不输入id呢
    return jsonify(return_dict)

@wx_record.route('/error_report', methods=['GET','POST'])
def error_report():    
    return_dict = {}
    
    return_dict["code"] = 1




    return jsonify(return_dict)