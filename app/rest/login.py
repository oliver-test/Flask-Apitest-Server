from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
app = Flask(__name__)

@rest.route('/',methods=['POST','GET'])
@rest.route('/login',methods=['POST','GET'])
def login():
    '''
    用户登陆接口
    return:token
    '''
    username = request.form.get('username')
    password = request.form.get('password')

    print(username,password)
    if (not username or not password):
    #    msg = '用户名和密码不能为空'
    #    status = '200'
       return common.jsonresp(status=400,errinfo='用户名和密码不能为空')
    else:
        msg='登陆成功'
        status = '200'
        return jsonify(status,msg)

