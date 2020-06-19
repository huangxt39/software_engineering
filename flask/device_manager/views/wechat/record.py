from device_manager.utils import *
from flask import Blueprint

record=Blueprint('record',__name__)

@record.route('/')
def show():
    return 'record.hello'


