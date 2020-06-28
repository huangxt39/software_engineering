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