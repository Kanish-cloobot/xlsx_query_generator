import traceback
import psycopg2
import psycopg2.extras
# connecting flask
from psycopg2.extras import execute_values

from constants import *

conn = None
conn_vector = None

    
def global_init_db(force = False):
    
    #initializing postgresql database
    global conn
    # print('In global_init_db', conn)
    
    try:
        if((not conn) or force):
            # print('In global_init_db::r2::')
            
            conn = psycopg2.connect(database=DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return cur
    except Exception as e:
        print('Connection to pg db failed::',e)
        reset_db(e)
    return None


def reset_db(e):
    if e and ('interfaceerror' in str(e).lower()):
        # print("interface error :: detected")
        global_init_db(force=True)
    else:
        # print("common error :: detected")
        try:
            global conn
            conn.rollback()
        except Exception as e:
            print("except while reset :: ",e)
            global_init_db(force=True)
    return True


def insert_new_row(table_name, rowDict):
    # print('sssssssssssssssssssssssssss')
    cur = global_init_db()
    if cur:
        exec_str = get_insert_row_exec_str(table_name, rowDict)
        # print('insernewrow::',exec_str)
        try:
            cur.execute(exec_str)
            update_db()
            # rows = cur.fetchall()
            return True
            # for row in rows:
            #     #print(row)
        except Exception as e:
            print("Error in cur.execute::",e,"::",exec_str)
            reset_db(e)
            
    return False

def get_insert_row_exec_str(table_name, rowDict):
    exec_str = "INSERT INTO " + table_name + " ("
    exec_str += ",".join(rowDict.keys()) 
    exec_str += ") VALUES ("
    val_str_list = []
    for key in rowDict:
        if type(rowDict[key]) == int:
            val_str_list.append(str(rowDict[key]))
        else:
            if not rowDict[key] or rowDict[key] == '':
                rowDict[key] = ""
            val_str_list.append("\'" + str(rowDict[key]).replace('\'','"') + "\'")
    exec_str += ",".join(val_str_list) 
    exec_str += ")"
    return exec_str


def update_db():
    global conn
    conn.commit()




def get_rows_by_col(table_name, key=None, val=None, opt_conds=None, order_by=None,adt_col_list = None,opt_conds_dict= None):
    # print('in grbc::', table_name, '::', key, '::', val, '::', opt_conds," :: ",order_by," :: ",opt_conds_dict)
    cur = global_init_db()
    # print("in grbc::1")
    if cur:
        # print("in grbc::2")
        # by default get all
        if adt_col_list:
            sel_cols = ",".join(adt_col_list)
            exec_str = "SELECT *," + sel_cols + " from " + table_name
        else:
            exec_str = "SELECT * from " + table_name
        if key and val != None:
            if type(val) == int:
                exec_str  += " WHERE " + key + "=" + str(val)
            else:
                exec_str +=  " WHERE " + key + "='" + val + "'"

        if opt_conds:
            if key and val != None:
                exec_str += " AND " + opt_conds
            else:
                exec_str += " WHERE " + opt_conds
        # print("in grbc::3")
        if opt_conds_dict:
            # print("in grbc::4")
            add_cond_str = ""
            for each_k,each_v in opt_conds_dict.items():
                if add_cond_str:
                    add_cond_str += (" AND " +\
                                      each_k + " = " +\
                                      (str(each_v) if isinstance(each_v,int) else ("'" + each_v + "' ")))
                else:
                    add_cond_str += ( each_k + " = " +\
                                      (str(each_v) if isinstance(each_v,int) else ("'" + each_v + "' ")))
            if key and val != None:
                exec_str += " AND " + add_cond_str
            else:
                exec_str += " WHERE " + add_cond_str

        if order_by:
            exec_str += " ORDER BY " + order_by 
        # print("check exec_str command : ",exec_str)
        try:
            # print("check command : ",exec_str)
            # if (PG_TABLE_GPT_JOB_META_TRACK in exec_str):
                # print("\n\n\n\ncheck PG_TABLE_GPT_JOB_META_TRACK command : ",exec_str)
            cur.execute(exec_str)
            update_db()
            rows = cur.fetchall()
            # print("\n frank_try : ",rows)
            # if (PG_TABLE_GPT_JOB_META_TRACK in exec_str):
            #     print('fetched rows :: ',rows)
            return rows
            # for row in rows:
            #     #print(row)
        except Exception as e:
            print("Error in cur.execute::",e,"::",exec_str)
            reset_db(e)
            
    return []


def update_row(table_name, rowDict, cond_key=None, cond_value=None, opt_conds=None):
    cur = global_init_db()
    if cur:
        exec_str = get_update_row_exec_str(table_name, rowDict, cond_key, cond_value, opt_conds)
        if 'WHERE' in exec_str or 'where' in exec_str:
            # if PG_TABLE_GPT_JOB_META_TRACK in exec_str:
            #     print('update_row::',exec_str)
            try:
                # print('update_row::',exec_str)
                cur.execute(exec_str)
                update_db()
                # print("\n\nsuccess")
                return True
            except Exception as e:
                print("Error in cur.execute::",e,"::")
                reset_db(e)

    return False



def get_update_row_exec_str(table_name, rowDict, cond_key=None, cond_value=None, opt_conds=None,return_col = None):
    # print("\n\n\ncheck : ",table_name, rowDict, cond_key, cond_value, opt_conds)
    exec_str = "UPDATE " + table_name + " SET "
    # #print("exec 1: ",exec_str)
    val_list = []
    for key in rowDict:
        if type(rowDict[key]) == int:
            val_list.append(key + "=" + str(rowDict[key]) )
        else:
            if rowDict[key] not in  ['null','None']:
                val_list.append(key + "='" + str(rowDict[key]).replace("'","''") + "'")
            else:
                # print("im out")
                val_list.append(key + "=" + str(rowDict[key]).replace("'","''") + "")
    exec_str += ",".join(val_list)
    # print("exec 2: ",exec_str)
    opt_flag = True
    if cond_value:
        exec_str += " WHERE "
        if type(cond_value) == int:
            exec_str += cond_key + "=" + str(cond_value) 
        else:
            if cond_value not in  ['null','None']:
                exec_str += cond_key + "='" + str(cond_value) + "'"
            else:
                exec_str += cond_key + "= null "
        # #print("exec 3: ",exec_str)
        if opt_conds:
            exec_str += " and "+opt_conds
            opt_flag = False
            
    if opt_conds and opt_flag:
        exec_str += " WHERE "+opt_conds

    if return_col != None:
        exec_str += " RETURNING " + return_col

    if exec_str == "":
        return None
    # print("\n\n\nexec_str1\n\n",exec_str)
    # print("\n\n\nexec_str2\n\n",exec_str.replace('None','null'))
    return exec_str



def exec_fetch_all(query_string):
    # print("\n exec all query string : ",query_string)
    try:
        cursor = global_init_db()
        if cursor:
            cursor.execute(query_string)
            data = cursor.fetchall()
            cursor.close()
            return data
    except Exception as e:
        print("Error in cur.execute::",e,"::",query_string)
        reset_db(e)
        
    return []


def insert_new_row_return_id(table_name, rowDict,return_col):
    cur = global_init_db()
    if cur:
        exec_str = get_insert_row_exec_str(table_name, rowDict) + " RETURNING " + return_col
        # print('insernewrow::',exec_str)
        # try:
        # if PG_TABLE_INSTANT_SCHEDULER in exec_str:
        #     print("PG_TABLE_INSTANT_SCHEDULER :: ",exec_str)
        try:
            cur.execute(exec_str)
            
            update_db()
            # rows = cur.fetchall()
            return True,cur.fetchone()[0]
        except Exception as e:
            print("Error in cur.execute::",e,"::",exec_str)
            reset_db(e)
            
        # for row in rows:
        #     #print(row)
        # except Exception as e:
        #     print("Error in cur.execute::",e,"::",exec_str)
        #     reset_db(e)
    else:
        print("no cur")
    return False,None


def exec_without_fetch(query_string):
    # print("\n exec_without_fetch query string : ",query_string)
    try:
        cursor = global_init_db()
        if cursor:
            cursor.execute(query_string)
            update_db()
            cursor.close()
    except Exception as e:
        print("Error in cur.execute::",e,"::",query_string)
        reset_db(e)
        
    return True


# Read functions
def get_row_by_id(table_name, id_key, id_val):
    cur = global_init_db()
    if cur:
        exec_str = "SELECT * from " + table_name
        if id_key and id_val:
            if type(id_val) == int:
                exec_str += " WHERE " + id_key + "=" + str(id_val)
            else:
                exec_str += " WHERE " + id_key + "='" + id_val + "'"

        try:
            cur.execute(exec_str)
            update_db()
            rows = cur.fetchall()
            return rows
            ##print(rows)
            # for row in rows:
            #     #print(row['user_id'])
        except Exception as e:
            print("Error in cur.execute::",e,"::",exec_str)
            reset_db(e)
            
    return []
