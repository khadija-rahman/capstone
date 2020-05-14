import os
from sqlalchemy import Table, ForeignKey, Column, String, TIMESTAMP, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
import json
from sqlalchemy.ext.declarative import declarative_base

database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()


'''
Movies

'''


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(TIMESTAMP)
    # actors = relationship("Actors", secondary="productions")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        # self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


'''
Actors
'''


class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    # movies = relationship("Movies", secondary="productions")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        # self.movies = movies

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# '''
# Production
# '''


# class Production(db.Model):
#     __tablename__ = 'productions'
#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey('movies.id'))
#     actor_id = Column(Integer, ForeignKey('actors.id'))

#     movie = relationship(Movies, backref=backref(
#         "productions", cascade="all, delete-orphan"))
#     actor = relationship(Actors, backref=backref(
#         "productions", cascade="all, delete-orphan"))
