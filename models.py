
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


_timer = time.perf_counter() #time.clock 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#class User(db.Model):
    # __tablename__ = 'UserRemap'
    # userName = db.Column("name",db.String(100))
    # #id = db.Column("id", db.Integer, primary_key = True)
    # #id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100))  
    # complete = db.Column(db.Boolean)
    #pass

class ToDO(db.Model):
    __tablename__ = 'toDO'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))  
    complete = db.Column(db.Boolean)

    def __init__(self,item): 
        self.item = item 
        self.complete = False 
    
    def __repr__(self):
        return '<Content %s>' % self.item

    
    
    #pass
