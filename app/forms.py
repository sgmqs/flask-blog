#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-18 21:00:57
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from flask.ext.wtf import Form

from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired
class LoginForm(Form):
	"""docstring for LoginForm"""
	openid	=	StringField('openid',validators=[DataRequired()])
	remember_me	=	BooleanField('remember_me',default=False)
