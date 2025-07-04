import boto3
import pyodbc
from sqlalchemy import create_engine
import pandas as pd

dynamo = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamo.Table('dynamopipeline')
items = table.scan()['Items']

df=pd.DataFrame(items)
df['technologies']=df['technologies'].apply(lambda x:','.join(x))
df.drop(columns=['_id'], inplace=True)

engine=create_engine("mssql+pyodbc://DESKTOP-NFGVTDJ\SQLEXPRESS/dynamodb?driver=ODBC+Driver+17+for+sql+server&trusted_connection=yes")
df.to_sql('projects',engine,if_exists='replace',index=False)