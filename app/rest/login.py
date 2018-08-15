from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
from app.auths import Auth
from app.model import User
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


    if (not username or not password):
    #    msg = '用户名和密码不能为空'
    #    status = '200'
       return common.jsonresp(status=400,errinfo='用户名和密码不能为空')
    else:
        print(Auth.authenticate(Auth,username,password))
        return Auth.authenticate(Auth,username,password)


@rest.route('/getuser',methods=['GET'])
@rest.route('/getuser/<id>',methods=['GET'])
def getuser(id=None):
    usermodle = User.get(User.id == id)
    return common.jsonresp(jsonobj=common.obj_to_dict(usermodle))