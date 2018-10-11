
from flask import jsonify
from .code import Code


def response(data={}, msg="请求成功", status_code=200, status=Code.SUCCESS.code):
    resp = jsonify()
    try:
        output = jsonify({"status": status, "data": data, "msg": msg})
    except TypeError as e:
        output = jsonify({"status": -1, "data": data, "msg": str(e)})
    resp = output
    # 解决ie下，请求json数据提示下载文件的问题
    resp.headers['Content-Type'] = 'text/json; charset=UTF-8'
    # 允许跨域请求
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers["Access-Control-Allow-Methods"] = "PUT,POST,GET,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Content-Length, Authorization, Accept,X-Requested-With"
    return resp
