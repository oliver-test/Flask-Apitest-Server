from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
from app.auths import Auth
from app.model import User
from playhouse.shortcuts import model_to_dict
from app.until.response import response
app = Flask(__name__)

@rest.route('/',methods=['POST','GET'])
@rest.route('/login',methods=['POST','GET'])
def login():
    '''
    用户登陆接口
    return:token
    '''
    data = json.loads(request.get_data(as_text=True))
    # username = request.form.get('username')
    # password = request.form.get('password')
    username = data['username']
    password = data['password']


    if (not username or not password):
    #    msg = '用户名和密码不能为空'
    #    status = '200'
       return common.jsonresp(status=400,errinfo='用户名和密码不能为空')
    else:
        print(Auth.authenticate(Auth,username,password))
        return Auth.authenticate(Auth,username,password)

@rest.route('/user',methods=['POST'])
def checktoken():
    '''
    对token进行鉴权，获取用户信息
    :return:json
    '''
    result = Auth.identify(Auth,request)
    return common.jsonresp(jsonobj=result,status=200)

@rest.route('/getuserinfo',methods=['GET'])
def getuserinfo():
    '''
    解析token
    返回用户信息
    '''
    usertoken = request.args.get('token')
    result = Auth.getuserinfo(Auth,usertoken)
    return result