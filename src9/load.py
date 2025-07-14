
from connection import sqlserver
import pandas as pd
def load(df):
    engine=sqlserver()
    df=pd.DataFrame(df)
    df.to_sql('sharetable',engine,if_exists='replace',index=False)

