# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class 借用设备表(db.Model):
    __tablename__ = '借用设备表'

    id = db.Column(db.String(10, 'utf8_general_ci'), primary_key=True, nullable=False)
    device_type = db.Column(db.ForeignKey('设备大类型表.big_type_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    num = db.Column(db.Integer, info='这个类型的设备借用了多少')
    state = db.Column(db.String(10), info='此设备借用的状态')

    设备大类型表 = db.relationship('设备大类型表', primaryjoin='借用设备表.device_type == 设备大类型表.big_type_id', backref='借用设备表S')



class 单个设备信息表(db.Model):
    __tablename__ = '单个设备信息表'

    device_id = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='设备编号')
    type_id = db.Column(db.Integer, info='设备类型id')
    state_id = db.Column(db.ForeignKey('设备状态表.state_id', ondelete='CASCADE', onupdate='CASCADE'), index=True, server_default=db.FetchedValue(), info='设备状态')
    position = db.Column(db.String(30, 'utf8_general_ci'), info='设备存放位置')

    state = db.relationship('设备状态表', primaryjoin='单个设备信息表.state_id == 设备状态表.state_id', backref='单个设备信息表S')



class 师生信息表(db.Model):
    __tablename__ = '师生信息表'

    id = db.Column(db.String(8, 'utf8_general_ci'), primary_key=True, info='学号/工号')
    type = db.Column(db.String(2, 'utf8_general_ci'), nullable=False, info='学生/老师')
    name = db.Column(db.String(10, 'utf8_general_ci'), nullable=False)


class 管理员表(师生信息表):
    __tablename__ = '管理员表'

    user_id = db.Column(db.ForeignKey('师生信息表.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, info='学号/工号')
    name = db.Column(db.String(255), info='姓名')
    phone = db.Column(db.String(20), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    account = db.Column(db.String(20), info='账号')
    password = db.Column(db.String(20, 'utf8_general_ci'), info='密码')
    description = db.Column(db.String(255), info='申请描述')



class 待审核管理员表(db.Model):
    __tablename__ = '待审核管理员表'

    user_id = db.Column(db.String(20), primary_key=True, info='学号/工号')
    name = db.Column(db.String(255), info='姓名')
    phone = db.Column(db.String(20), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    account = db.Column(db.String(20), info='账号')
    password = db.Column(db.String(20, 'utf8_general_ci'), info='密码')
    description = db.Column(db.String(255), info='申请描述')



class 损坏状态表(db.Model):
    __tablename__ = '损坏状态表'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10))



class 损坏设备信息表(db.Model):
    __tablename__ = '损坏设备信息表'

    id = db.Column(db.String(20, 'utf8_general_ci'), primary_key=True, info='损坏编号')
    time = db.Column(db.DateTime, info='提交时间')
    device_id = db.Column(db.String(20, 'utf8_general_ci'), info='设备编号')
    device_type_id = db.Column(db.Integer, info='设备类型')
    user_id = db.Column(db.String(20, 'utf8_general_ci'), info='用户学号，工号')
    demage_state_id = db.Column(db.ForeignKey('损坏状态表.id', ondelete='CASCADE', onupdate='CASCADE'), index=True, info='损坏处理状态')
    user_name = db.Column(db.String(20), info='上报人')
    description = db.Column(db.String(255, 'utf8_general_ci'), info='损坏的描述')
    contact = db.Column(db.Integer, info='联系维修师傅')
    track_down = db.Column(db.Integer, info='追查责任人')
    punish = db.Column(db.Integer, info='惩罚损坏人')

    demage_state = db.relationship('损坏状态表', primaryjoin='损坏设备信息表.demage_state_id == 损坏状态表.id', backref='损坏设备信息表S')



class 用户类型表(db.Model):
    __tablename__ = '用户类型表'

    user_type_id = db.Column(db.Integer, primary_key=True, info='用户类型id')
    user_type_name = db.Column(db.String(10), info='用户类型')



class 用户表(db.Model):
    __tablename__ = '用户表'

    wxid = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, info='微信号，真正使用的时候使用UnionID')
    user_type = db.Column(db.Integer, index=True, info='用户类型')
    user_id = db.Column(db.String(8, 'utf8_general_ci'), nullable=False, index=True, info='学号/工号')
    user_name = db.Column(db.String(20), info='用户姓名')
    phone = db.Column(db.String(11, 'utf8_general_ci'), info='电话')
    email = db.Column(db.String(50, 'utf8_general_ci'), info='邮箱')
    photo = db.Column(db.String(20), info='照片路径')



class 订单状态表(db.Model):
    __tablename__ = '订单状态表'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10))



class 设备信息表(db.Model):
    __tablename__ = '设备信息表'

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



class 设备借用记录表(db.Model):
    __tablename__ = '设备借用记录表'

    id = db.Column(db.String(13, 'utf8_general_ci'), primary_key=True, info='订单编号')
    submit_time = db.Column(db.DateTime)
    submit_check = db.Column(db.String(10), info='申请审核人')
    book_borrow_time = db.Column(db.DateTime, info='预约的领取时间')
    actual_borrow_time = db.Column(db.DateTime, info='实际领取设备时间')
    borrow_check = db.Column(db.String(255), info='领取审核人')
    book_return_time = db.Column(db.DateTime, info='预计归还时间')
    return_check = db.Column(db.String(255), info='归还审核人')
    actual_return_time = db.Column(db.DateTime, info='实际归还时间')
    user_id = db.Column(db.String(8, 'utf8_general_ci'), index=True, info='用户id')
    borrow_reason = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue(), info='借用理由')
    state_id = db.Column(db.Integer, index=True, info='订单状态')



class 设备大类型表(db.Model):
    __tablename__ = '设备大类型表'

    big_type_id = db.Column(db.Integer, primary_key=True, info='类型id')
    name = db.Column(db.String(10, 'utf8_general_ci'), info='设备名称')



class 设备状态表(db.Model):
    __tablename__ = '设备状态表'

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(10))
