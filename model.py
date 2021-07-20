import pymysql
'''
    db = pymysql.connect('localhost', 'root', '123456', 'r915')
    cursor = db.cursor()
    db.close()
'''

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connect = create_engine("mysql+pymysql://root:dyf201105@localhost:3306/mqs",
                        encoding="utf-8",
                        echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "station_table"
    id = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(255))
    Numbering = Column(String(255))


Base.metadata.create_all(connect)
DBsession = sessionmaker(bind=connect)
session = DBsession()

#new_user = User(name='MAC', passward='123456')

#session.add(new_user)
#session.commit()
#session.close()