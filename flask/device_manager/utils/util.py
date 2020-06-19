from sqlalchemy.util._collections import AbstractKeyedTuple
import datetime
import decimal
import json

def get_dict_list_from_result(result):
    list_dict = []
    for i in result:
        i_dict = i._asdict()  # sqlalchemy.util._collections.result , has a method called _asdict()
        list_dict.append(i_dict)
    return list_dict

def list_dict_to_json(data):
    list_json = []
    for item in data:
        item = json.dumps(item, ensure_ascii=False)
        list_json.append(item)
    return json.dumps(list_json, ensure_ascii=False)


def db_datalist_to_dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, list):  # 列表解析
        if len(res_obj) == 0:
            return None
        if isinstance(res_obj[0], AbstractKeyedTuple):  #
            dic_list = datalist_format([dict(zip(result.keys(), result)) for result in res_obj])
            if dic_list:
                for item in dic_list:
                    for key in item.keys():
                        if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                            item[key] = str(item[key])
            return dic_list
        elif isinstance(res_obj[0], TTDModel):
            [item.__dict__.pop("_sa_instance_state") for item in res_obj]
            return datalist_format([item.__dict__ for item in res_obj])
        elif isinstance(res_obj[0], dict):  #在db中存在json字段时返回的是dict
            return datalist_format(res_obj)
        else:
            return None
    else:
        return db_data_to_dict(res_obj)
#
# 数据库返回单个数据 转 dict
#
def db_data_to_dict(res_obj):
    if not res_obj:
        return None
    if isinstance(res_obj, dict):
        return res_obj
    elif isinstance(res_obj, AbstractKeyedTuple):
        # 转成字典
        dict_obj = data_format(dict(zip(res_obj.keys(), res_obj)))
        # 把null 转空字符串
        if res_obj and len(res_obj.keys()) > 0:
            for key in res_obj.keys():
                if not dict_obj[key]:
                    dict_obj[key] = ""
                if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                    dict_obj[key] = str(dict_obj[key])

        return dict_obj
    elif isinstance(res_obj, TTDModel):
        res_obj.__dict__.pop("_sa_instance_state")
        return data_format(res_obj.__dict__)
    else:
        return None


def datalist_format(reslist):
    """
    列表 中 时间格式datetime.datetime  转 [2018:12:12 10:10:56]
    :param res: 列表
    :return:
    """
    if not reslist or not isinstance(reslist, list):
        return reslist
    for item in reslist:
        for key in item.keys():
            if isinstance(item[key], datetime.datetime) \
                    or isinstance(item[key], datetime.date):
                item[key] = str(item[key])
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
    return reslist


def data_format(bean):
    """
    对象 中 时间格式datetime.datetime  转 [2018:12:12 10:10:56]
    :param bean: 传入dict
    :return:
    """
    if not bean or not isinstance(bean, dict):
        return bean
    for key in bean.keys():
        if isinstance(bean[key], datetime.datetime) \
                or isinstance(bean[key], datetime.date):
            bean[key] = str(bean[key])
        if isinstance(bean[key], decimal.Decimal):
            bean[key] = float(bean[key])
    return bean

## 可用
def existing_database(db):
    for i in db.get_tables_for_bind():
        print(i)
    all_table = {table_obj.name: table_obj for table_obj in db.get_tables_for_bind()}
    return all_table

## 可用
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream