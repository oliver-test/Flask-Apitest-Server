# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, TextField, DateTimeField, fn
import datetime
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


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

# 建表
def create_table():
    db.connect()
    db.create_tables([ Api, User])


if __name__ == '__main__':
    create_table()
