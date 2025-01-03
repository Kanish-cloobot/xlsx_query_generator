from flask import Flask,request,render_template, jsonify,Response,make_response
import json
from flask_cors import CORS
import pickle
import random 
import sys
# from Monolithic.postgres_utils import global_init_db,global_init_db_vector
from Monolithic.utils import print_statement,valid_user,query_generator
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








@app.route('/check_login', methods=['POST'])
def check_login():
    try:
        mydata = json.loads(request.data.decode("UTF-8"))
        print_statement("get_round_format Json : ", json.dumps(mydata, indent=4))
        status, user_id = login_user(mydata['user_name'])
        return {"status": status, "user_id": user_id,"msg": "User logged in successfully"}
    except json.JSONDecodeError:
        print_statement('Error in json parsing')
        print_statement(traceback.format_exc())
        return {"data": False, "msg": "Error in parsing request"}

@app.route('/ids_register', methods=['POST','OPTIONS'])
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
            return {"status" : False,"message_type":"Phone number or Email Id already exist"} 
        elif status_user:
            if 'sign_up_type' in mydata and mydata['sign_up_type'] == 'Google':
                outputResponse = get_users_verification_status(mydata['email'], mydata['password'])
                outputResponse['status'] = True
                outputResponse['message_type'] = 'Success'
                return outputResponse
            else:
                return {"status" : True,"message_type":"Success","verification_status":comment} 
    else:
        return {"status" : False,"message_type":"Phone number or Email Id already exist"}   
    




@app.route('/upload_files', methods=['POST', 'OPTIONS'])
def upload_book_files():
    # Try to parse the form data and files
    try:
        user_id   = request.form.get('user_id')
        files_data = request.files.getlist('attachments')
        user_query = request.form.get("user_query")
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
    status,id= query_generator(files_data,user_id,user_query)
    if status:
        return jsonify({'status': True, 'data': status}), 201
    else:
        return jsonify({'status': False, 'data': None, 'msg': 'Workspace creation or file upload failed'}), 500
    

    





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