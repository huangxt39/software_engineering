from device_manager.utils import *
from flask import Blueprint,request, jsonify
from device_manager.models import *
from datetime import datetime, timedelta
import uuid
import json

wx_record=Blueprint('wx_record',__name__)


@wx_record.route('/get_record', methods=['GET','POST'])
def get_record():    
    return_dict = {}
    
    user_id = request.values.get('user_id')
    page = request.values.get("page")
    per_page = request.values.get("per_page")
    
    if page:
        page = int(page)
    else:
        page = 0
    if per_page:
        per_page = int(per_page)
    else:
        per_page = 5

    if user_id is not None:
        is_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(is_user) == 1:
            # record_lists = db.session.query(Borrow_record).filter(Borrow_record.user_id == user_id).all()
            res = db.session.query(Borrow_record.id, Device_information.device_name, \
                Borrow_record.book_borrow_time, \
                Borrow_record.book_return_time, \
                Borrow_record.num, Record_state.state,\
                    Device_information.image).filter(Borrow_record.user_id == user_id).\
                filter(Borrow_record.state_id == Record_state.id).\
                filter(Borrow_record.device_type == Device_information.type_id).paginate(page, per_page, error_out=False)
                # filter(Borrow_record.device_type == Device_information.type_id).all()
            timeout = []
            waiting2obtain = []
            items = res.items
            for i in range(len(items)):
                if items[i].state=="进行中" and items[i].book_return_time < datetime.now():
                    timeout.append(1)
                else:
                    timeout.append(0)
                if items[i].state=="未开始" and items[i].book_borrow_time < datetime.now():
                    waiting2obtain.append(1)
                else:
                    waiting2obtain.append(0)
            items = query2dict(items)
            for i in range(len(items)):
                items[i]["timeout"] = timeout[i]  
                items[i]["waiting2obtain"] = waiting2obtain[i]
            return_dict["result"] = items
            return_dict["pages"] = res.total
            return_dict["pages"] =  res.pages
            return_dict["code"] = 1
        else:
            return_dict["code"] = -1 # 这个人没注册？ 或者这个人竟然有多个（出大问题
    else:
        return_dict["code"] = 0 # 没传user_id过来
    # 生成的数据

    return jsonify(return_dict)

@wx_record.route('/get_single_record', methods=['GET','POST'])
def get_single_record():
    return_dict = {}
    record_id = request.values.get('record_id')
    user_id = request.values.get('user_id')
    if record_id is not None and user_id is not None:
        is_record = db.session.query(Borrow_record).filter(Borrow_record.id == record_id, Borrow_record.user_id == user_id).all()
        if len(is_record) == 1:
            # record_lists = db.session.query(Borrow_record).filter(Borrow_record.user_id == user_id).all()
            record_lists = db.session.query(Borrow_record.id, Device_information.device_name, \
                Borrow_record.submit_time, \
                Borrow_record.book_borrow_time, Borrow_record.actual_borrow_time, \
                Borrow_record.book_return_time, Borrow_record.actual_return_time, \
                Borrow_record.num, Borrow_record.cost, Record_state.state).filter(Borrow_record.user_id == user_id).\
                filter(Borrow_record.state_id == Record_state.id).\
                filter(Borrow_record.device_type == Device_information.type_id).all()
            records = query2dict(record_lists)
            return_dict["result"] = records
            return_dict["code"] = 1
        else:
            return_dict["code"] = -1 # 订单不唯一
    else:
        return_dict["code"] = 0 # 没传record_id过来
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
    book_return_time = request.values.get("book_return_time")
    real_cost = request.values.get("real_cost")

    num = int(num)
    if user_id and real_cost:
        is_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(is_user) == 1:
            user_now = is_user[0]
            is_device = db.session.query(Device_information).filter(Device_information.type_id == device_type_id).all()
            if len(is_device) == 1:
                device_type= is_device[0]
                submit_time = datetime.now()
                # book_borrow_time = datetime.strptime(book_borrow_time + str(submit_time)[10:19],'%Y-%m-%d %H:%M:%S')
                # book_return_time = datetime.strptime(book_return_time + str(submit_time)[10:19],'%Y-%m-%d %H:%M:%S')
                book_borrow_time = datetime.strptime(book_borrow_time,'%Y-%m-%d')
                book_return_time = datetime.strptime(book_return_time,'%Y-%m-%d') + timedelta(days=1)
                # book_return_time = book_borrow_time + timedelta(days=30)
                borrow_cost = float(real_cost) * (book_return_time - book_borrow_time).days
                
                if user_now.money >= borrow_cost:
                    if device_type.available_num > num:
                        ## 有足够的空闲设备，则开始创建记录信息
                        # device_type.available_num = device_type.available_num - num
                        # device_type.real_cost = device_type.cost + (device_type.total_num - device_type.available_num)/device_type.total_num * float(device_type.index1) * float(device_type.index2)

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
                        new_record.num = num
                        new_record.cost = borrow_cost
                        user_now.money = float(user_now.money) - borrow_cost
                        # user_now.bor_now = user_now.bor_now + num
                        # user_now.bor_history = user_now.bor_history + num
                        db.session.add(new_record)
                        db.session.commit()
                        return_dict["record_id"] = record_id
                        return_dict["code"] = 1  #成功
                        return_dict["info"] = "你借到了，但你扣钱了"
                    else:
                        return_dict["code"] = -4 # 设备不足以借出
                        return_dict["info"] = "设备不足以借出"
                else:
                    return_dict["code"] = -3  # 你没钱了还想借？
                    return_dict["info"] = "你没钱了还想借？"
            else:
                return_dict["code"]  = -2 # 没这个设备，或设备id查询出来多个结果（出大问题
                return_dict["info"] = "没这个设备，或设备id查询出来多个结果（出大问题"
        else:
            return_dict["code"] = -1 # 没这个人，或者这个人竟然有多个（出大问题
            return_dict["info"] = "没这个人，或者这个人竟然有多个（出大问题"
    else:
        return_dict["code"] = 0 # 没传用户数据过来啊
        return_dict["info"] = "没传用户数据或者没给我花多少钱"
    # 生成的数据
    return jsonify(return_dict)

