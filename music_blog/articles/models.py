import datetime
from slugify import slugify
from music_blog.profile.models import UserProfile
from music_blog.extensions import db

favoriter_assoc = db.Table(
    "favoritor_assoc",
    db.Column("favoriter", db.Integer, db.ForeignKey("userprofile.user_id")),
    db.Column("favorited_article", db.Integer, db.ForeignKey("article.id")))

tag_assoc = db.Table(
    "tag_assoc", db.Column("tag", db.Integer, db.ForeignKey("tags.id")),
    db.Column("article", db.Integer, db.ForeignKey("article.id")))


class Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(100))

    def __init__(self, tagname):
        db.Model.__init__(self, tagname=tagname)

    def __repr__(self):
        return self.tagname


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow)
    author_id = db.Column(db.ForeignKey('userprofile.user_id'), nullable=False)
    author = db.relationship('UserProfile', backref='comments')
    article_id = db.Column(db.ForeignKey('article.id'), nullable=False)

    def __init__(self, article, author, body, **kwargs):
        db.Model.__init__(self,
                          author=author,
                          body=body,
                          article=article,
                          **kwargs)


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    slug = db.Column(db.Text, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.ForeignKey('userprofile.user_id'), nullable=False)
    author = db.relationship('UserProfile', backref='articles')
    youtube_id = db.Column(db.Text,
                           nullable=False,
                           server_default='nZq_jeYsbTs')
    favoriters = db.relationship('UserProfile',
                                 secondary=favoriter_assoc,
                                 backref='favorites')
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.utcnow)
    tag_list = db.relationship('Tags', secondary=tag_assoc, backref='articles')

    comments = db.relationship('Comment',
                               backref=db.backref('article'),
                               lazy='dynamic')

    def __init__(self,
                 author,
                 title,
                 body,
                 description,
                 youtube_id,
                 slug=None,
                 **kwargs):
        db.Model.__init__(self,
                          author=author,
                          title=title,
                          description=description,
                          body=body,
                          youtube_id=youtube_id,
                          slug=slug or slugify(title),
                          **kwargs)

    def favourite(self, profile):
        if not self.is_favourite(profile):
            self.favoriters.append(profile)
            return True
        return False

    def unfavourite(self, profile):
        if self.is_favourite(profile):
            self.favoriters.remove(profile)
            return True
        return False

    def is_favourite(self, profile):
        return bool(
            self.query.filter(
                favoriter_assoc.c.favoriter == profile.user_id).filter(
                    favoriter_assoc.c.favorited_article == self.id).count())

    def add_tag(self, tag):
        if tag not in self.tag_list:
            self.tag_list.append(tag)
            return True
        return False

    def remove_tag(self, tag):
        if tag in self.tag_list:
            self.tag_list.remove(tag)
            return True
        return False

    @property
    def favoritesCount(self):
        return len(self.favoriters.all())
