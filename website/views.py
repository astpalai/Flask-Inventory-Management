from flask import Blueprint, render_template,request, flash, redirect, url_for
from flask_login import login_required, current_user

from website import db
from website.models import Products
from website.forms import AddProductForm

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/inventory')
@login_required
def inventory():
    if current_user.username != 'admin':
        flash('Access Denied', category = 'danger')
        return redirect(url_for('views.home'))
    
    add_form = AddProductForm()        
    products = Products.query.filter_by()
    return render_template('inventory.html', products = products, add_form = add_form)
