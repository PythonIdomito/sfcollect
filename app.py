from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import *

db=SQLAlchemy()
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.instance_path=app.root_path
app.template_folder="templates"
db.init_app(app)

@app.route("/")
def home():
    return render_template("wrapper.html")

@app.route("/results/", methods=["GET"])
@app.route("/results/<int:paginate>", methods=["GET"])
def results(paginate=None):
    paginate=0 if paginate==None else paginate
    allempty=True
    
    for key in request.args.keys():
        if request.args[key]!="" and request.args[key]!=None:
            allempty=False
        else:
            pass
    if allempty: return render_template("results.html", comments=[], len=0)
    
    comments=db.session.query(Comment)
    comments=comments.filter(Comment.comment_text.ilike(request.args["comment"])) if request.args["comment"]!="" else comments
    comments=comments.filter(Comment.name.ilike(request.args["user"]) ) if request.args["user"]!="" else comments
    comments=comments.filter(request.args["is_reg"] == Comment.is_registered) if request.args["is_reg"]!="" else comments
    comments=comments.filter(request.args["points"] <= Comment.points) if request.args["points"]!="" else comments
    
    return render_template("results.html", comments=comments, len=comments.count())