import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv() # Search .env file

# Get the enviroment viarables
account = os.getenv("SNOWFLAKE_ACCOUNT")
usr = os.getenv("SNOWFLAKE_USER")
pwd = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

def get_snowflake_connection():
  conn = snowflake.connector.connect(
    account = account,
    user = usr,
    password = pwd,
    role = role,
    warehouse = warehouse,
    database = database,
    schema = schema,
  )

  return conn
