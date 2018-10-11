from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
from app.auths import Auth
from app.model import User
from app.until.response import response

@rest.route('/getuser',methods=['GET'])
@rest.route('/getuser/<id>',methods=['GET'])
def get_user(id=None):
    if id == None:
        userlist = User.select(User.id,User.username,User.status,User.role_id)
        result = userlist
    else:
        userlist = User.select(User.id,User.username,User.status,User.role_id).where(User.id == id)
        result = userlist
        # return response(data={'userinfo':common.query_to_list(userinfo)},status_code=200)
    
    return response(data={'userlist':common.query_to_list(result)},status_code=200)