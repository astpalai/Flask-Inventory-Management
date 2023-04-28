from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from website import db
from website.models import User
from website.forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash('Username doesn\' exist', category='warning')
        elif user and check_password_hash(user.password, form.password.data) == False:
             flash('Incorrect Password', category='warning')
        else:
            login_user(user)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out!", category='info')
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