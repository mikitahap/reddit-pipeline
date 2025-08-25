from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from init_database import db_init

class Loader:
    def __init__(self, transformed_data):
        self.__engine, self.__posts =  db_init()
        self.__transformed_data = transformed_data

    def save_to_db(self):
        with self.__engine.connect() as connection:
            connection.execute(self.__posts.insert(), self.__transformed_data)

