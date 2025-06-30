import configparser
from sqlalchemy import create_engine
from sqlalchemy.sql import text
def ssms():
    config=configparser.ConfigParser()
    config.read(r"C:\Users\Vennela\Desktop\pipeline2\config.ini")
    engine=config['server']['engine']
    return engine