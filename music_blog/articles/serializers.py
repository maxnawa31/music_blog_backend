from marshmallow import Schema, fields, pre_load, post_dump
from music_blog.profile.serializers import ProfileSchema
from flask_jwt_extended import current_user

class TagSchema(Schema):
    tagname = fields.Str()


class ArticleSchema(Schema):
    id = fields.Str()
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    body = fields.Str()
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
    youtube_id = fields.Str()
    tag_list = fields.List(fields.Str())
    favoritesCount = fields.Int(dump_only=True)
    favorited = fields.Method('is_article_favorited')

    def is_article_favorited(self, obj):
        if current_user:
            is_favorited = obj.is_favourite(current_user.profile)
            return is_favorited
        else:
            return None

    @pre_load
    def make_article(self, data, **kwargs):
        return data['article']

    @post_dump
    def dump_article(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return {'article': data}

    class Meta:
        strict = True


class ArticleSchemas(ArticleSchema):

    @post_dump
    def dump_article(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many, **kwargs):
        return {'articles': data, 'articlesCount': len(data)}


class CommentSchema(Schema):
    created_at = fields.DateTime()
    body = fields.Str()
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    id = fields.Int()

    # for the envelope
    comment = fields.Nested('self', exclude=('comment',), default=True, load_only=True)

    @pre_load
    def make_comment(self, data, **kwargs):
        return data['comment']

    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return {'comment': data}

    class Meta:
        strict = True


class CommentsSchema(CommentSchema):

    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def make_comment(self, data, many, **kwargs):
        return {'comments': data}


article_schema = ArticleSchema()
articles_schema = ArticleSchemas(many=True)
comment_schema = CommentSchema()
comments_schema = CommentsSchema(many=True)