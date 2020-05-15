from flask import Blueprint
from flask_apispec import marshal_with
from music_blog.user.models import User
from flask_jwt_extended import current_user, jwt_required, jwt_optional


from .serializers import profile_schema
blueprint = Blueprint('profiles', __name__)


@blueprint.route('/api/profiles/<username>', methods=["GET"])
@jwt_optional
@marshal_with(profile_schema)
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=["POST"])
@jwt_required
@marshal_with(profile_schema)
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    current_user.profile.follow(user.profile)
    current_user.profile.save()
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=["DELETE"])
@jwt_required
@marshal_with(profile_schema)
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    current_user.profile.unfollow(user.profile)
    current_user.profile.save()
    return user.profile
