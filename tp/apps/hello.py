from flask import Blueprint, jsonify
from helpers.hello_helper import hello_helper
app_hello = Blueprint('app_hello', __name__)

@app_hello.route('/', methods=['GET', 'POST'])
def app():
    return 'hello'
