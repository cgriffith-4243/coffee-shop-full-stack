import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
    GET /drinks
        public endpoint
        response contains drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def show_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]

        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
    GET /drinks-detail
        requires the 'get:drinks-detail' permission
        response contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def show_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]

        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(404)

'''
    POST /drinks
        creates a new row in the drinks table
        requires the 'post:drinks' permission
        response contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    error = False
    form = request.get_json()
    # verify payload contains essential data
    title = form.get('title', None)
    recipe = form.get('recipe', None)
    
    if not (title and recipe):
        abort(422)
    # attempt insertion of new entry
    try:
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )

        drink.insert()
    except:
        error = True
    finally:
        if not error:
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        else:
            abort(422)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        updates the corresponding row for <id>
        requires the 'patch:drinks' permission
        response contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, id):
    error = False
    form = request.get_json()
    # verify payload contains essential data
    title = form.get('title', False)
    recipe = form.get('recipe', False)

    drink = Drink.query.get(id)
    # if entry with matching id is found, attempt updating attribute values
    if drink:
        try:
            # only update if payload value is not None
            drink.title = title if title else drink.title
            drink.recipe = json.dumps(recipe) if recipe else drink.recipe
            
            drink.update()
        except:
            error = True
        finally:
            if not error:
                return jsonify({
                    'success': True,
                    'drinks': [drink.long()]
                })
            else:
                abort(422)
    else:
        abort(404)

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        deletes the corresponding row for <id>
        requires the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    error = False

    drink = Drink.query.get(id)
    # if entry with matching id is found, attempt deletion
    if drink:
        try:
            drink.delete()
        except:
            error = True
        finally:
            if not error:
                return jsonify({
                    'success': True,
                    'delete': id
                })
            else:
                abort(422)
    else:
        abort(404)

## Error Handling
'''
error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
error handling for resource not found
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
error handling for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code