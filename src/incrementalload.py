import pandas as pd
from sqlalchemy import create_engine,inspect
from ssmsconn import ssms
from mysqlconn import mysql
from datetime import datetime
from sqlalchemy import text

engine1=create_engine(ssms())
engine2=create_engine(mysql())
inspector=inspect(engine2)


if not(inspector.has_table('customers')):
    df=pd.read_sql('select * from customers',engine1)
    df.to_sql('customers',engine2,if_exists='fail',index=False)
else:
    max_date=pd.read_sql('select max(last_updated) from customers',engine2)
    max_date=max_date.iloc[0,0]
    query = text("SELECT * FROM customers WHERE last_updated > :max_date")
    newrec = pd.read_sql(query, engine1, params={"max_date": max_date})
    if not newrec.empty:
            newrec['last_updated']=datetime.now()
            newrec.to_sql('customers',engine2,if_exists='append',index=False)
            print("New records found and appended")
    else:
            print("new records not found")
    df1=pd.read_sql("select * from customers where status='Active' order by customer_id ",engine1)
    df2=pd.read_sql("select * from customers where status='Active' order by customer_id ",engine2)
    df1=df1.drop('last_updated',axis=1)
    df2=df2.drop('last_updated',axis=1)
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)
    ud=[]
    for _,row in df1.iterrows():
        cid=row['customer_id']
        old=df2[df2['customer_id']==cid]
        if not old.empty:
            ssms=row.drop(['customer_id','status'])
            mysql=old.iloc[0].drop(['customer_id','status'])
            if not ssms.equals(mysql):
                ud.append(row)
                with engine2.connect() as conn:
                    conn.execute(text(f"update customers set status='Inactive' where customer_id={cid}"))
                    conn.commit()
            
    if ud:
            print('updates found working on it')
            update=pd.DataFrame(ud)
            update['status']='Active'
            update['last_updated']=datetime.now()
            update.to_sql('customers',engine2,if_exists='append',index=False)
            print('updates found and Updated')
    else:
            print('updates not found')
    
   
 

