# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, TextField, DateTimeField, fn
import datetime
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import os




db = MySQLDatabase('education', host='39.107.92.144', user='root', passwd='mcr2018..', charset='utf8', port=3306)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)

# 用户表
class User(UserMixin, BaseModel):
    
    username = CharField(verbose_name='用户名',null=False)  # 用户名
    password = CharField(verbose_name='密码',null=False)  # 密码
    status = IntegerField(verbose_name='状态',null=False,default=0)#状态-0正常-1禁用
    role_id = IntegerField(verbose_name='角色')#角色-1用户-0管理员

    @staticmethod
    def check_password(tpassword,raw_password):
        return check_password_hash(tpassword,raw_password)
    
    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

class Api(BaseModel):
    api_ame = CharField(verbose_name='接口名称',null=False) 
    url = CharField(verbose_name='接口地址',null=False)
    Method = CharField(verbose_name='请求方法',null=False,default='GET')
    Hearders = CharField(verbose_name='请求头',null=False)
    Body = CharField(verbose_name='请求参数',null=False)
    Params = CharField(verbose_name='参数',null=False)
    Cookies = CharField(verbose_name='缓存',null=False)
    # Upload_file
    Status = CharField(verbose_name='状态',null=False)
    Description = CharField(verbose_name='描述',null=False)
    Create_time = DateTimeField()
    Update_time = DateTimeField()


def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['__data__']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict

def query_to_list(query, exclude=None):
    list = []
    for obj in query:
        dict = obj_to_dict(obj, exclude)
        list.append(dict)
    return list


db.connect()

userlist = User.select()
print(query_to_list(userlist))
