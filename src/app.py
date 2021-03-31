from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'

mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)  # Parse data to JSON

    # mimetype => So that client get it as JSON
    return Response(response, mimetype='application/json')


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    response = json_util.dumps(user)

    # mimetype => So that client get it as JSON
    return Response(response, mimetype='appication/json')


@app.route('/users', methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        # db.users doesn't exists at this point but mongo creates it if it's not there
        user_id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password}
        )

        response = {
            'id': str(user_id),
            'username': username,
            'password': hashed_password,
            'email': email
        }

        # return response

    else:

        return not_found()

    return {'message': 'received'}


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = mongo.db.users.find_one_and_delete({'_id': ObjectId(user_id)})
    response = jsonify({'message': 'User ' + id + ' was deleted successfully'})

    return Response(response, mimetype='application/json')


@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})

        response = jsonify(
            {'message': 'User ' + str(user_id) + ' was updated successfully'})
        return response


@app.errorhandler(404)
def not_found(error=None):

    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })

    response.status_code = 404

    return response


# App init
if __name__ == '__main__':
    app.run(debug=True)
