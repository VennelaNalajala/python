from ssmsconn import ssms
from mysqlconn import mysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine1=create_engine(ssms())
engine2=create_engine(mysql())
df1=pd.read_sql('select * from dbo.customers',engine1)
df1.to_sql('customers',engine2,if_exists='fail',index=False)
