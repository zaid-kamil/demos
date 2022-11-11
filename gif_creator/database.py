# create a user table, gif table

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Gif(Base):
    __tablename__ = "gif"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  

engine = create_engine('sqlite:///database.sqlite3', echo=True)
Base.metadata.create_all(bind=engine)
