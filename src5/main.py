from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from .newconnection import sqlserver

app=FastAPI()

class Restaurent(BaseModel):
    foodtype:str
    foodname:str
    availability:str

@app.get('/')
def home():
    return 'welcome to Brundavanam'

#for new todo insertion(create)
@app.post('/add_menu/')
def insert(new:Restaurent):
    connection=sqlserver()
    if not connection:
        raise HTTPException (status_code=500,detail="Database connection failed")
    cursor=connection.cursor()
    cursor.execute("Insert into Restaurent(foodtype,foodname,availability) values(?,?,?)",(new.foodtype,new.foodname,new.availability))
    connection.commit()
    connection.close()
    return 'insertion succesfull'


#for fetching all(read)
@app.get('/fetch_all/')
def fetching():
    connection=sqlserver()
    if not connection:
        raise HTTPException(status_code=500,detail="Database connection failed")
    cursor=connection.cursor()
    cursor.execute("select * from restaurent")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    connection.close()
    result = [dict(zip(column_names, row)) for row in rows]
    return result


#updating the columns(update)
@app.put('/updating/{foodtype}:{availability}')
def update(foodtype:str,availability:str):
    connection=sqlserver()
    if not connection:
        raise HTTPException (status_code=500,detail="Database connection failed")
    cursor=connection.cursor()
    cursor.execute(f"update restaurent set availability=? where foodtype=?",(availability,foodtype))
    connection.commit()
    connection.close()
    return 'insertion succesfull'


#deleting (delete)
@app.delete('/deleteitem_menu/{foodname}')
def deleting(foodname:str):
    connection=sqlserver()
    if not connection:
        raise HTTPException (status_code=500,detail="Database connection failed")
    cursor=connection.cursor()
    cursor.execute("delete from restaurent where foodname=?",foodname)
    connection.commit()
    connection.close()
    return 'deletion succesfull'
    
