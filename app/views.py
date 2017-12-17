# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:26:22
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import app

@app.route('/')
@app.route('/index')
def index():
	user 	=	{'nickname':'sgmqs'}
	return ''' 
<html>
	<head>
		<title>Home Page</title>
	</head>
	<body>
		<h1>Hello ,'''+user['nickname']+'''</h1>

	</body>	
</html>	
'''
