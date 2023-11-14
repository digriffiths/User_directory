from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class users_table(Base):
    __tablename__ = 'users_table'

    id = Column(Integer, Sequence('url_table_id_seq'), primary_key=True)
    name = Column(String)
    email = Column(String)
