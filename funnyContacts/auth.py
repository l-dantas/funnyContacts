import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from funnyContacts.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	db = get_db()
	
	if(db.execute('SELECT id FROM user LIMIT 1').fetchone() is not None):
		flash('Already exist a user.')
		return redirect(url_for('auth.login'))

	if(request.method == 'POST'):
		password = request.form['password']
		error = None

		if(not password):
			error = 'Password is required.'
		elif(db.execute(
			'SELECT id FROM user WHERE password = ?', (password,)
		).fetchone() is not None):
			error = 'por enquanto nada!'

		if(error is None):
			db.execute(
				'INSERT INTO user (password) VALUES (?)', (generate_password_hash(password),)
			)
			db.commit()
		
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	db = get_db()
	
	if(db.execute('SELECT id FROM user LIMIT 1').fetchone() is None):
		return redirect(url_for('auth.register'))

	if(request.method == 'POST'):
		password = request.form['password']
		error = None
		user = db.execute(
			'SELECT * FROM user'
		).fetchone()

		if(not check_password_hash(user['password'], password)):
			error = 'Incorrect password.'

		if(error is None):
			session.clear()
			session['user_id'] = user['id']

			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')

@bp.route('/change-pass', methods=('GET', 'POST'))
def change_pass():

	if(request.method == 'POST'):
		old_pass = request.form['old_password']
		new_pass = request.form['new_password']
		error = None
		db = get_db()
		user = db.execute(
			'SELECT * FROM user'
		).fetchone()

		if(not check_password_hash(user['password'], old_pass)):
			error = 'Old password incorrect.'

		if(error is None):
			db.execute(
				'''
				UPDATE user SET password = ?
				WHERE id = ?
				''', (generate_password_hash(new_pass), user['id'])
			)
			db.commit()

			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/change-pass.html')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if(user_id is None):
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))

def login_required(view):
	@functools.wraps(view)
	
	def wrapped_view(**kwargs):
		if(g.user is None):
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view



