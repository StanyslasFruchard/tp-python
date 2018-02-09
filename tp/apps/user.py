from flask import Blueprint, jsonify, request, session
import hashlib 
from models import User, Token, Code
from playhouse.shortcuts import model_to_dict, dict_to_model
import os, binascii
import nexmo
import random
import stripe

client = nexmo.Client(key="72ca6f30", secret="1d2bc4041491906e")

app_user = Blueprint('app_user', __name__)

# login
@app_user.route('/login', methods=['POST'])
def login():
  params = request.get_json() # dict
  try:
    email    = params.get('email')
    password = params.get('password')
    user     = User.get(User.email == email)

    if user.password == password:      
      code = Code.create(user = user, string = random.randint(1000,9999))
      code.save
      '''client.send_message({
        'from': 'Python Test',
        'to': user.mobile,
        'text': "Your authentification code is {code}".format(code = code.string),
      })'''
      # Convert our model (object) to dictionnary
      data = {"user_id" : user.id, "code" : code.string}
      # Jsonify work only with dict, we've to convert everything
      return jsonify({'data': data}), 201
    else:
      return jsonify({'error': 'User not found'}), 404
  except Exception as error:
    return jsonify({'error': 'User not found {error}'.format(error=error) }), 404

# Authentification
@app_user.route('/user/authentification', methods=['POST'])
def authentification():
  params = request.get_json() # dict
  try:
    code     = params.get('code')
    codeUser = Code.get(Code.string == code)
    user     = codeUser.user
    codeUser.delete_instance()
    try:
      userToken = Token.get(Token.user == user)
    except Exception as error:
      userToken = Token.create(user = user, string = binascii.b2a_hex(os.urandom(16)))
      userToken.save()
      # Convert our model (object) to dictionnary
    data = {"user_id" : userToken.user.id, "token" : userToken.string}
    # Jsonify work only with dict, we've to convert everything
    return jsonify({'data': data}), 201
  except Exception as error:
    return jsonify({'error': 'Code not found {error}'.format(error=error) }), 404

# Create user
@app_user.route('/users', methods=['POST'])
def create_user():
  params   = request.get_json() # dict
  email    = params.get('email')
  password = params.get('password')
  mobile   = params.get('mobile')
  try:
    user = User.get(User.email == email)
  except Exception as error:
    customer = stripe.Customer.create(
            email=email,
            description="Test customer",
    )
    user = User.create(email=email, password=password, mobile=mobile, stripe_id=customer.id)
    user.save()
  # Convert our model (object) to dictionnary
  data = {"email" : user.email, "id" : user.id, "mobile" : user.mobile}
  # Jsonify work only with dict, we've to convert everything
  return jsonify({'data': data}), 201

# Get user
@app_user.route('/user/<id>', methods=['GET'])
def get_user(id):
  try:
    user = User.get(user.id == id)
    # We convert once again
    data = {"email" : user.email, "id" : user.id}

    # We send the information to the browser
    return jsonify({'data': data}), 201
  except Exception as error:
    return jsonify({'error': 'User not found {error}'.format(error=error) }), 404

# Modify user
@app_user.route('/user/<id>', methods=['PUT'])
def put_user(id):
  try:
    user   = User.get(User.id == id)
    params = request.get_json() # dict

    if params.get('email', None) is not None :
      user.email = params.get('email')
    if params.get('password', None) is not None :
      user.password = params.get('password')
    if params.get('mobile', None) is not None :
      user.mobile = params.get('mobile')
    user.save()

    # We convert once again
    data = {"email" : user.email, "id" : user.id}

    # We send the information to the browser
    return jsonify({'data': data}), 201
  except Exception as error:
    return jsonify({'error': 'Not found {error}'.format(error=error) }), 404

# Delete user
@app_user.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  try:
    user       = User.get(User.id == id)
    is_deleted = user.delete_instance()

    return str(is_deleted)
  except Exception as error:
    return jsonify({'error': 'Not found {error}'.format(error=error) }), 404

# Get all users
@app_user.route('/users', methods=['GET'])
def get_all_users():
  return jsonify({'data': list(User.select().dicts()) }), 201
