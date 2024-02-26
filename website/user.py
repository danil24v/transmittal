from flask_login import *
import base64
import random
from . import login_manager


class User(UserMixin):
    api_key = random.randint(11111, 99999)

    def __init__(self, rocket_ad):
        self.id = rocket_ad


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    def get_user_pass(creds_base64):
        decoded_creds = base64.b64decode(creds_base64)
        creds = decoded_creds.split(':')
        return creds[0], creds[1]

    creds_b64 = request.args.get('creds')
    if creds_b64:
        print('Request auth')
    else:
        creds_b64 = request.headers.get('Authorization')
        if creds_b64:
            print('Headers auth')
            creds_b64 = creds_b64.replace('Basic ', '', 1)

    if creds_b64:
        usr, pwd = get_user_pass(creds_b64)
        user = User(usr)
        if user:
            return user

    return None
