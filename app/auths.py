# -*- coding: utf-8 -*-
import jwt, datetime, time
from flask import jsonify
from app.model import User
from app import common
from conf.config import config
import os
from werkzeug.security import check_password_hash,generate_password_hash
from app.until.response import response


#加载配置
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

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, cfg.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

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
                #返回值
                # return common.jsonresp(jsonobj=token.decode(),status=200)
                return response(data={'token':token.decode()},status=200)
            else:
                return common.jsonresp(status=400,errinfo='密码不正确')

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                # result = common.falseReturn('', '请传递正确的验证头信息')
                result = common.jsonresp(status=400,errinfo='请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    
                    user = User.get(User.id==payload['data']['id'])
                    user_info=common.obj_to_dict(user)
                    if (user is None):
                        # result = common.falseReturn('', '找不到该用户信息')
                        result = common.jsonresp(status=400,errinfo='找不到该用户信息')
                    else:
                        # result = common.trueReturn(user.id, '请求成功')
                        
                        result = common.jsonresp(jsonobj=user_info,status=200)
                        # if (user.login_time == payload['data']['login_time']):
                        #     result = common.trueReturn(user.id, '请求成功')
                        # else:
                        #     result = common.falseReturn('', 'Token已更改，请重新登录获取')
                else:
                    # result = common.falseReturn('', payload)
                    result = common.jsonresp(jsonobj=payload)
        else:
            # result = common.falseReturn('', '没有提供认证token')
            result = common.jsonresp(status=400,errinfo='没有提供认证token')
        return result

    def getuserinfo(self,usertoken):
        payload = self.decode_auth_token(usertoken)
        if not isinstance(payload, str):
                    
            user = User.get(User.id==payload['data']['id'])
            user_info=common.obj_to_dict(user)
            if (user is None):
                result = response(data={},status_code=400)
            else:
                #将role_id的id转换成对应的角色：1-admin 2-tester
                if (user_info['id']==1):
                    user_info['role_id'] = ['admin']
                else:
                    user_info['role_id']=['editor']
                print(user_info)
                result = response(data={'user_info':user_info},status_code=200)
        else:
            result = response(data={'user_info':payload},status_code=200)
        return result
    
    

