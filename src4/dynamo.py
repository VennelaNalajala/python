from pymongo import MongoClient
import boto3


client = MongoClient('mongodb://localhost:27017/')
mongo_db = client["mongo"]
mongo_collection = mongo_db["collection"]
dynamo = boto3.resource("dynamodb", region_name="ap-south-1")  
dynamo_table = dynamo.Table("dynamopipeline")
for document in mongo_collection.find():
    document["_id"] = str(document["_id"])
    dynamo_table.put_item(Item=document)

print("Transfer complete") 
