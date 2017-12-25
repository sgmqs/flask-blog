#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-18 21:00:57
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length
from app.models import User

class PostForm(Form):
	"""docstring for PostForm"""
	post 	=	StringField('post',validators=[DataRequired()])
	
		

class LoginForm(Form):
	"""docstring for LoginForm"""
	openid	=	StringField('openid',validators=[DataRequired()])
	remember_me	=	BooleanField('remember_me',default=False)


class EditForm(Form):
	"""docstring for EditForm"""
	nickname	=	StringField('nickname',validators=[DataRequired()])
	about_me	=	TextAreaField('about_me',validators=[Length(min=0,max=140)])
	uid 		=	IntegerField('uid', validators=[DataRequired()])

	def __init__(self,original_nickname,*arg,**kwargs):
		Form.__init__(self,*arg,**kwargs)
		self.original_nickname	=	original_nickname

	def validate(self):
		if not Form.validate(self):
			return False
		if self.nickname.data==self.original_nickname:
			return True
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user !=None:
			self.nickname.errors.append('This nickname:{0} is already in database'.format(self.nickname.data))
			return False
		return True

		
