# -*- coding: utf-8 -*-
# @Date    : 2017-12-17 21:26:22
# @Author  : org (928758777@qq.com)
# @Link    : ${link}
# @Version : $Id$

from app import app,db,lm,oid
from flask import render_template,flash,redirect,session,url_for,request,g
from flask.ext.login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,EditForm,PostForm
from .models import User,Post
from datetime import datetime
from config import POSTS_PER_PAGE,DATABASE_QUERY_TIMEOUT
from flask.ext.sqlalchemy import get_debug_queries
# from flask.ext.sqlalchemy import get_debug_queries


@app.route('/follow/<nickname>')
def follow(nickname):
	user = User.query.filter_by(nickname=nickname).firstI()
	if user is None:
		flash('User {0} not found'.format(nickname))
		return redirect(url_for('index'))
	if user==g.user:
		flash('You can\'t follow yourself!')
		return redirect(url_for('user',nickname=nickname))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow {0}'.format(nickname))
		return redirect(url_for('user',nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You are now following {0}'.format(nickname))
	return redirect(url_for('user',nickname=nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
	user = User.query.filter_by(nickname=nickname).firts()
	if user is None:
		flash('User {0} not found'.format(nickname))
		return redirect(url_for('index'))
	if user==g.user:
		flash('You can\'t unfollow yourself!')
		return redirect(url_for('user',nickname=nickname))

	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow {0}'.format(nickname))
		return redirect(url_for('user',nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following {0}'.format(nickname))
	return redirect(url_for('user',nickname=nickname))


@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
@app.route('/index/<int:page>',methods=['POST','GET'])
# @login_required
def index(page=1):
	#user 	=	{'nickname':'sgmqs'}
	form 	=	PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data,timestamp=datetime.utcnow(),user_id=session['id'])
		db.session.add(post)
		db.session.commit()
		flash('You post is now live!')
		return redirect(url_for('index'))

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
	#posts = User().followed_posts(session['id']).all()
	posts = User().followed_posts(session['id']).paginate(page,POSTS_PER_PAGE,False)
	print("posts:",posts)
	return render_template('index.html',
		title='Home',
		form=form,
		posts=posts,
		user = user
		)

@app.route('/login',methods=['POST','GET'])
# @oid.loginhandler
def login():
	# exit(1)
	print(session)

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
			session['id']	=	user.id
			return redirect(url_for('index'))
		else:
			# return oid.try_login(form.openid.data,ask_for=['nickname','email'])
			nickname =	User.make_unique_nickname(form.openid.data)
			user = User(nickname=nickname,email=nickname+'@sgmqsblog.com')
			db.session.add(user)
			db.session.commit()
			#make the user follw him/herself
			db.session.add(User.follow(user))
			db.session.commit()
			print("---ppp-------------",user.id)
			session['nickname'] = nickname
			session['id']	=	user.id
			return redirect(url_for('index'))

	return render_template('login.html',
		title='Sign In',
		form=form,
		providers=app.config['OPENID_PROVIDERS']
		)


@app.before_request
def before_request():
	pass
	g.user = current_user
	#print(dir(current_user.nickname))
	if session['_id'] is not None:
		# User.last_seen	=	datetime.utcnow()
		# User.nickname 	=	session['nickname']
		## sqlalchery session orm 配合commit使用   类库 session 做事务处理
		db.session.query(User).filter(User.nickname==session['nickname']).update({'last_seen':datetime.utcnow()})
		db.session.commit()
		
		## sqlalchery orm   类库
		# User.query.filter(User.nickname==session['nickname']).update({'last_seen':datetime.utcnow()})
		# db.session.add(User)

@app.after_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration>=DATABASE_QUERY_TIMEOUT:
			app.logger.warning("Slow Query:%s\nParameters:%s\nDuration:%fs\nConteext:%s\n" %(query.statement,query.parameters,query.duration,query.context))
	return response
		


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

# @oid.after_login
# def after_login(resp):

# 	if resp.email is None or resp.email =="":
# 		flash('Invalid login,Please try again')
# 		return redirect(url_for('login'))
# 	user =	User.query.filter_by(email=resp.email).first()
# 	if user is None:
# 		nickname = resp.nickname
# 		if nickname is None or nickname=="":
# 			nickname = resp.email.split('@')[0]
# 		user = User(nickname=nickname,email=resp.email)
# 		db.session.add(user)
# 		db.session.commit()
# 	remember_me = False
# 	if 'remember_me' in session:
# 		remember_me = session['remember_me']	
# 		session.pop('remember_me',None)


# 	nickname =	User.make_unique_nickname('ppppp')

# 	print("---user---dddd4444----------",nickname)

# 	user = User(nickname=nickname)

# 	db.session.add(user)
# 	intid = db.session.commit()
# 	print("---ppp-------------",intid)
# 	session['nickname'] = nickname
# 	login_user(user,remember=remember_me)
# 	return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
	# logout_user()
	session['nickname']=None
	return redirect(url_for('index'))

@app.route('/user/<nickname>/<int:page>')
@app.route('/user/<nickname>')
def user(nickname,page=1):
	# print(app.config['SQLALCHEMY_DATABASE_URL'])
	print(dir(g.user))
	user =	User.query.filter_by(nickname=nickname).first()
	if user==None:
		flash('User '+nickname+' not found')
		return redirect(url_for('index'))
	posts = [
		{'author':user,'body':'test post #1'},
		{'author':user,'body':'test post #2'}
	]

	print("posts:",user.posts)

	posts = user.posts

	return render_template('user.html',
		 posts = posts,
		 user = user
		)

@app.route('/edit',methods=['GET','POST'])
def edit():

	editform 	=	EditForm(session['nickname'])
	if editform.validate_on_submit():
		session['nickname']	=	editform.nickname.data
		uid =request.form.get("user_id")
		print("dd:",editform.about_me.data)
		#User.query.filter(User.id==uid).update({'about_me':'ddd'})
		# User.query.filter(User.id==uid).update({'about_me':datetime.utcnow()})
		# User.query.filter(User.nickname==session['nickname']).update({'about_me':datetime.utcnow()})
		#更新，添加 删除都要commit
		db.session.query(User).filter(User.id==uid).update({'nickname':editform.nickname.data,'about_me':editform.about_me.data})
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		user = User.query.filter_by(nickname=session['nickname']).first()
		editform.nickname.data = user.nickname
		editform.about_me.data = user.about_me
		return render_template('edit.html',form=editform)

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'),500

