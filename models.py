from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean

Base=registry().generate_base()

engine=create_engine("sqlite:///db.sqlite")

class Comment(Base):
    __tablename__="comment"
    id=Column(Integer, primary_key=True)
    name=Column(String(30 ))
    date=Column(DateTime())
    comment_text=Column(Text())
    points=Column(Integer)
    is_registered=Column(Boolean)
    page_number=Column(Integer)

Base.metadata.create_all(engine)