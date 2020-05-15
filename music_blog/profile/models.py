from flask_jwt_extended import current_user
from music_blog.extensions import db

followers_assoc = db.Table("followers_assoc",
                           db.Column("follower", db.Integer,
                                     db.ForeignKey("userprofile.user_id")),
                           db.Column("followed_by", db.Integer, db.ForeignKey("userprofile.user_id")))


class UserProfile(db.Model):
    __tablename__ = 'userprofile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship(
        'User', backref=db.backref('profile', uselist=False))
    follows = db.relationship('UserProfile', secondary=followers_assoc, primaryjoin=id == followers_assoc.c.follower,
                              secondaryjoin=id == followers_assoc.c.followed_by,
                              backref='followed_by', lazy='dynamic')

    def __init__(self, user, **kwargs):
        db.Model.__init__(self, user=user, **kwargs)

    def is_following(self, profile):
        return bool(self.follows.filter(followers_assoc.c.follwed_by == profile.id).count())

    def follow(self, profile):
        if self is not profile and not self.is_following(profile):
            self.follows.append(profile)
            return True
        return False

    def unfollow(self, profile):
        if self is not profile and self.is_following(profile):
            self.follows.remove(profile)
            return True
        return False

    @property
    def following(self):
        if current_user:
            return current_user.profile.is_following(self)
        return False

    @property
    def username(self):
        return self.user.username

    @property
    def bio(self):
        return self.user.bio

    @property
    def image(self):
        return self.user.image

    @property
    def email(self):
        return self.user.email
