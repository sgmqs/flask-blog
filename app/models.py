#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-18 22:05:06
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import db
from hashlib import md5
class User(db.Model):
	"""docstring for User"""
	id 	=	db.Column(db.Integer,primary_key=True)
	nickname = db.Column(db.String(64),index=True,unique=True)
	email	=	db.Column(db.String(120),index=True,unique=True)
	posts	=	db.relationship('Post',backref='author',lazy='dynamic')
	about_me	=	db.Column(db.String(140))
	last_seen =	db.Column(db.DateTime)

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


		