from device_manager.utils import *
from flask import Blueprint
from device_manager.models import *
login=Blueprint('login',__name__)

# @login.route('/')
# def show():
#     return 'login.hello'

@login.route('/')
def hello_world():
    # res = db.session.query(User).filter_by(wxid='wxid_kun2nu3lor4x22').with_entities(User.wxid,User.name).all()
    # res = get_dict_list_from_result(res)
    # res_json = list_dict_to_json(res)

    res = db.session.query(School_information).filter_by(id='17363031').with_entities(School_information.id,School_information.type,School_information.name).all()
    res = get_dict_list_from_result(res)
    res_json = list_dict_to_json(res)
    return res_json