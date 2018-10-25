from flask import Flask,request
from . import rest
import jwt,datetime,time,json
from flask import jsonify
from app import common
from app.auths import Auth
from app.model import User
from app.until.response import response
from peewee import SQL

@rest.route('/user/getuser',methods=['GET'])
def get_user():
    
    
    # if id == None and username == None:
    #     userlist = User.select(User.id,User.username,User.status,User.role_id)
    #     result = userlist
    # if id != None and username == None:
    # userlist = User.select(User.id,User.username,User.status,User.role_id).where(User.id == id)
    #     result = userlist
    #     # return response(data={'userinfo':common.query_to_list(userinfo)},status_code=200)
    # if id == None and username != None:
    #     userlist = User.select(User.id,User.username,User.status,User.role_id).where(User.username == username)
    #     result = userlist
    # userlist = User.select(User.id,User.username,User.status,User.role_id)
    # result = userlist
    username = request.args.get('username')
    role_id = request.args.get('userrole')
    status = request.args.get('status')
    if username or role_id or status:
        userlist = User.select(User.id,User.username,User.status,User.role_id).where(User.status != '10')
        try:
            if username:
                userlist = userlist.where(User.username == username)
            #    userlist = User.select(User.id,User.username,User.status,User.role_id).where(User.username == username)   
            if role_id:
                userlist = userlist.where(User.role_id == role_id)
            if status:
                userlist = userlist.where(User.status == status)
            # userlist = User.select(User.id,User.username,User.status,User.role_id).where(SQL(sql_content))
            # userlist = User.raw('select User.id,User.username,User.status,User.role_id from User Where (%s)',sql_content)
        except:
            # return utils.jsonresp(status=404, errinfo='查询不到资料')
            return response(msg='No data available',status_code=404)
        return response(data={'userlist':common.query_to_list(userlist)},status_code=200)
    else:
        #全量查询
        try:
            # 当前页码
            page = request.args.get('page')
            if page: 
                page = int(page)
            # 每页展示数量
            length = request.args.get('limit')
            if length:
                length = int(length)
            else:
                length = cfg.ITEMS_PER_PAGE
            # 排序
            sort = request.args.get('sort')
            if sort:
                sort_column = 'id'
                if sort == '+id':
                # sort_column = sort.split('+')[1]
                    sort_direction = 'asc'
                else:
                    sort_direction = 'desc'

            # 搜索
            search_value = request.args.get('searchValue', '')
        except:
            return response(data={},status_code=200,msg='参数格式不正确')
        
        #查询
        query = User.select(User.id,User.username,User.status,User.role_id).where(User.status != '10')
        total_count = query.count()
            
        #根据sort进行判断排序
        if sort:
            if sort_column in User._meta.fields:
                field = getattr(User, sort_column)
                if sort_direction != 'asc':
                    field = field.desc()
                query = query.order_by(field)
        #分页
        if page:
                    query = query.paginate(page, length)

    

        return response(data={'userlist':common.query_to_list(query),'totalElements': total_count},status_code=200)




# @rest.route('/user/update',methods=['POST'])
@rest.route('/user/update',methods=['POST'])
def update_user():
    '''
    修改用户接口
    return:json
    '''
    data = json.loads(request.get_data(as_text=True))
    print(data)
    # user_id = request.form.get('id')
    # status = request.form.get('status')
    user_id = data['id']
    status = data['status']
    try:
        User.update({User.status : status}).where(User.id == user_id).execute()
    except:
        return response(msg='Request params not valid',status_code=404)
    
    return response(msg='success',status_code=200)


