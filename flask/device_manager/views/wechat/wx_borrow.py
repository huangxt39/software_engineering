from device_manager.utils import *
from flask import Blueprint

wx_borrow=Blueprint('wx_borrow',__name__)

@wx_borrow.route('/')
def show():
    return 'borrow.hello'