from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from funnyContacts.auth import login_required
from funnyContacts.db import get_db


bp = Blueprint('contacts', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
	db = get_db()

	contacts = None
	contactsASC = None
	contactsDESC = None

	contactsRecently = db.execute(
		'''
		SELECT c.id, create_date, user_id, name, surname, email, num
		FROM contact c JOIN user u ON c.user_id = u.id
		ORDER BY create_date DESC
		'''
	).fetchall()


# testando as posibilidades
	if(request.method == 'POST'):
		print('Houve um POST')		

		contactsASC = db.execute(
			'''
			SELECT c.id, create_date, user_id, name, surname, email, num
			FROM contact c JOIN user u ON c.user_id = u.id
			ORDER BY name ASC
			'''
		).fetchall()

		contactsDESC = db.execute(
			'''
			SELECT c.id, create_date, user_id, name, surname, email, num
			FROM contact c JOIN user u ON c.user_id = u.id
			ORDER BY name DESC
			'''
		).fetchall()

	contacts = contactsRecently
	return render_template('contact/index.html', contacts=contacts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if(request.method == 'POST'):
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		number = request.form['number']
		error = None

		if(not name):
			error = 'Name is required.'
		elif(not number):
			error = 'Number is required.'

		if(error is not None):
			flash(error)
		else:
			db = get_db()
			db.execute(
				'''INSERT INTO contact (name, surname, email, num, user_id)
				VALUES (?, ?, ?, ?, ?)''', (name, surname, email, number, g.user['id'])
			)
			db.commit()

			return redirect(url_for('contacts.index'))

	return render_template('contact/create.html')


# Função para obter apenas um contato pelo ID
def get_contact(id, check_user=True):
	contact = get_db().execute(
		'''SELECT c.id, create_date, user_id, name, surname, email, num
		FROM contact c JOIN user u ON c.user_id = u.id
		WHERE c.id = ?''', (id,)
	).fetchone()

	if(contact is None):
		abort(404, "Contact id {0} doesn't exist." .format(id))

	if(check_user and contact['user_id'] != g.user['id']):
		abort(403)

	return contact

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
	contact = get_contact(id)

	if(request.method == 'POST'):
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		number = request.form['number']
		error = None

		if(not name):
			error = 'Name is required.'
		elif(not number):
			error = 'Number is required.'

		if(error is not None):
			flash(error)
		else:
			db = get_db()
			db.execute(
				'''UPDATE contact SET name = ?, surname = ?, email = ?, num = ?
				WHERE id = ?''', (name, surname, email, number, id)
			)
			db.commit()

			return redirect(url_for('contacts.index'))

	return render_template('contact/update.html', contact=contact)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
	get_contact(id) #<<< dúvida, para quê isso ?
	db = get_db()
	db.execute('DELETE FROM contact WHERE id = ?', (id,))
	db.commit()

	return redirect(url_for('contacts.index'))
	
