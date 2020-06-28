
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import device_manager.utils.global_var as gol
gol._init()
gol.set_value("debug",0)
# debug = 0
db = SQLAlchemy(use_native_unicode='utf8')

## 生成models
# flask-sqlacodegen "mysql+pymysql://root:123456@108.166.209.115:3306/设备管理" --outfile model.py --flask

## 用户账户数据库
class User(db.Model):
    __tablename__ = '用户表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'user'

    wxid = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='微信号，真正使用的时候使用UnionID')
    user_type = db.Column(db.Integer, info='用户类型')
    user_id = db.Column(db.String(8, 'utf8_general_ci'), info='学号/工号')
    user_name = db.Column(db.String(20), info='用户姓名')
    phone = db.Column(db.String(11, 'utf8_general_ci'), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    photo = db.Column(db.String(20), info='照片路径')
    money = db.Column(db.Numeric(10, 2), info='虚拟币金额')
    bor_now = db.Column(db.Integer, info='当前正在借的设备数量')
    bor_history = db.Column(db.Integer, info='历史借了多少设备')
    violate = db.Column(db.Integer, info='违规次数')
    description = db.Column(db.String(255), info='自我描述')


class User_type(db.Model):
    __tablename__ = '用户类型表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'user'

    user_type_id = db.Column(db.Integer, primary_key=True, info='用户类型id')
    user_type_name = db.Column(db.String(10), info='用户类型')
    wages = db.Column(db.Integer, info='每月工资/最大虚拟币')

class Manager(db.Model):
    __tablename__ = '管理员表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'user'

    user_id = db.Column(db.String(20), primary_key=True, info='学号/工号')
    name = db.Column(db.String(255), info='姓名')
    phone = db.Column(db.String(20), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    account = db.Column(db.String(20), info='账号')
    password = db.Column(db.String(20), info='密码')
    description = db.Column(db.String(255), info='申请描述')

class Pre_Manager(db.Model):
    __tablename__ = '待审核管理员表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'user'

    user_id = db.Column(db.String(20), primary_key=True, info='学号/工号')
    name = db.Column(db.String(255), info='姓名')
    phone = db.Column(db.String(20), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    account = db.Column(db.String(20), info='账号')
    password = db.Column(db.String(20), info='密码')
    description = db.Column(db.String(255), info='申请描述')

## 设备信息表
class Device_information(db.Model):
    __tablename__ = '设备信息表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'device'

    type_id = db.Column(db.Integer, primary_key=True, info='类型id')
    device_name = db.Column(db.String(10, 'utf8_general_ci'), info='设备名称')
    description = db.Column(db.String(50, 'utf8_general_ci'), info='设备描述')
    total_num = db.Column(db.SmallInteger, info='总共有多少设备')
    available_num = db.Column(db.SmallInteger, info='可用数量')
    student_limit_time = db.Column(db.Integer, info='学生最大借用时间')
    student_limit = db.Column(db.Integer, info='学生借用上限')
    teacher_limit_time = db.Column(db.Integer, info='学生最大借用时间')
    teacher_limit = db.Column(db.Integer, info='老师借用上限')
    image = db.Column(db.String(255, 'utf8_general_ci'), info='设备图片路径')
    big_type_id = db.Column(db.Integer, info='设备大类型，例如turtlebot2属于turtlebot系列')
    cost = db.Column(db.Integer, info='虚拟币花费')
    index1 = db.Column(db.Numeric(10, 2), info='虚拟币指数1')
    index2 = db.Column(db.Numeric(10, 2), info='虚拟币指数2')
    real_cost = db.Column(db.Numeric(10, 2), info='虚拟币实际花费')

class Device_big_type(db.Model):
    __tablename__ = '设备大类型表'
    __bind_key__ = 'manager'
    big_type_id = db.Column(db.Integer, primary_key=True, info='类型id')
    name = db.Column(db.String(10, 'utf8_general_ci'), info='设备名称')


# class Signal_device(db.Model):
#     __tablename__ = '单个设备信息表'
#     __bind_key__ = 'manager'
#     # __bind_key__ = 'device'

#     device_id = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='设备编号')
#     type_id = db.Column(db.Integer, info='设备类型id')
#     state_id = db.Column(db.String(5, 'utf8_general_ci'), info='设备状态')
#     position = db.Column(db.String(30, 'utf8_general_ci'), info='设备存放位置')


class Device_state(db.Model):
    __tablename__ = '设备状态表'
    __bind_key__ = 'manager'
    # __bind_key__ = 'device'

    state_id = db.Column(db.String(10), primary_key=True)
    state_name = db.Column(db.String(10))
    
## 全院师生信息
class School_information(db.Model):
    __tablename__ = '师生信息表'
    __bind_key__ = 'manager' 
    # __bind_key__ = 'school' 

    id = db.Column(db.String(8, 'utf8_general_ci'), primary_key=True, info='学号/工号')
    type = db.Column(db.String(2, 'utf8_general_ci'), nullable=False, info='学生/老师')
    name = db.Column(db.String(10, 'utf8_general_ci'), nullable=False)


## 借用审批

# class Record_devices(db.Model):  ## 每次借用借用了什么设备
#     __tablename__ = '借用设备表'
#     __bind_key__ = 'manager'
#     # __bind_key__ = 'record'

#     id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True, nullable=False)
#     device_type = db.Column(db.ForeignKey('设备信息表.type_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
#     num = db.Column(db.Integer, info='这个类型的设备借用了多少')
#     state = db.Column(db.String(10), info='此设备借用的状态')


# class Record_Single_devices(db.Model):  ## 每次借用借用了什么设备
#     __tablename__ = '借用单个设备表'
#     __bind_key__ = 'manager'
#     # __bind_key__ = 'record'

#     id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True, nullable=False)
#     device_id = db.Column(db.ForeignKey('设备信息表.type_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
#     state = db.Column(db.String(10), info='此设备借用的状态')

class Borrow_record(db.Model):  
    __tablename__ = '设备借用记录表'
    __bind_key__ = 'manager' 
    # __bind_key__ = 'record' 

    id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True, info='订单编号')
    submit_time = db.Column(db.DateTime)
    # submit_check = db.Column(db.String(10), info='申请审核人')
    book_borrow_time = db.Column(db.DateTime, info='预约的领取时间')
    actual_borrow_time = db.Column(db.DateTime, info='实际领取设备时间')
    # borrow_check = db.Column(db.String(255), info='领取审核人')
    book_return_time = db.Column(db.DateTime, info='预计归还时间')
    # return_check = db.Column(db.String(255), info='归还审核人')
    actual_return_time = db.Column(db.DateTime, info='实际归还时间')
    user_id = db.Column(db.String(8, 'utf8_general_ci'), info='用户id')
    borrow_reason = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue(), info='借用理由')
    state_id = db.Column(db.String(10, 'utf8_general_ci'), info='订单状态')
    device_type = db.Column(db.Integer, info='类型id')
    num = db.Column(db.Integer, info='借用数量')
    cost = db.Column(db.Numeric(10, 2), info='虚拟币花费')


class Record_state(db.Model):
    __tablename__ = '订单状态表'
    __bind_key__ = 'manager' 
    # __bind_key__ = 'record' 

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10))


