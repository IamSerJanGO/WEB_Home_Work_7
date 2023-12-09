import configparser
import pathlib

from  sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker

#URI: postgresql://username:password@domain.potr/database

fil_conaig = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(fil_conaig)

user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
db = config.get('DEV_DB', 'DB_NAME')
port = config.get('DEV_DB', 'PORT')
domain = config.get('DEV_DB', 'DOMAIN')

URI = f'postgresql://{user}:{password}@{domain}:{port}/{db}'
engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)

DBSession = sessionmaker(bind=engine)
session = DBSession()

