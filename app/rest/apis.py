from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
from app.model import Api
from app.until.response import response
from peewee import SQL
from webargs import fields
from webargs.flaskparser import parser

class MultType(fields.Field):
    # 自定义field，body中的default字段不限制类型
    def _serialize(self, value, attr, obj):
        return value.default


body_field = {
    "default": MultType(attribute='default'),
    "key": fields.Str(),
    "value": fields.Str()
}

# 接口输入参数schema
request_field = {
    "name": fields.Str(required=True),
    "group": fields.Str(allow_none=True),
    "url": fields.Str(),
    "method": fields.Str(),
    "headers": fields.List(fields.Dict(), allow_none=True),
    "body": fields.List(fields.Nested(body_field), allow_none=True),
    "params": fields.List(fields.Dict(), allow_none=True),
    "cookies": fields.List(fields.Dict(), allow_none=True),
    "status": fields.Str(allow_none=True),
    "description": fields.Str(allow_none=True)
}

query_args = {
    'id':fields.Int(),
    'api_name': fields.Str(),
    'group': fields.Str(),
    'status': fields.Str(),
    "page": fields.Int(missing='1'),
    "limit": fields.Int(missing='20'),
    "sort": fields.Str()
   
}



@rest.route('/apis/getapilist',methods=['GET'])
def get_apilist():
    '''
    获取接口列表

    '''
    args = parser.parse(query_args, request)
    try:
        # 当前页码
        page = args.get('page')
        # 每页展示数量
        length = args.get('limit')
        apilist = Api.select().where(Api.Status != 10)
        if args.get('api_name'):
            apilist = apilist.where(Api.api_name == args.get('api_name'))
        if args.get('group'):
            apilist = apilist.where(Api.group == args.get('group'))
        if args.get('status'):
            apilist = apilist.where(Api.Status == args.get('status'))
            print('status')
        apilist = apilist.paginate(page, length)
    except:
        return response(data={},status_code=200,msg='参数格式不正确')
    
    return response(data={'apilist':common.query_to_list(apilist),'totalElements': apilist.count()},status_code=200)

@rest.route('/apis/updateapi',methods=['POST'])
def update_api_status():
    '''
    修改状态接口
    '''
    args = parser.parse(query_args, request)
    try:
        Api.update(Status = args.get('status'),Update_time = datetime.datetime.now()).where(Api.id == args.get('id')).execute()
        # User.update({User.status : status}).where(User.id == user_id).execute()
    except:
        return response(msg='Request params not valid',status_code=404)
    
    return response(msg='success',status_code=200)

    
    


@rest.route('/apis/saveapi',methods=['POST'])
def save_api():
    apilist = Api.select().where(Api.Status == 0 and Api.Status != 10)
    return response(data={'apilist':common.query_to_list(apilist),'totalElements': apilist.count()},status_code=200)

    