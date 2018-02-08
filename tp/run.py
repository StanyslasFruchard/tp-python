from flask import Flask
from apps.hello import app_hello
from apps.user import app_user
from apps.transaction import app_transaction

app = Flask(__name__)
app.register_blueprint(app_hello)
app.register_blueprint(app_user)
app.register_blueprint(app_transaction)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
