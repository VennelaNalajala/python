import configparser
from sqlalchemy import create_engine
from sqlalchemy.sql import text
def mysql():
    config=configparser.ConfigParser()
    config.read(r"C:\Users\Vennela\Desktop\pipeline2\config.ini")
    engine=config['mysql']['engine']
    return engine
