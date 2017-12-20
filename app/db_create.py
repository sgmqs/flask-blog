#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-18 22:11:05
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URL
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO,'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URL,SQLALCHEMY_MIGRATE_REPO)
else:
	api.version_control(SQLALCHEMY_DATABASE_URL,SQLALCHEMY_MIGRATE_REPO,api.version(SQLALCHEMY_MIGRATE_REPO))	

