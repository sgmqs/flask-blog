#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:23:53
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy 


app	=	Flask(__name__)
app.config.from_object('config')
db	=	SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view	=	'login'

oid = OpenID(app,os.path.join(basedir,'tmp'))

from app import views,models
