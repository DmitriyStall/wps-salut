from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    password = Column(String(120), unique=False)
    department = Column(String(120), unique=False)
    privileges = Column(Integer, unique=False)
    def __init__(self, login=None, password=None, department=None, privileges=None):
        self.login = login
        self.password = password
        self.department = department
        self.privileges = privileges
    #def __repr__(self):
   #    return '<User %r>' % (self.name)

class RedCard(Base):
    __tablename__ = 'redcards'
    CardID = Column(Integer, primary_key = True)
    CardNumber = Column(Integer, unique = False)
    CardStatus = Column(String(20), unique = False)
    WorkDOer = Column(String(50), unique = False)
    DocFromWhere = Column(String(100), unique = False)
    DocName = Column(String(30), unique = False)
    DocID = Column(String(10), unique = False)
    DocDate = Column(String(10), unique = False)
    WorkDueTo = Column(String(10), unique=False)
    WorkDesc = Column(String(100), unique=False)
    WorkTaker = Column(String(50), unique=False)
    WorkClosedDate = Column(String(10), unique=False)
    def __init__(self, CardNumber = None, CardStatus = None, WorkDOer = None, DocFromWhere = None, DocName = None, DocID = None, DocDate = None, WorkDueTo = None, WorkDesc = None, WorkTaker = None, WorkClosedDate = None):
        self.CardStatus = CardStatus
        self.CardNumber = CardNumber
        self.WorkDOer = WorkDOer
        self.DocFromWhere = DocFromWhere
        self.DocName = DocName
        self.DocID = DocID
        self.DocDate = DocDate
        self.WorkDueTo = WorkDueTo
        self.WorkDesc = WorkDesc
        self.WorkTaker = WorkTaker
        self.WorkClosedDate = WorkClosedDate