class Demage_state(db.Model):
    __tablename__ = '损坏状态表'
    __bind_key__ = 'manager' 
    # __bind_key__ = 'record' 

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10))

class Demage_devices(db.Model):
    __tablename__ = '损坏设备信息表'
    __bind_key__ = 'manager' 
    # __bind_key__ = 'record' 

    id = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='损坏编号')
    time = db.Column(db.DateTime, info='提交时间')
    device_id = db.Column(db.String(50, 'utf8_general_ci'), info='设备编号')
    device_type_id = db.Column(db.Integer, info='设备类型')
    user_id = db.Column(db.String(20, 'utf8_general_ci'), info='用户学号，工号')
    demage_state_id = db.Column(db.ForeignKey('损坏状态表.id', ondelete='CASCADE', onupdate='CASCADE'), index=True, info='损坏处理状态')
    user_name = db.Column(db.String(20), info='上报人')
    description = db.Column(db.String(255, 'utf8_general_ci'), info='损坏的描述')
    methods = db.Column(db.String(255), info='处理方法，是个json格式')


## 实用工具

def query2dict(model_list):
    if isinstance(model_list,list):  #如果传入的参数是一个list类型的，说明是使用的all()的方式查询的
        if isinstance(model_list[0],db.Model):   # 这种方式是获得的整个对象  相当于 select * from table
            lst = []
            for model in model_list:
                dic = {}
                for col in model.__table__.columns:
                    dic[col.name] = getattr(model,col.name)
                lst.append(dic)
            return lst
        else:                           #这种方式获得了数据库中的个别字段  相当于select id,name from table
            try:
                lst = [dict(zip(r.keys, r)) for r in model_list]
            except:
                lst = [r._asdict() for r in model_list] # # sqlalchemy.util._collections.result
            return lst
    else:                   #不是list,说明是用的get() 或者 first()查询的，得到的结果是一个对象
        if isinstance(model_list,db.Model):   # 这种方式是获得的整个对象  相当于 select * from table limit=1
            dic = {}
            for col in model_list.__table__.columns:
                dic[col.name] = getattr(model_list,col.name)
            return dic
        else:    #这种方式获得了数据库中的个别字段  相当于select id,name from table limit = 1
            return dict(zip(model_list.keys(),model_list))

