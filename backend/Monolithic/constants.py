GPT_35_16K = 0
OPENAI_ENGINE_NAME_GPT3_5_16K = "Cloobot-ChatGPT3-16k"
OPENAI_ENGINE_NAME_GPT3_5_16K_V2 = "Cloobot-ChatGPT35-16k-SwitzNorth"
OPENAI_ENGINE_NAME_GPT3_5_16K_V3 = "Cloobot-ChatGPT35-16k-SwitzNorth"

GPT_4_32K = 1
OPENAI_ENGINE_NAME_GPT4_32K = "Cloobot-32K-GPT4"
OPENAI_ENGINE_NAME_GPT4_32K_V2 = "Cloobot-ChatGPT4-32k-SwitzNorth"
OPENAI_ENGINE_NAME_GPT4_32K_V3 = "Cloobot-ChatGPT4-32k-CanadaEast"

GPT_VECT_EMBED = 2
OPENAI_ENGINE_NAME_GPT_VECT_EMBED = "Cloobot-ChatGPT4-VectEmbed-32k-EastUS"

GPT_4o_50k = 3
OPENAI_ENGINE_NAME_GPT4o_50k = "GPT4o"


GPT_4O_12K = 4
OPENAI_ENGINE_NAME_GPT4O_12K = "brd_image_indexing"



JSON_OBJ = 0
JSON_LIST = 1
JSON_NONE = 2

# to be modified based on the azure storage account
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=idscloobotxstorage;AccountKey=UGtDhvfkbDKqQSqxXs6F0R6Z2GBZamz+2kn7CNK4lM+lJ57Qn6rOvluzA8LcdkSLHOENYMG55aOk+AStYpFloA==;EndpointSuffix=core.windows.net"


######################## database credentials ############################

DB_HOST = "sim-scam-db.postgres.database.azure.com"
DB_PASS = "AjZgsNUME8N8swdAAKvQ"
DB_USER = "admin_simscam"
DB_PORT = 5432
DB_NAME = "postgres"



#############################################


OpenAI_Res_Depl_ID_Map = {}
OpenAI_Res_Depl_ID_Map[OPENAI_ENGINE_NAME_GPT_VECT_EMBED] = "vector_embedding_test_1"