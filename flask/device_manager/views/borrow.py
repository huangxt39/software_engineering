from device_manager.utils import *
from flask import Blueprint

borrow=Blueprint('borrow',__name__)

@borrow.route('/')
def show():
    return 'borrow.hello'