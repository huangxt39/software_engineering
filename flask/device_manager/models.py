
from flask_sqlalchemy import SQLAlchemy
# from device_manager import create_app

db = SQLAlchemy(use_native_unicode='utf8')

class User(db.Model):
    __tablename__ = '用户表'
    __bind_key__ = 'users' # 已设置__bind_key__,则采用设置的数据库引擎
    
    wxid = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='微信号')
    user_type = db.Column(db.Integer)
    user_id = db.Column(db.String(8, 'utf8_general_ci'), info='学号/工号')
    name = db.Column(db.String(10, 'utf8_general_ci'))
    phone_number = db.Column(db.String(11, 'utf8_general_ci'))
    email = db.Column(db.String(50, 'utf8_general_ci'))
    photo = db.Column(db.LargeBinary())



class Device_information(db.Model):
    __tablename__ = '设备信息表'
    __bind_key__ = 'device'

    device_id = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True)
    device_type = db.Column(db.Integer)
    status = db.Column(db.String(5, 'utf8_general_ci'))
    position = db.Column(db.String(30, 'utf8_general_ci'))



class Device_limit(db.Model):
    __tablename__ = '设备借用上限表'
    __bind_key__ = 'device'

    device_type = db.Column(db.Integer, primary_key=True)
    student_limit = db.Column(db.Integer)
    teacher_limit = db.Column(db.Integer)



class Device_type(db.Model):
    __tablename__ = '设备类型表'
    __bind_key__ = 'device'

    device_type = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(10, 'utf8_general_ci'))
    description = db.Column(db.String(50, 'utf8_general_ci'))


class School_information(db.Model):
    __tablename__ = '师生信息表'
    __bind_key__ = 'school' 

    id = db.Column(db.String(8, 'utf8_general_ci'), primary_key=True, info='学号/工号')
    type = db.Column(db.String(2, 'utf8_general_ci'), nullable=False, info='学生/老师')
    name = db.Column(db.String(10, 'utf8_general_ci'), nullable=False)

class Borrow_check(db.Model): 
    __tablename__ = '借用审批记录表'
    __bind_key__ = 'record'

    id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True)
    submit_check = db.Column(db.String(8, 'utf8_general_ci'))
    borrow_check = db.Column(db.String(8, 'utf8_general_ci'))
    return_check = db.Column(db.String(8, 'utf8_general_ci'))

class Borrow_record(db.Model):  
    __tablename__ = '设备借用记录表'
    __bind_key__ = 'record' 

    id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    device_type = db.Column(db.Integer)
    user_id = db.Column(db.String(8, 'utf8_general_ci'))
    user_name = db.Column(db.String(10, 'utf8_general_ci'))
    borrow_reason = db.Column(db.String(255, 'utf8_general_ci'))
