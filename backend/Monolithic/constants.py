
# to be modified based on the azure storage account
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=idscloobotxstorage;AccountKey=UGtDhvfkbDKqQSqxXs6F0R6Z2GBZamz+2kn7CNK4lM+lJ57Qn6rOvluzA8LcdkSLHOENYMG55aOk+AStYpFloA==;EndpointSuffix=core.windows.net"


######################## database credentials ############################

DB_HOST = "localhost"
DB_PASS = "Kanish@2003"
DB_USER = "postgres"
DB_PORT = 5432
DB_NAME = "xlsx_query_generator"



#############################################


MODEL=f"gemini/gemini-2.0-flash-exp",



#Login timeout
JWT_EXP_DELTA_SECONDS = 86400 * 30

#secret code used to encrypt stuff
JWT_SECRET = 'BDa8yfPp29X918cA2e7w'




PG_TABLE_USERS = "users"
pg_col_name_dict = {}
pg_col_name_dict[PG_TABLE_USERS] = {}
pg_col_name_dict[PG_TABLE_USERS][0] = "user_id"
pg_col_name_dict[PG_TABLE_USERS][1] = "user_name"
pg_col_name_dict[PG_TABLE_USERS][2] = "user_mail"
pg_col_name_dict[PG_TABLE_USERS][3] = "user_password"
pg_col_name_dict[PG_TABLE_USERS][4] = "user_created_timestamp" 
pg_col_name_dict[PG_TABLE_USERS][5] = "user_status"


extraction_prompt = """You are tasked with extracting the schema description from a DataFrame and presenting it a text output.
here is the first 10 records of the Table df:
<df>
Instructions:
1. Carefully understand the schema of the dataframe and understand the relations between the columns.
2. for each column generate an one liner description of the column that should have enough context to llm that helps to generate sql query with the scema.
3. Make sure to add example values in description for enriching the context.
4. Dont write any python code in the output.
The output should be in the following format should be wihin the <answer></answer> tags:

<answer>
<table_name> Schema Description:
column : description
column : description
</answer>
The Final output should only contain the <answer></answer> tags.
"""


QUERY_PROMPT = """Given an input question, first create a syntactically correct SQL query to run.
Question: {user_query}
Here is the schema of the database:
{temp_schema}
The final output should only contain the SQL query."""
