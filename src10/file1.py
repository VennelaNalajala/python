import configparser
import json
import io
from pymongo import MongoClient
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")
site_url = config["sharepoint"]["site_url"]
username = config["sharepoint"]["username"]
password = config["sharepoint"]["password"]
folder_url = config["sharepoint"]["url"]  
mongo_host = config["mongodb"]["host"]
mongo_port = int(config["mongodb"]["port"])
mongo_db = config["mongodb"]["database"]  
ctx_auth = AuthenticationContext(site_url)
if not ctx_auth.acquire_token_for_user(username, password):
    raise Exception("SharePoint authentication failed")
ctx = ClientContext(site_url, ctx_auth)
folder = ctx.web.get_folder_by_server_relative_url(folder_url)
files = folder.files
ctx.load(files)
ctx.execute_query()
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
for file in files:
    file_name = file.properties["Name"]
    if not file_name.endswith(".json"):
        continue
    collection_name = file_name.replace(".json", "")  
    print(f"\n Processing: {file_name} → Collection: {collection_name}")
    file_url = file.properties["ServerRelativeUrl"]
    download_result = io.BytesIO()
    ctx.web.get_file_by_server_relative_url(file_url).download(download_result).execute_query()
    try:
        download_result.seek(0)
        content = download_result.read().decode("utf-8")
        json_data = json.loads(content)
        if isinstance(json_data, list):
            db[collection_name].insert_many(json_data)
        else:
            db[collection_name].insert_one(json_data)
        print(f"Uploaded to MongoDB collection: {collection_name}")
    except Exception as e:
        print(f" Failed to process {file_name}: {e}")
print("\n All files processed.")
