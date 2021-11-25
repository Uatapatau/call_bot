from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()


def create_db():
    engine = create_engine('sqlite:///sqlite.db')
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    return engine


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,
                unique=True)

    user_id = Column(String(length=12))
    balance = Column(Integer)

    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance


class History(Base):

    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,
                unique=True)

    user_id = Column(String(length=12))
    type = Column(Text)
    data = Column(Text)

    def __init__(self, user_id, data, type):
        self.user_id = user_id
        self.type = type
        self.data = data


class Promo(Base):

    __tablename__ = 'promo'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,
                unique=True)

    bonus_id = Column(String(length=12))
    bonus = Column(Integer)
    data = Column(Text)
    def __init__(self, bonus_id, bonus,data):
        self.bonus_id = bonus_id
        self.bonus = bonus
        self.data= data

def create_row(engine, table, kwargs):
    with Session(engine) as session:
        row = session.query(table).filter_by(**kwargs).first()
        if row is None:
            session.add(table(**kwargs))
            session.commit()
            return False
        else:
            return True

def create_promo(engine, bonus_id, kwargs):
    with Session(engine) as session:
        row = session.query(Promo).filter_by(bonus_id=bonus_id).first()
        if row is None:
            session.add(Promo(**kwargs))
            session.commit()
            return False
        else:
            return True


def update_promo(engine,bonus_id, data):
    with Session(engine) as session:
        promo = session.query(Promo).filter_by(bonus_id = bonus_id).first()
        if promo:
            promo.data = data
            session.commit()


def get_row(engine, table, kwargs):
    with Session(engine) as session:
        user = session.query(table).filter_by(**kwargs).first()
        return user

def update_balance(engine, user_id, balance):
    with Session(engine) as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user is not None:
            user.balance = balance
            session.commit()

def create_log(engine, user_id, type, data):
    with Session(engine) as session:
        session.add(History(user_id=user_id, type=type, data=data))
