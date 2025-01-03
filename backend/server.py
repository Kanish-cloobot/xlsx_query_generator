from flask import Flask,request,render_template, jsonify,Response,make_response
import json
from flask_cors import CORS
import pickle
import random 
import sys
# from Monolithic.postgres_utils import global_init_db,global_init_db_vector
# from Monolithic.utils import print_statement
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




@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Hello world :)</h1>"

if _name_ == '_main_':
    # print_statement("Server initated")
    # Initialisaing logger
    logging.basicConfig(filename='serverlog_'+str(datetime.today().strftime("%D").replace("/","-"))+'.log', level=logging.DEBUG, force=True, filemode='a')
    # print_statement('---------------------------------------Started')
    
    #initialising db
    # global_init_db()
    
    #For live x.cloobot.ai/backend
    if ENVIRONMENT == "Server":
        app.run(host='0.0.0.0', port=5000, debug=True ,use_reloader=False)