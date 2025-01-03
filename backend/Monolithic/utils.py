from datetime import datetime,timedelta
import time
import json
import re
import requests
import logging
import hashlib
import jwt
import tempfile
import random
import math
import pandas as pd
from mimetypes import guess_extension
import google.generativeai as genai
from Monolithic.constants import *
import os
from litellm import completion
from Monolithic.postgres_utils import get_row_by_id,get_rows_by_col,insert_new_row,insert_new_row_return_id


os.environ['GEMINI_API_KEY'] = "AIzaSyChbvX4KEqTygPSYTEEtp7e24cAGdNE3Ag"
genai.configure(api_key=os.getenv("AIzaSyChbvX4KEqTygPSYTEEtp7e24cAGdNE3Ag"))

def setup_gemini():
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 8192,
        
    }
    
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

def get_gmt_timestamp():
    return datetime.utcnow()


def print_statement(*args):
    # logger = logging.getLogger(__name__)
    # logger.debug(args)
    print(datetime.now(),args, flush=True)
    # ps(args)



def convert_datetime_to_string(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # Convert to ISO 8601 format
    return data



def register(mydata,normal_user = False):
    email_user_row = get_user_row_from_mail_id(mydata['email'])
    if email_user_row == None:
        people_info = [{
            "user_name":mydata['username'],
            "user_password":mydata['password'],
            "user_email":mydata['email'],
        }]
        people_status,already,comment = people_update_changes(people_info)
        print(people_status,already,comment)
        if already == "Already_exist":
            return False,already,None
        print_statement("people_status,already :: ",people_status,already)
        return True,already,comment
    else:
        return False,[],None
    
def get_users_verification_status(useremail, password):    #  function verifies that the mail is in the users table and user_verification table
    print("user_email", useremail, "password", password)
    try:
        user_info = get_rows_by_col(PG_TABLE_USERS, "lower(" + pg_col_name_dict[PG_TABLE_USERS][2] + ")", useremail.lower())[0]
        # print("user_info ::",user_info)
        user_id = user_info[0]
        # print(user_info)
        if user_id:
            return get_token(useremail, password)
        else:
            return {"message":"User does not exist"}
    except Exception as e:
        print("get_users_verification_status :: Exception Occurred :: ",e)
        return {"message":"User does not exist"}
    
def people_update_changes(people_info):
    if people_info:
        user_email    = people_info[0]['user_email']
        user_name     = people_info[0]['user_name']
        user_password = people_info[0]['user_password']
        email_info    = get_rows_by_col(PG_TABLE_USERS,pg_col_name_dict[PG_TABLE_USERS][2],user_email)
        if not email_info:
            status,user_id = create_new_user(user_name,user_email,user_password)
            if user_id:
                comment = "User created successfully"
            return status,user_id,comment
        else:
            return False,"Already_exist",None
        

def create_new_user( 
                        user_name,
                        user_email,
                        user_password
                    ):
    print_statement('createnewuser::',user_name, user_password)
    
    if insert_new_row(PG_TABLE_USERS, {
        
            pg_col_name_dict[PG_TABLE_USERS][1] : user_name,
            pg_col_name_dict[PG_TABLE_USERS][2] : user_email,
            pg_col_name_dict[PG_TABLE_USERS][3] : user_password,
            pg_col_name_dict[PG_TABLE_USERS][4] : get_gmt_timestamp(),
            pg_col_name_dict[PG_TABLE_USERS][5] : 1
        }):
        print_statement('createnewuser::user created')

        user_id = get_user_id_from_email(user_email)
        
        return True,user_id

    return False,None



def get_user_id_from_email(useremail):
    user_info = get_rows_by_col(PG_TABLE_USERS, pg_col_name_dict[PG_TABLE_USERS][2], useremail)     
    if len(user_info):
        row = user_info[0]
        return row[0]
    return None
    

def get_user_row_from_mail_id(userEmail):
    user_info = get_rows_by_col(PG_TABLE_USERS, opt_conds = " lower(trim(both from " + pg_col_name_dict[PG_TABLE_USERS][2] + ")) = '" + userEmail.lower().strip() + "' ")      
    if len(user_info):
        row = user_info[0]
        return row
    return None
    

def valid_user(token):
    try:
        decode = jwt.decode(token, JWT_SECRET,algorithms=['HS256'])
        # print("decode ::", decode)
        user_info = get_row_by_id(PG_TABLE_USERS, pg_col_name_dict[PG_TABLE_USERS][0], decode['user_id'])
        # print("user_info::", user_info)
        if len(user_info):
            try:
                return True, decode['user_id']
            except:
                return True, decode['user_id']
    except:
        print_statement("\n\n\nerror in jwt\n\n\n")
    return False, None

def get_jwt_token(payload):
    return jwt.encode( payload, JWT_SECRET, algorithm='HS256')

def get_token(useremail, password):
    user_info = get_rows_by_col(PG_TABLE_USERS,opt_conds= " lower(" + pg_col_name_dict[PG_TABLE_USERS][2] + ") = '" + useremail.lower() + "' ")
    if len(user_info):
        row = user_info[0]
        if(row[2] == password):
            payload = {
                'user_id': row[0],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            #prepare token for new user
            encoded = get_jwt_token(payload)
            hashed_pwd = hashlib.md5(str.encode(row[3])).hexdigest()

            return {"data":encoded,"user_id":row[0],"auth_level":row[5],"status":"old","user_name":user_info[0][1],"secret":hashed_pwd}

    return {"data":False}


def query_generator(file_data, user_id, user_query, usecase):
    if file_data:
        print("file_data ::", file_data)
        temp_schema = ""
        
        # Iterate through all files in the file_data list
        for file in file_data:
            # Check if the file is an Excel file (based on its extension)
            if file.filename.endswith((".xls", ".xlsx")):  # Check for Excel files
                print(f"Processing file: {file.filename}")
                
                # Define the temporary file path
                temp_path = os.path.join(os.getcwd(), file.filename)
                
                # Save the file temporarily to disk
                file.save(temp_path)
                
                # Ensure the file exists after saving it temporarily
                if not os.path.exists(temp_path):
                    print(f"File does not exist: {temp_path}")
                    continue
                
                # Read the Excel file from the temporary path into a pandas DataFrame
                try:
                    df = pd.read_excel(temp_path)
                    df = df.head(10)  
                
                # Construct the table name (strip file extension)
                    table_name = os.path.splitext(file.filename)[0]
                    print_statement("table_name ::",table_name)
                    model = setup_gemini()
                    # Replace placeholders in the prompt
                    prompt = extraction_prompt.replace("<df>", df.to_string(index=False))
                    prompt = prompt.replace("<table_name>", table_name)
                    # response = completion(
                    #     model= MODEL,
                    #     messages=[{"role": "user", "content": prompt}],
                    #     safety_settings=[
                    #         {
                    #             "category": "HARM_CATEGORY_HARASSMENT",
                    #             "threshold": "BLOCK_NONE",
                    #         },
                    #         {
                    #             "category": "HARM_CATEGORY_HATE_SPEECH",
                    #             "threshold": "BLOCK_NONE",
                    #         },
                    #         {
                    #             "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    #             "threshold": "BLOCK_NONE",
                    #         },
                    #         {
                    #             "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    #             "threshold": "BLOCK_NONE",
                    #         },
                    #     ]
                    # )
                    # res = response.choices[0].message.content.strip()
                    response = model.generate_content(prompt)
                    res = response.text.strip()
                    print_statement("res ::",res)
                    # Look for content between <answer> tags and clean it
                    if '<answer>' in res and '</answer>' in res:
                        json_str = res.split('<answer>')[1].split('</answer>')[0].strip()
                    else:
                        json_str = res.strip()

                    # Basic cleaning - remove any remaining XML-like tags
                    json_str = json_str.replace('<answer>', '').replace('</answer>', '')
                    json_str = json_str.replace('```json', '').replace("```",'')
                    temp_schema = temp_schema + f"-----------------------\n"
                    temp_schema = temp_schema + f"{json_str}\n"


                    prompt = QUERY_PROMPT.replace('{user_query}',user_query).replace('{temp_schema}',temp_schema)


                    messages=[{"role": "user", "content": prompt}]
                    response = model.generate_content(prompt)
                    print_statement("response ::",response)
                    generated_query = response.text.strip()
                    if generated_query:
                        id,status = inser_records(user_id,user_query,usecase,generated_query)
                        os.remove(temp_path)
                    return generated_query,status
                except Exception as e:
                    return None,False
            

def inser_records(user_id,user_query,usecase,generated_query):
    insert_dict = {
            pg_col_name_dict[PG_TABLE_RECORDS][1] : usecase,
            pg_col_name_dict[PG_TABLE_RECORDS][2] : user_query,
            pg_col_name_dict[PG_TABLE_RECORDS][3] : generated_query,
            pg_col_name_dict[PG_TABLE_RECORDS][4] : user_id,
            pg_col_name_dict[PG_TABLE_RECORDS][5] : get_gmt_timestamp(),
            pg_col_name_dict[PG_TABLE_RECORDS][6] : user_id,
            pg_col_name_dict[PG_TABLE_RECORDS][7] : get_gmt_timestamp(),
            pg_col_name_dict[PG_TABLE_RECORDS][8] : 1
    }
    status,id = insert_new_row_return_id(PG_TABLE_RECORDS,insert_dict,pg_col_name_dict[PG_TABLE_RECORDS][0])
    return id , True

def fetch_user_data(user_id):
    user_info = get_rows_by_col(PG_TABLE_USERS, pg_col_name_dict[PG_TABLE_USERS][0], user_id)
    if user_info:
        user_name = user_info[0][1]
        user_mail = user_info[0][2]
        return {"username":user_name,"email":user_mail},True
    return {user_info:"User does not exist"},False


def get_user_id_from_email(useremail):
    user_info = get_rows_by_col(PG_TABLE_USERS, pg_col_name_dict[PG_TABLE_USERS][2], useremail)     
    if len(user_info):
        row = user_info[0]
        return row[0]
    return None