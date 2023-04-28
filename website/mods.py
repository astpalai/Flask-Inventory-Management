from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from website import db
from website.models import Products

mods = Blueprint('mods', __name__)

@mods.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        barcode = request.form.get('barcode')
        quantity = request.form.get('quantity')
        new_product = Products(product = product_name, price = price, barcode = barcode, quantity = quantity)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added!', category='success')

    return redirect(url_for('views.inventory'))

@mods.route('/delete/<int:id>')
def delete(id):
    product = Products.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted.', category='warning')

    return redirect(url_for('views.inventory'))
    