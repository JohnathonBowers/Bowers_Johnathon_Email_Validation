from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def home():
    return redirect ('/users')

@app.route('/users')
def r_get_all_users():
    return render_template('show_users.html', users = User.get_all_users())

@app.route('/users/add')
def r_add_user():
    return render_template('add_user.html')

@app.route('/users/add_user', methods=['POST'])
def f_add_user():
    if not User.validate_user(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/users/add')
    User.add_user(request.form)
    # I learned to use session.pop from a post on intellipaat.com
    if session:
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
    return redirect ('/users')