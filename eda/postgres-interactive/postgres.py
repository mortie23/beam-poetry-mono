# %%
import psycopg2
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv

# %%
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
PG_USERNAME = os.getenv("PG_USERNAME")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOSTNAME = os.getenv("PG_HOSTNAME")

# %%
# Establish a connection to the database
connection = psycopg2.connect(
    host=PG_HOSTNAME,
    dbname="mortimer_dev",
    user=PG_USERNAME,
    password=PG_PASSWORD,
)

# %%
# Execute a SELECT statement
sql = "SELECT * FROM mortimer_nfl.venue"

# Use pandas to execute the query and store the result in a DataFrame
df = pd.read_sql_query(sql, connection)

# %%
