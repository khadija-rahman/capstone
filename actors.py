import os
from flask import Flask, Blueprint, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from functools import wraps
from models import setup_db, Movies, Actors
from auth import requires_auth

actors_controller = Blueprint('actors_controller', __name__)

# GET all Actors
@actors_controller.route("/actors")
@requires_auth("get:actors")
def actors(jwt):
    actors = Actors.query.all()

    return jsonify({
        "success": True,
        "actors": [actor.format() for actor in actors]
    })

# GET Actor by ID
@actors_controller.route("/actors/<actor_id>")
@requires_auth("get:actors")
def actor(jwt, actor_id):
    actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

    if actor is None:
        abort(404)

    return jsonify({
        "success": True,
        "actor": actor.format()
    })

# DELETE Actor
@actors_controller.route("/actors/<actor_id>", methods=['DELETE'])
@requires_auth("delete:actor")
def delete_actor(jwt, actor_id):
    actor = None
    try:
        actor = Actors.query.filter(
            Actors.id == actor_id).one_or_none()
    except:
        abort(422)

    if actor is None:
        abort(404)

    try:
        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor.id
        })
    except:
        abort(422)

# CREATE/POST new Actor
@actors_controller.route("/actors", methods=['POST'])
@requires_auth("add:actor")
def add_actor(jwt):
    body = request.get_json()
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
        actor = Actors(name=new_name, age=new_age, gender=new_gender)

        actor.insert()

        return jsonify({
            'success': True,
            'created': actor.id,
        })
    except BaseException as e:
        print(e)
        abort(422)


# UPDATE/PATCH Actor
@actors_controller.route("/actors/<actor_id>", methods=['PATCH'])
@requires_auth("update:actor")
def update_actor(jwt, actor_id):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
        actor = Actors.query.filter(
            Actors.id == actor_id
        ).one_or_none()
        
        if actor is None:
            abort(404)

        actor.name = new_name
        actor.age = new_age
        actor.gender = new_gender

        actor.update()

        return jsonify({
            "success": True,
            "actor": actor.format()
        })
    except BaseException as e:
        print(e)
        abort(500)
