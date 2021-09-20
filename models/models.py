from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class OnegaiContent(Base):
    __tablename__ = 'onegaicontents'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    body = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, title=None, body=None, date=None):
        self.title = title
        self.body = body
        self.date = date

    def __repr__(self):
        return '<Title %r>' % (self.title)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, user_name=None, hashed_password=None, created_at=None):
        self.user_name = user_name
        self.hashed_password = hashed_password
        self.created_at = created_at

    def __repr__(self):
        return '<Name %r>' % (self.user_name)

