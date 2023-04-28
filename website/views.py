from flask import Blueprint, render_template,request, flash, redirect, url_for
from flask_login import login_required, current_user

from website import db
from website.models import Products

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/inventory', methods = ['GET', 'POST'])
@login_required
def inventory():
    if current_user.username != 'admin':
        flash('Access Denied', category = 'danger')
        return redirect(url_for('views.home'))
        
    products = Products.query.filter_by()
    return render_template('inventory.html', products = products)

@views.route('/delete/<int:id>')
def delete(id):
    product = Products.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted.', category='warning')

    products = Products.query.filter_by()
    return redirect(url_for('views.inventory'))
