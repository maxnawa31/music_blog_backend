import datetime
import requests
import os
import json
from music_blog.exceptions import InvalidUsage
from music_blog.profile.models import UserProfile
from sqlalchemy.exc import IntegrityError
from .serializers import user_schema
from music_blog.extensions import db
from flask import Blueprint, request, jsonify, redirect, url_for, make_response

from flask_apispec import use_kwargs, marshal_with
from .models import User
from flask_jwt_extended import current_user, jwt_optional, create_access_token, jwt_refresh_token_required, create_refresh_token, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, decode_token, jwt_required, get_raw_jwt
from music_blog.utils import get_google_provider_cfg
from music_blog.utils import google_client

blueprint = Blueprint('user', __name__)

@blueprint.route('/api/users', methods=["POST"])
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    try:
        userprofile = UserProfile(
            User(username, email, password=password, **kwargs).save()).save()
        return userprofile.user
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'message': 'User already registered',
            'status_code': 422
        })

@blueprint.route('/api/users/signup', methods=["GET"])
def signup_user():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'])
    return redirect(request_uri)

@blueprint.route('/api/users/login', methods=["POST"])
@jwt_optional
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user_jwt = create_access_token(identity=user.email, fresh=True)
        user.token = user_jwt
        return user
    else:
        return jsonify({
            'message': 'Something went wrong',
            'status_code': 422
        })

@blueprint.route('/api/user/logout', methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']


@blueprint.route('/api/user/<int:user_id>', methods=["GET"])
@jwt_required
@marshal_with(user_schema)
def get_user(user_id):
    user = User.query.get(user_id)
    return user


@blueprint.route('/api/user/<int:user_id>', methods=["PATCH"])
@jwt_required
@use_kwargs(user_schema)
@marshal_with(user_schema)
def users_update(**kwargs):
    user_id = kwargs.get('user_id')
    user = User.query.get(user_id)
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user