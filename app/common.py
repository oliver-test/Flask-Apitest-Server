# -*- coding: utf-8 -*-

import json
import datetime
from app.model import User,Api
from flask import Response,jsonify


#封装http响应
def jsonresp(jsonobj=None, status=200, errinfo=None):
    if status >= 200 and status < 300:
        jsonstr = json.dumps(jsonobj, ensure_ascii=False, default=datetime_handler)
        # return Response(jsonstr, mimetype='application/json', status=status)
        return jsonify({"status": status,"data": jsonobj})

    else:
        return Response('{"errinfo":"%s"}' % (errinfo,), mimetype='application/json', status=status)

# peewee转dict
def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['__data__']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict
#peewee转list
def query_to_list(query, exclude=None):
    list = []
    for obj in query:
        dict = obj_to_dict(obj, exclude)
        list.append(dict)
    return list



# def datetime_handler(x):
#     if isinstance(x, datetime.datetime):
#         # return x.isoformat()
#         return x.strftime("%Y-%m-%d %H:%M:%S")
#     raise TypeError("Unknown type")

def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }

# def obj_to_dict(obj, exclude=None):
#     dict = obj.__dict__['__data__']
#     if exclude:
#         for key in exclude:
#             if key in dict: dict.pop(key)
#     return dict