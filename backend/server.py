from flask import Flask,request,render_template, jsonify,Response,make_response
import json
from flask_cors import CORS
import pickle
import random 
import sys
# from Monolithic.postgres_utils import global_init_db,global_init_db_vector
from Monolithic.utils import print_statement,valid_user,query_generator,register,get_users_verification_status,fetch_user_data
# from Monolithic.postgres_utils import global_init_db,global_init_db_vector
import logging
from logging import FileHandler
import traceback

import datetime
import traceback

# from db_ops import *
# from constants import *
# from utils import *
from datetime import datetime
app = Flask(__name__,template_folder='assets/html_templates')

app.debug = True

cors = CORS(app, resources={r"/": {"origins": ""}})

app.logger.handlers.clear()
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

app.logger.debug("Hello World")
ENVIRONMENT = "Server"





@app.route('/register', methods=['POST','OPTIONS'])
def register_user():
    
    dict_ = request.data.decode("UTF-8")
    print_statement("\n dict_ : ",dict_)
    mydata = None
    try:
        mydata = json.loads(dict_)        
    except:
        print_statement('Error in json parsing')
        return {"data":False}
  
    print_statement("\n received value : ",mydata) 
    status_user,already_exist_users,comment=  register(mydata)
    if status_user:
        if already_exist_users == "already":
            return {"status" : False,"message":"Phone number or Email Id already exist"} 
        else:
            return {"status" : True,"message":"Success","verification_status":comment} 
    else:
        return {"status" : False,"message":"Phone number or Email Id already exist"}                

@app.route('/checklogin', methods=['GET','POST'])
def signin():
    ui_param = request.args.get('ui')
    # print("login",request.data.decode("UTF-8"))
    dict_ = request.data.decode("UTF-8")
    mydata = json.loads(dict_)
    outputResponse = get_users_verification_status(mydata['useremail'], mydata['password'])
    if outputResponse['message'] in ['User does not exist','Password does not match']:
        outputResponse['data'] = False
        return outputResponse
    else:
        return {"data":False}
    

@app.route('/upload_files', methods=['POST', 'OPTIONS'])
def upload_book_files():
    # Try to parse the form data and files
    try:
        user_id   = request.form.get('user_id')
        files_data = request.files.getlist('attachments')
        user_query = request.form.get("user_query")
        usecase = request.form.get("usecase")
    except Exception as e:
        print_statement('Error in parsing request:', str(e))
        return jsonify({"status": False, "msg": "Error in parsing request"}), 400
    
    # Extract and validate authorization token
    headers = request.headers
    bearer = headers.get('Authorization')
    if not bearer:
        return jsonify({"status": False, "msg": "Authorization header is missing"}), 401
    token = bearer.split()[1]
    status, user_id = valid_user(token)
    if not user_id:
        return jsonify({"status": False, "msg": "Invalid user or token"}), 401
    
    # Create workspace and upload files
    query,status= query_generator(files_data,user_id,user_query,usecase)
    if status:
        return jsonify({'status': True, 'data': query}), 201
    else:
        return jsonify({'status': False, 'data': None, 'msg': 'Workspace creation or file upload failed'}), 500
    

@app.route('/getUserDetails', methods=['GET','POST'])
def getUserDetails():
    # print("login",request.data.decode("UTF-8"))
    dict_ = request.data.decode("UTF-8")
    mydata = json.loads(dict_)
    outputResponse,status = fetch_user_data(mydata['user_id'])
    if status:
        return {"data" : outputResponse}
    else:
        return {"data":False}   





@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Hello world :)</h1>"

if __name__ == '__main__':
    # print_statement("Server initated")
    # Initialisaing logger
    logging.basicConfig(filename='serverlog_'+str(datetime.today().strftime("%D").replace("/","-"))+'.log', level=logging.DEBUG, force=True, filemode='a')
    # print_statement('---------------------------------------Started')
    
    #initialising db
    # global_init_db()
    
    #For live x.cloobot.ai/backend
    if ENVIRONMENT == "Server":
        app.run(host='0.0.0.0', port=5000, debug=True ,use_reloader=False)