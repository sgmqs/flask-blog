# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:26:22
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user 	=	{'nickname':'sgmqs'}
	posts=[
		{
			'author':{'nickname':'Jack'},
			'body':'Beautiful day in protland!'
		},
		{
			'author':{'nickname':'zhan san'},
			'body':'The avergers movie was so cool!'
		}
	]
	return render_template('index.html',
		title='Home',
		user=user,
		posts=posts)
