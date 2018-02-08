from models import User
def login_helper() :
    if session['logged_in'] is True :
        return True
    else:
        return False