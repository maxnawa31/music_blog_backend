import os

from flask import Flask
import datetime as dt
import music_blog.user.models
import music_blog.profile.models
import music_blog.articles.models
from music_blog import user, profile, articles
from music_blog.extensions import bcrypt, cache, db, migrate, cors, jwt
from flask_sqlalchemy import Model

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "it's a secret"
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:3000',
        'http://localhost:3000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'music_blog_dev'
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/music_blog_dev'
    CACHE_TYPE = 'simple'
    JWT_SECRET_KEY = 'super-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(days=7)
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    CORS_ORIGIN_WHITELIST = [
        'http://http://127.0.0.1:5000',
        'http://localhost:5000',
        'http://localhost:3000'
    ]


def create_app(config_object):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    migrate.init_app(app, db)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(articles.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(articles.views.blueprint)
    app.register_blueprint(profile.views.blueprint)