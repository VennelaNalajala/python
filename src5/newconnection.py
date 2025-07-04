import configparser
from sqlalchemy import create_engine
def sqlserver():
    config=configparser.ConfigParser()
    config.read(r"C:\Users\Vennela\Desktop\fastapi\config.ini")
    engine=create_engine(config['server']['engine'])
    return engine.raw_connection()