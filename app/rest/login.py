from flask import Flask,request
from . import rest
import jwt, datetime, time
from flask import jsonify
app = Flask(__name__)

@rest.route('/',methods=['GET'])
def homepage():
    status = 200
    msg='hello world'
    return jsonify(status,msg)
@rest.route('/login',methods=['POST','GET'])
def login():
    username = request.form.get('username')
    # password = request.form.get('password')
    login_time = int(time.time())  
    id = int(1)
    token = encode_auth_token(id,login_time)


