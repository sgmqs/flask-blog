# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:26:22
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import app,db,lm,oid
from flask import render_template,flash,redirect,session,url_for,request,g
from flask.ext.login import login_user,logout_user,current_user,login_required
from .forms import LoginForm
from .models import User
from datetime import datetime


@app.route('/')
@app.route('/index')
# @login_required
def index():
	#user 	=	{'nickname':'sgmqs'}

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

@app.route('/login',methods=['POST','GET'])
# @oid.loginhandler
def login():
	# exit(1)

	# for x in g:
	# 	pass
	# 	print(x.__sizeof__)
	# print("ddd",(g.user))
	# print('ttt',g.user.is_authenticated)
	# if g.user.is_authenticated:
		# return redirect(url_for('index'))

	form 	=	LoginForm()
	if form.validate_on_submit():
		session['remember_me']=form.remember_me.data
		# flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		# return redirect('/index')
		user =	User.query.filter_by(nickname=form.openid.data).first()
		if user is not None:
			session['nickname']=user.nickname 
			return redirect(url_for('index'))
		else:
			return oid.try_login(form.openid.data,ask_for=['nickname','email'])

	return render_template('login.html',
		title='Sign In',
		form=form,
		providers=app.config['OPENID_PROVIDERS']
		)


@app.before_request
def before_request():
	 # g.user = current_user
	if session['nickname'] is not None:
		# User.last_seen	=	datetime.utcnow()
		# User.nickname 	=	session['nickname']
		## sqlalchery session orm 配合commit使用   类库 session 做事务处理
		#db.session.query(User).filter(User.nickname==session['nickname']).update({'last_seen':datetime.utcnow()})
		#db.session.commit()
		# User.update().where(User.nickname==session['nickname']).values(last_seen=datetime.utcnow())
		## sqlalchery orm   类库
		User.query.filter(User.nickname==session['nickname']).update({'last_seen':datetime.utcnow()})
		# db.session.add(User)
		


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@oid.after_login
def after_login(resp):

	if resp.email is None or resp.email =="":
		flash('Invalid login,Please try again')
		return redirect(url_for('login'))
	user =	User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname=="":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname,email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']	
		session.pop('remember_me',None)
	login_user(user,remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
	# logout_user()
	session['nickname']=None
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
def user(nickname):
	# print(app.config['SQLALCHEMY_DATABASE_URL'])
	user =	User.query.filter_by(nickname=nickname).first()
	if user==None:
		flash('User '+nickname+' not found')
		return redirect(url_for('index'))
	posts = [
		{'author':user,'body':'test post #1'},
		{'author':user,'body':'test post #2'}
	]
	return render_template('user.html',
		 posts = posts,
		 user = user
		)