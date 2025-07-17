import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
mongo_host = config["mongodb"]["host"]
mongo_port = int(config["mongodb"]["port"])
mongo_db_name = config["mongodb"]["database"]
sql_conn_str = config["server"]["engine"]
mongo_client = MongoClient(mongo_host, mongo_port)
mongo_db = mongo_client[mongo_db_name]
sql_engine = create_engine(sql_conn_str)
collections = [
    "product_dimension",
    "sales_fact",
    "store_dimension",
    "time_dimension",
    "sales_dimensions"
]
for collection_name in collections:
    print(f"\n Processing collection: {collection_name}")
    data = list(mongo_db[collection_name].find({}, {"_id": 0}))
    if not data:
        print(f" Collection {collection_name} is empty, skipping.")
        continue
    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=["number"]).columns
    object_cols = df.select_dtypes(include=["object"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[object_cols] = df[object_cols].fillna("")
    try:
        df.to_sql(
            name=collection_name,
            con=sql_engine,
            if_exists="replace",
            index=False
        )
        print(f" Successfully uploaded to SQL table: {collection_name}")
    except Exception as e:
        print(f" Failed to upload {collection_name}: {e}")
print("\n All collections processed and uploaded to SQL Server.")
