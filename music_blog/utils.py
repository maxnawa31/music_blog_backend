def jwt_identity(payload):
    from music_blog.user.models import User
    user = User.query.filter_by(email=payload).first()
    return user


def identity_loader(email):
    return email


import requests
import json
from oauthlib.oauth2 import WebApplicationClient
import os


def get_google_provider_cfg():
    return requests.get(os.environ.get('GOOGLE_DISCOVERY_URL')).json()


google_client = WebApplicationClient(os.environ.get('GOOGLE_CLIENT_ID'))