@wx_record.route('/check', methods=['GET','POST'])
def record_check():   
    return_dict = {}
    user_id = request.values.get("user_id")
    record_id = request.values.get("record_id")
    if record_id and user_id:
        record_list = db.session.query(Borrow_record).filter(Borrow_record.id == record_id).filter(Borrow_record.user_id == user_id).all()
        this_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(record_list) == 1 and len(this_user) == 1:
            record = record_list[0]
            this_user = this_user[0]
            this_device = db.session.query(Device_information).filter(Device_information.type_id == record.device_type).first()
            if record.state_id == 0:
                record.state_id = 1 # 正在进行
                record.actual_borrow_time = datetime.now()
                this_user.bor_now = this_user.bor_now + record.num
                this_user.bor_history = this_user.bor_history + record.num
                this_device.available_num = this_device.available_num - record.num
                this_device.real_cost = this_device.cost + (this_device.total_num - this_device.available_num)/this_device.total_num * float(this_device.index1) * float(this_device.index2)
                # this_device.real_cost = 
                db.session.commit()
                return_dict["code"] = 1
                return_dict["info"] = "成功了，我把状态改成正在进行了"
            else:
                return_dict["code"] = -2
                return_dict["info"] = "你的状态不连续啊，你要还没领取才能确认领取"
        else:
            return_dict["code"] = -1
            return_dict["info"] = "id搜索出多个结果，出大问题"
    else:
        return_dict["code"] = 0
        return_dict["info"] = "老哥传id啊"
    return jsonify(return_dict)

@wx_record.route('/cancel', methods=['GET','POST'])
def cancel_record():   
    return_dict = {}
    user_id = request.values.get("user_id")
    record_id = request.values.get("record_id")
    if record_id and user_id:
        record_list = db.session.query(Borrow_record).filter(Borrow_record.id == record_id).filter(Borrow_record.user_id == user_id).all()
        this_user = db.session.query(User).filter(User.user_id == user_id).all()
        if len(record_list) == 1 and len(this_user) == 1:
            record = record_list[0]
            this_user = this_user[0]
            this_device = db.session.query(Device_information).filter(Device_information.type_id == record.device_type).first()
            if record.state_id == 0:
                record.state_id = 2 # 已结束
                params = get_manger_params()
                record.actual_borrow_time = datetime.now()
                # this_device.available_num = this_device.available_num - record.num
                # this_device.real_cost = this_device.cost + (this_device.total_num - this_device.available_num)/this_device.total_num * float(this_device.index1) * float(this_device.index2)
                this_user.money = float(this_user.money) + (1 - 0.01 *  float(params["订单取消惩罚比例"])) * float(record.cost)
                db.session.commit()
                return_dict["code"] = 1
                return_dict["info"] = "成功了，你的订单已经取消了,但你扣了60%的钱"
            # elif record.state_id == 1:
            #     record.state_id = 2 # 已结束
            #     this_device.available_num = this_device.available_num + record.num
            #     this_user.bor_now = this_user.bor_now - record.num
            #     this_device.real_cost = float(this_device.cost) + (this_device.total_num - this_device.available_num)/this_device.total_num * float(this_device.index1) * float(this_device.index2)
            #     db.session.commit()
            #     return_dict["code"] = 1
            #     return_dict["info"] = "成功了，你的订单已经取消了,但你扣了全部的钱"
            else:
                return_dict["code"] = 2
                return_dict["info"] = "如果已经开始了请走归还操作"

        else:
            return_dict["code"] = -1
            return_dict["info"] = "id搜索出多个结果，出大问题"
    else:
        return_dict["code"] = 0
        return_dict["info"] = "老哥传id啊"
    return jsonify(return_dict)


