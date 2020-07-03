from device_manager.models import *
from device_manager.utils import *
import os
from flask import Flask, Response, request, render_template, jsonify
from flask import Blueprint
from datetime import datetime, timedelta
import device_manager.utils.global_var as gol
import numpy as np
admin_setting=Blueprint('admin_setting',__name__)

@admin_setting.route('/setting', methods=['GET','POST'])
def setting():
    return_dict = {}
    type_id = request.values.get("type_id")
    time = request.values.get("time") # 默认30天


@admin_setting.route('/set_money', methods=['GET','POST'])
def set_money():
    return_dict = {}
    
    teacher_money = request.values.get("teacher_money")
    student_money = request.values.get("student_money")


    res = db.session.query(User_type).filter(User_type.user_type_id == 1).first()
    res.wages = int(teacher_money)
    db.session.commit()

    res = db.session.query(User_type).filter(User_type.user_type_id == 2).first()
    res.wages = int(student_money)
    db.session.commit()

    return_dict["code"] = 1

    return jsonify(return_dict)

@admin_setting.route('/give_money', methods=['GET','POST'])
def give_money():
    money = request.values.get("money")

    res =db.session.query(User).filter(User.user_type == 1).all()
    for i in range(len(res)):
            res[i].money = res[i].money + money

    res =db.session.query(User).filter(User.user_type == 1).all()
    for i in range(len(res)):
            res[i].money = res[i].money + money
    db.session.commit()
    return jsonify({"code":1})

# @scheduler.scheduled_job('cron', id='interval_wages', minute='1' ) # day='last sun'
def interval_wages():
    res =db.session.query(User_type).filter(User_type.user_type_id == 1).first()
    teacher_wages = res.wages
    res =db.session.query(User_type).filter(User_type.user_type_id == 2).first()
    student_wages = res.wages

    res =db.session.query(User).filter(User.user_type == 1).all()
    for i in range(len(res)):
        if res[i].money <= teacher_wages:
            res[i].money = res[i].money if teacher_wages + res[i].money <= res[i].wages else res[i].wages

    res =db.session.query(User).filter(User.user_type == 2).all()
    for i in range(len(res)):
        if res[i].money <= student_wages:
            res[i].money = res[i].money if student_wages + res[i].money <= res[i].wages else res[i].wages
    db.session.commit()

