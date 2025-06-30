import pandas as pd
import json
from sqlalchemy import create_engine
import pyodbc
df=pd.read_json('project.json')
engine=create_engine("mssql+pyodbc://DESKTOP-NFGVTDJ\SQLEXPRESS/mongodb?driver=ODBC+Driver+17+for+sql+server&trusted_connection=yes")

for _,row in df.iterrows():
    technology=','.join(row['technologies'])
    row['technologies']=technology

df.to_sql("projects",engine,if_exists='replace',index=False)
