from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('postgresql+psycopg2://postgres:admin@127.0.0.1:5432/myown')
engine = create_engine('postgresql+psycopg2://ieopcjmfavotog:2T0rwgU2gJDF6b1ARLk6ZIHsal@ec2-54-225-246-33.compute-1.amazonaws.com:5432/d1b3hpvloc15mu')
#engine = create_engine('sqlite:///C:\\Users\\Laptop\\PycharmProjects\\DataTransmissionTest\\dbs\\sqliteDB.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))



Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)