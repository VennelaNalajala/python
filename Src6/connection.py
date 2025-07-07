import configparser
from sqlalchemy import create_engine
def sqlserver():
    config=configparser.ConfigParser()
    config.read('config.ini')
    engine=create_engine(config['server']['engine'])
    return engine.raw_connection()