@wx_record.route('/return', methods=['GET','POST'])
def record_return():    
    return_dict = {}
    user_id = request.values.get("user_id")
    record_id = request.values.get("record_id")

    if record_id and user_id:
        record_list = db.session.query(Borrow_record).filter(Borrow_record.id == record_id).filter(Borrow_record.user_id == user_id).all()
        if len(record_list) == 1:
            record = record_list[0]
            # devices_lists = db.session.query(Record_Single_devices).filter(Record_Single_devices.id == record_id).all()
            # if len(devices_lists):
            device_type = db.session.query(Device_information).filter(Device_information.type_id == record.device_type).first()
            available_sum = device_type.available_num + record.num
            # available_sum = device_type.available_num + len(devices_lists)
            user_now = db.session.query(User).filter(User.user_id == user_id).first()
            if device_type.total_num >= available_sum:
                if record.state_id == 1:
                    record.state_id = 2
                    record.actual_return_time = datetime.now()
                    record.actual_return_time = datetime.now()
                    
                    device_type.available_num = available_sum
                    device_type.real_cost = float(device_type.cost) + (device_type.total_num - device_type.available_num)/device_type.total_num * float(device_type.index1) * float(device_type.index2)
                    
                    user_now.bor_now = user_now.bor_now - record.num
                    if datetime.now() >record.book_return_time:
                        user_now.violate = user_now.violate + 1
                    db.session.commit()

                    return_dict["code"] = 1 # 没问题
                    return_dict["info"] = "没问题,你的订单结束了" # 
                else:
                    return_dict["info"] = "我发现了你都没拿到东西就结束了"
                    return_dict["code"] = -3 # 状态不连续，从1直接到3了
            else:
                return_dict["info"] = "空闲数量统计出错" # 
                return_dict["code"] = -2 # 空闲数量统计出错
        else:
            return_dict["info"] = "出大问题，订单不唯一" # 
            return_dict["code"] = -1 # 出大问题，订单不唯一
    else:
        return_dict["info"] = "老哥，你为什么不输入id呢" # 
        return_dict["code"] = 0 # 老哥，你为什么不输入id呢
    return jsonify(return_dict)

@wx_record.route('/damage_report', methods=['GET','POST'])
def damage_report():    
    return_dict = {}
    user_id = request.values.get("user_id")
    record_id = request.values.get("record_id")
    device_id = request.values.get("device_id")
    description = request.values.get("description")

    submit_time = datetime.now()
    if device_id:
        res = db.session.query(Borrow_record).filter(Borrow_record.user_id == user_id).\
            filter(Borrow_record.id == record_id).all()
        users = db.session.query(User).filter(User.user_id == user_id).all()
        if len(res)==1 and len(users) == 1:
            record = res[0]
            user_now = users[0]
            new_demage_device = Demage_devices()
            uid = str(uuid.uuid1())
            uid = uid[:8] + uid[19:21]
            demage_record_id = "DD"+str(submit_time)[:10].replace("-","") + uid
            new_demage_device.id = demage_record_id
            new_demage_device.time = submit_time
            new_demage_device.device_id = device_id
            new_demage_device.user_id = user_id
            new_demage_device.device_type_id = record.device_type
            new_demage_device.user_name = user_now.user_name
            new_demage_device.demage_state_id = 0
            methods = json.dumps({"追查责任人":0,"联系维修师傅":0,"惩罚损坏人":0}, cls=DateEncoder, ensure_ascii=False)
            new_demage_device.methods = methods
            new_demage_device.description = description
            return_dict["info"] = "上报成功" # 
            return_dict["code"] = 1 # 老哥，你为什么不输入id呢
            db.session.add(new_demage_device)
            db.session.commit()
        else:
            return_dict["info"] = "没有这个用户或者订单" # 
            return_dict["code"] = -1 # 老哥，你为什么不输入id呢
    else:
        return_dict["info"] = "老哥，你为什么不输入id呢" # 
        return_dict["code"] = 0 # 老哥，你为什么不输入id呢
    return jsonify(return_dict)