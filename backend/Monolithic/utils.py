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
from Monolithic.constants import *
import os
from litellm import completion
from Monolithic.postgres_utils import get_row_by_id



os.environ['GEMINI_API_KEY'] = "AIzaSyChbvX4KEqTygPSYTEEtp7e24cAGdNE3Ag"



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

def register(mydata):
    # Create organisation and get the status and org_id
    
    # If organisation creation is successful
    if mydata:
        people_info = [{
            "user_name": mydata['user_name'],
            "user_password": mydata['password'],
            "user_email": mydata['email'],
            "code": mydata['code'],
        }]
        
        # Call people_update_changes to update user data
        sign_up_type = 'email'
        if 'sign_up_type' in mydata and mydata['sign_up_type'] == 'Google':
            sign_up_type = 'Google'
            
        people_status, already, comments = people_update_changes(people_info, org_id, sign_up_type)
        
        # If user already exists
        if already == "Already_exist":
            return False, already, comments
        
        print_statement("people_status,already ::", people_status, already)
        # If google signup alone - make automatically verified because they are already verified by Google
        if people_status  and sign_up_type == 'Google':
            user_id = already
            insert_user_verification(user_id,mydata['email'],'Google')
        return True, already, comments
    
    # If organisation creation failed
    else:
        return False, [], []
    

def valid_user(token):
    try:
        decode = jwt.decode(token, JWT_SECRET,algorithms=['HS256'])
        # print("decode ::", decode)
        user_info = get_row_by_id(PG_TABLE_USERS, pg_col_name_dict[PG_TABLE_USERS][PG_TABLE_USERS], decode['user_id'])
        # print("user_info::", user_info)
        if len(user_info):
            try:
                return True, decode['user_id']
            except:
                return True, decode['user_id']
    except:
        print_statement("\n\n\nerror in jwt\n\n\n")
    return False, None


def query_generator(file_data, user_id, user_query):
    if file_data:
        temp_schema = ""
        # Iterate through all files in the file_data list
        for filename in file_data:
            if filename.endswith((".xls", ".xlsx")):  # Check for Excel files
                # Check if the file is an absolute path or relative
                if not os.path.isabs(filename):
                    # Construct the full path using the current working directory
                    file_path = os.path.join(os.getcwd(), filename)
                else:
                    file_path = filename

                # Ensure the file exists
                if not os.path.exists(file_path):
                    print(f"File does not exist: {file_path}")
                    continue

                # Read the Excel file into a pandas DataFrame
                df = pd.read_excel(file_path)
                df = df.head(10)

                # Construct the table name (strip file extension)
                table_name = os.path.splitext(os.path.basename(file_path))[0]
                prompt = extraction_prompt.replace("<df>", df.to_string(index=False))
                prompt = prompt.replace("<table_name>", table_name)
                response = completion(
                    model= MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_NONE",
                        },
                    ]
                )
                res = response.choices[0].message.content.strip()
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
                response = completion(
                    model=MODEL,
                    messages=messages,
                        )
                query = response.choices[0].message.content
                return query