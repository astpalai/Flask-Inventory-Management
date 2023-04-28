from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from website import db
from website.models import User
from website.forms import RegisterForm

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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data,
                     password = generate_password_hash(form.password.data, method='scrypt'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created successfully.', category='success')
        
        return redirect(url_for('views.home'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(*err_msg, category='danger')
    
    return render_template('register.html', form=form)