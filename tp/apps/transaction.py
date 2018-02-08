from flask import Blueprint, jsonify, request, session
from helpers import login_helper
from models import Transaction, Token, User
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime

app_transaction = Blueprint('app_post', __name__)

def logged_checker(tokenString):
  try:
    token = Token.get(Token.string == tokenString)
    if (token.createdAt + datetime.timedelta(seconds=3600)) > datetime.datetime.now():
      return token
    else:
      token.delete_instance()
      return False
  except Exception as error:
    return False

def user_checker(Token, Transaction):
  if Token.user == Transaction.user:
    return True
  else:
    return False  

# Create transaction
@app_transaction.route('/transactions', methods=['POST'])
def create_transaction():
  params = request.get_json() # dict
  token  = params.get('token')
  if logged_checker(token) is False:
    return jsonify({'error':'Not connected or token expired'})
  else:
    userToken   = logged_checker(token)
    params      = request.get_json() # dict
    amount      = params.get('amount')
    description = params.get('description')
    transaction = Transaction.create(amount=amount, description=description, user=userToken.user)
    transaction.save()

    # Convert our model (object) to dictionnary
    data = model_to_dict(transaction)
    # Jsonify work only with dict, we've to convert everything
    return jsonify({'data': data}), 201

# Get transaction
@app_transaction.route('/transaction/<id>', methods=['POST'])
def get_transaction(id):
  params = request.get_json() # dict
  token  = params.get('token')
  if logged_checker(token) is False:
    return jsonify({'error':'Not connected or token expired'})
  else:
    userToken = logged_checker(token)
    try:
      transaction = Transaction.get(Transaction.id == id)
      if user_checker(userToken, transaction) is False:
        return jsonify({'error': 'this user cant access this transaction'}), 403
      else:
        data = model_to_dict(transaction)
        return jsonify({'data': data}), 201
    except Exception as error:
      return jsonify({'error': 'Not found {error}'.format(error=error) }), 404

# Modify transaction
@app_transaction.route('/transaction/<id>', methods=['PUT'])
def put_transaction(id):
  params = request.get_json() # dict
  token  = params.get('token')
  if logged_checker(token) is False:
    return jsonify({'error':'Not connected or token expired'})
  else:
    userToken = logged_checker(token)
    try:
      transaction = Transaction.get(Transaction.id == id)
      if user_checker(userToken, transaction) is False:
        return jsonify({'error': 'this user cant access this transaction'}), 403
      else:
        if params.get('amount', None) is not None :
          transaction.amount = params.get('amount')
        if params.get('description', None) is not None :
          transaction.description = params.get('description')
        transaction.save()
      # We convert once again
      data = model_to_dict(transaction)
      # We send the information to the browser
      return jsonify({'data': data}), 201
    except Exception as error:
      return jsonify({'error': 'Not found {error}'.format(error=error) }), 404

# Delete transaction
@app_transaction.route('/transaction/<id>', methods=['DELETE'])
def delete_transaction(id):
  params = request.get_json() # dict
  token  = params.get('token')
  if logged_checker(token) is False:
    return jsonify({'error':'Not connected or token expired'})
  else:
    userToken = logged_checker(token)
    try:
      transaction = Transaction.get(Transaction.id == id)
      if user_checker(userToken, transaction) is False:
        return jsonify({'error': 'this user cant access this transaction'}), 403
      else:
        is_deleted = transaction.delete_instance()
        return str(is_deleted)
    except Exception as error:
      return jsonify({'error': 'Not found {error}'.format(error=error) }), 404

# Get all transactions
@app_transaction.route('/alltransactions', methods=['POST'])
def get_all_transactions():
  params = request.get_json() # dict
  token  = params.get('token')
  if logged_checker(token) is False:
    return jsonify({'error':'Not connected or token expired'})
  else:
    userToken = logged_checker(token)
    return jsonify({'data': list(Transaction.select().where(Transaction.user == userToken.user).dicts())}), 201
