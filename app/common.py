# -*- coding: utf-8 -*-

import json
import datetime
from app.model import User,Api
from flask import Response


#封装http响应
def jsonresp(jsonobj=None, status=200, errinfo=None):
    if status >= 200 and status < 300:
        jsonstr = json.dumps(jsonobj, ensure_ascii=False, default=datetime_handler)
        return Response(jsonstr, mimetype='application/json', status=status)
    else:
        return Response('{"errinfo":"%s"}' % (errinfo,), mimetype='application/json', status=status)

# peewee转dict
def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['__data__']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        # return x.isoformat()
        return x.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Unknown type")