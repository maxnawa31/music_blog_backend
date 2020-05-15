import datetime

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from marshmallow import fields
from .models import Article, Tags, Comment
from music_blog.user.models import User
from .serializers import article_schema, articles_schema, comment_schema, comments_schema

blueprint = Blueprint('articles', __name__)


@blueprint.route('/api/articles', methods=["GET"])
@jwt_optional
@use_kwargs(articles_schema)
@marshal_with(articles_schema)
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
    if author:
        res = res.join(
            Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    found_articles = res.offset(offset).limit(limit).all()
    return found_articles


@blueprint.route('/api/articles', methods=('POST', ))
@jwt_required
@use_kwargs(article_schema)
@marshal_with(article_schema)
def make_article(body, title, description, youtube_id, tag_list=None):
    article = Article(title=title,
                      description=description,
                      body=body,
                      author=current_user.profile,
                      youtube_id=youtube_id)
    if tag_list is not None:
        for tag in tag_list:
            mtag = Tags.query.filter_by(tagname=tag).first()
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            article.add_tag(mtag)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=["DELETE"])
@jwt_required
def delete_article(slug):
    article = Article.query.filter_by(slug=slug,
                                      author_id=current_user.id).first()
    article.delete()
    return jsonify({'message': 'Article Deleted', 'status_code': 200})


@blueprint.route('/api/articles/<slug>', methods=["GET"])
@jwt_optional
@marshal_with(article_schema)
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        return jsonify({'message': 'Article not found'})
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=["POST"])
@jwt_required
@marshal_with(article_schema)
def favorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    article.favourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=["DELETE"])
@jwt_required
@marshal_with(article_schema)
def unfavorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    article.unfavourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/feed', methods=["GET"])
@jwt_required
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def articles_feed(limit=20, offset=0):
    return Article.query.order_by(
        Article.created_at.desc()).offset(offset).limit(limit).all()


@blueprint.route('/api/tags', methods=["GET"])
def get_tags():
    return jsonify({'tags': [tag.tagname for tag in Tags.query.all()]})


@blueprint.route('/api/articles/<slug>/comments', methods=["GET"])
@marshal_with(comments_schema)
def get_comments(slug):
    article = Article.query.filter_by(slug=slug).first()
    return article.comments


@blueprint.route('/api/articles/<slug>/comments', methods=["POST"])
@jwt_required
@use_kwargs(comment_schema)
@marshal_with(comment_schema)
def make_comment_on_article(slug, body, **kwargs):
    article = Article.query.filter_by(slug=slug).first()
    comment = Comment(article, current_user.profile, body, **kwargs)
    comment.save()
    return comment


@blueprint.route('/api/articles/<slug>/comments/<cid>', methods=["DELETE"])
@jwt_required
def delete_comment_on_article(slug, cid):
    article = Article.query.filter_by(slug=slug).first()
    comment = article.comments.filter_by(id=cid,
                                         author=current_user.profile).first()
    comment.delete()
    return '', 200
