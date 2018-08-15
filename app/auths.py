# -*- coding: utf-8 -*-
import jwt, datetime, time
from flask import jsonify
from app.model import User
from app import common
from conf.config import config
import os
from werkzeug.security import check_password_hash,generate_password_hash

#加载配置文件
cfg = config[os.getenv('FLASK_CONFIG') or 'default']

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                cfg.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def authenticate(self, username, password):
        '''
        用户登录，登录成功返回token；登录不成功，返回错误原因
        :param username password
        :return:json
        '''
        try:
            userInfo = User.get(User.username == username)
        except:
            userInfo = None

        if (userInfo is None):
            return common.jsonresp(status=400,errinfo='为查询到用户信息')
        else:
            ture_passowrd = generate_password_hash(userInfo.password)
            if(User.check_password(ture_passowrd,password)):
                login_time = int(time.time())
                token = self.encode_auth_token(userInfo.id,login_time)
                print(token)
                return common.jsonresp(jsonobj=token.decode(),status=200)
            else:
                return common.jsonresp(status=400,errinfo='密码不正确')
    
    
    

