from device_manager.utils import *
from flask import Blueprint

wx_user=Blueprint('wx_user',__name__)

@wx_user.route('/')
def show():
    return 'record.hello'
