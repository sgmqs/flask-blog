#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-18 22:05:06
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import db
from hashlib import md5

followers	=	db.Table('followers',
		db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
		db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
	)

class User(db.Model):
	"""docstring for User"""
	id 	=	db.Column(db.Integer,primary_key=True)
	nickname = db.Column(db.String(64),index=True,unique=True)
	email	=	db.Column(db.String(120),index=True,unique=True)
	posts	=	db.relationship('Post',backref='author',lazy='dynamic')
	about_me	=	db.Column(db.String(140))
	last_seen =	db.Column(db.DateTime)
	role 	=	db.Column(db.Integer)
	# followed = db.relationship('User',
	# 		secondary = followers,
	# 		primaryjoin= (followers.c.follower_id==id),
	# 		secondaryjoin = (followers.c.followed_id==id),
	# 		backref=db.backref('followers',lazy='dynamic'),
	# 		lazy='dynamic'
	# 	)
	followed = db.relationship('User',
		secondary = followers,
		primaryjoin = (followers.c.follower_id == id),
		secondaryjoin = (followers.c.followed_id == id),
		backref = db.backref('followers', lazy = 'dynamic'),
		lazy = 'dynamic')
	#被关注者提交的文章 follower_id--关注者id  followed_id--被 关注者id
	def followed_posts(self,uid):
		return Post.query.join(followers,(followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==uid).order_by(Post.timestamp.desc())

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, uid):
		return self.followed.filter(followers.c.followed_id == uid).count() > 0

	@property
	def is_authenticated(self):
		return False

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id) #python2 
		except NameError:
			return str(self.id) #python3

	#py 3 坑md5时对原字符串进行编码设置
	def avatar(self,size):
		return 'http://www.gravatar.com/avatar/'+ md5(self.email.encode('utf8')).hexdigest() +'?d=mm&s='+str(size)		

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first()==None:
			return nickname
		version 	=	2
		while True:
			new_nickname	= nickname+str(version)
			if User.query.filter_by(nickname=nickname).first()==None:
				break
			version 	+=	1
				
		return new_nickname



	def __repr__(self):
		return "<User %r>" %(self.nickname)


class Post(db.Model):
	"""docstring for Post"""
	id 	=	db.Column(db.Integer,primary_key=True)
	body	=	db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id	=	db.Column(db.Integer,db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)


		