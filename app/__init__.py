#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:23:53
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$


from flask import Flask

app	=	Flask(__name__)

from app import views
