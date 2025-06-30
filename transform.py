import pandas as pd
import json
from sqlalchemy import create_engine
import pyodbc
df=pd.read_json('unstructured.json')
for _,row in df.iterrows():
    technology=','.join(row['technologies'])
    row['technologies']=technology
normalised = pd.json_normalize(df['client'])
df = df.drop(columns='client').join(normalised)
df['project_manager'] = df['team'].apply(lambda x: x.get('project_manager') if isinstance(x, dict) else None)
df['members'] = df['team'].apply(lambda x: x.get('members') if isinstance(x, dict) else [])
df = df.explode('members')
members_df = pd.json_normalize(df['members']).add_prefix('member_')
df = df.drop(columns=['team', 'members'], errors='ignore').reset_index(drop=True).join(members_df)
df['milestones'] = df['milestones'].apply(lambda x: x if isinstance(x, list) else [])
df = df.explode('milestones')
milestones_df = pd.json_normalize(df['milestones']).add_prefix('milestone_')
df = df.drop(columns=['milestones'], errors='ignore').reset_index(drop=True).join(milestones_df)
engine=create_engine("mssql+pyodbc://DESKTOP-NFGVTDJ\SQLEXPRESS/mongo2?driver=ODBC+Driver+17+for+sql+server&trusted_connection=yes")
df.to_sql("projects",engine,if_exists='replace',index=False)