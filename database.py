# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://dhuougvpvjteqs:c237462613ab7c92b9d5382e7a2f0fea29ac74e46904b58c6e8f043f1cbd8faf@ec2-79-125-13-42.eu-west-1.compute.amazonaws.com:5432/ddtpe15um8rbnq', convert_unicode=True)
#engine = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/qqq')
#engine = create_engine('postgresql+psycopg2://dhuougvpvjteqs:c237462613ab7c92b9d5382e7a2f0fea29ac74e46904b58c6e8f043f1cbd8faf@ec2-79-125-13-42.eu-west-1.compute.amazonaws.com:5432/ddtpe15um8rbnq')
#engine = create_engine('sqlite:///C:\\Users\\DM\\\sqliteDB.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))



Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)