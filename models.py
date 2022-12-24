# from sqlalchemy import create_engine
# from sqlalchemy.orm import registry
# from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean
from flask_sqlalchemy import SQLAlchemy
database=SQLAlchemy()



class Comment(database.Model):
    # __tablename__="comment"
    id=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(30 ))
    date=database.Column(database.DateTime())
    comment_text=database.Column(database.Text())
    points=database.Column(database.Integer)
    is_registered=database.Column(database.Boolean)
    page_number=database.Column(database.Integer)
