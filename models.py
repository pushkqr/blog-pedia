from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, Column, ForeignKey
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(Text, unique=True)
    password = Column(Text, nullable=False)
    bio = Column(Text)
    join_date = Column(String(250), nullable=False)
    blog_posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='author')


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    subtitle = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    body = Column(Text, nullable=False)
    img_url = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship('User', back_populates='blog_posts')
    comments = relationship('Comment', back_populates='blog')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('PostTag', back_populates='post')


class Comment(db.Model):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blog_posts.id"))
    author = relationship('User', back_populates='comments')
    blog = relationship('BlogPost', back_populates='comments')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('BlogPost', back_populates='category')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('PostTag', back_populates='tag')


class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    post = db.relationship('BlogPost', back_populates='tags')
    tag = db.relationship('Tag', back_populates='posts')
