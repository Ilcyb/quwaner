from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from datetime import datetime


like = db.Table('like',
                db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                db.Column('travel_id',db.Integer,db.ForeignKey('travel.id')))


user_tag = db.Table('user_tag',
                    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


travel_tag = db.Table('travel_tag',
                    db.Column('travel_id',db.Integer,db.ForeignKey('travel.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class Follow(db.Model):
    follower_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True) #粉丝
    followed_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True) #被关注的人
    timestamp = db.Column(db.DateTime,default=datetime.now)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Tag:{}>'.format(self.name)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(130))
    school = db.Column(db.String(40))
    province = db.Column(db.String(20))
    city = db.Column(db.String(40))
    register_time = db.Column(db.DateTime,default=datetime.now)
    avatar = db.Column(db.String(200))
    travels = db.relationship('Travel',backref='user',lazy='dynamic')
    followers = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                                backref=db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    likes = db.relationship('Travel',secondary=like,
                            backref=db.backref('likeusers',lazy='dynamic'))
    comments = db.relationship('Comment',backref='user',lazy='dynamic')
    tags = db.relationship('Tag',secondary='user_tag',
                            backref=db.backref('users',lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User:{}>'.format(self.username)
        
    
class Travel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    begin_time = db.Column(db.DateTime)
    travel_days = db.Column(db.Integer)
    avg_cost = db.Column(db.Float)
    destination = db.Column(db.String(40))
    body = db.Column(db.Text)
    background_img = db.Column(db.String(200))
    publish_time = db.Column(db.DateTime,default=datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comments = db.relationship('Comment',backref='travel',lazy='dynamic')
    tags = db.relationship('Tag',secondary='travel_tag',
                            backref=db.backref('travels',lazy='dynamic'))

    def __init__(self,title,begin_time,travel_days,avg_cost,
                destination,body,background_img,user_id):
        self.title = title
        self.begin_time = begin_time
        self.travel_days = travel_days
        self.avg_cost = avg_cost
        self.destination = destination
        self.body = body
        self.background_img = background_img
        self.user_id = user_id
            
    def __repr__(self):
        return '<Travel:{}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    travel_id = db.Column(db.Integer,db.ForeignKey('travel.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,user_id,travel_id,body):
        self.user_id = user_id
        self.travel_id = travel_id
        self.body = body

    def __repr__(self):
        return '<Comment:{}>'.format(self.body[:5] + '...')