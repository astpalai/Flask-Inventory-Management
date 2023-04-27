from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from website import db
from website.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category = 'error')
        else:
            flash('Username does not exist.', category = 'error')

    return render_template('login.html')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')        
        password1 = request.form.get('password')
        password2 = request.form.get('password_confirm')

        # Validations
        user_mail = User.query.filter_by(email = email).first()
        user_name = User.query.filter_by(username = username).first()
        create_db = True
        if user_mail:
            flash('Email already exists.', category = 'danger')
            create_db = False
        if user_name:
            flash('Username already exists.', category = 'danger')
            create_db = False
        if len(username)<2:
            flash('Username must be longer than one character', category = 'danger')
            create_db = False
        if len(password1)<2:
            flash('Password must be longer than one character', category = 'danger')
            create_db = False
        if password1 != password2:
            flash('Passwords don\'t match.', category='danger')
            create_db = False
        if create_db == True:
            new_user = User(email = email, username = username, password = generate_password_hash(
                password1, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category = 'success')
            return redirect(url_for('views.home'))    

    return render_template('register.html')