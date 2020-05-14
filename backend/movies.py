import os
from flask import Flask, Blueprint, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from functools import wraps
from models import setup_db, Movies, Actors
from auth import requires_auth

movie_controller = Blueprint('movie_controller', __name__)

# GET all Movies
@movie_controller.route("/movies")
@requires_auth("get:movies")
def movies(jwt):
    movies = Movies.query.all()

    return jsonify({
        "success": True,
        "movies": [movie.format() for movie in movies]
    })

# GET Movie by ID
@movie_controller.route("/movies/<movie_id>")
@requires_auth("get:movies")
def movie(jwt, movie_id):
    movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    return jsonify({
        "success": True,
        "movie": movie.format()
    })

# DELETE Movie
@movie_controller.route("/movies/<movie_id>", methods=['DELETE'])
@requires_auth("delete:movie")
def delete_movie(jwt, movie_id):
    movie = None
    try:
        movie = Movies.query.filter(
            Movies.id == movie_id).one_or_none()
    except:
        abort(422)

    if movie is None:
        abort(404)

    try:
        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie.id
        })
    except:
        abort(422)

# CREATE new Movie
@movie_controller.route("/movies", methods=['POST'])
@requires_auth("add:movie")
def add_movie(jwt):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
        movie = Movies(title=new_title, release_date=new_release_date)

        movie.insert()

        return jsonify({
            'success': True,
            'created': movie.id,
        })
    except:
        abort(422)

# UPDATE/PATCH movie
@movie_controller.route("/movies/<movie_id>", methods=['PATCH'])
@requires_auth("update:movie")
def update_movie(jwt, movie_id):
    body = request.get_json()
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
        movie = Movies.query.filter(
            Movies.id == movie_id
        ).one_or_none()

        if movie is None:
            abort(404)

        movie.title = new_title
        movie.release_date = new_release_date

        movie.update()

        return jsonify({
            "success": True,
            "movie": movie.format()
        })
    except BaseException as e:
        print(e)
        abort(500)
