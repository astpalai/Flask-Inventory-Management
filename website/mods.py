from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from website import db
from website.models import Products
from website.forms import AddProductForm, EditProductForm

mods = Blueprint('mods', __name__)

@mods.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    add_form = AddProductForm()
    if add_form.validate_on_submit():
        product = Products(product_name = add_form.product_name.data,
                           price = add_form.price.data, barcode = add_form.barcode.data, quantity = add_form.quantity.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', category='success')
    if add_form.errors != {}: #If there are not errors from the validations
        for err_msg in add_form.errors.values():
            flash(*err_msg, category='danger')
    return redirect(url_for('views.inventory'))

@mods.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    product = Products.query.filter_by(id=id).first()
    edit_form = EditProductForm()
    if edit_form.validate_on_submit():
        product.product_name = edit_form.product_name.data
        product.price = edit_form.price.data
        #product.barcode = edit_form.barcode.data
        product.quantity = edit_form.quantity.data
        #db.session.update(product)
        db.session.commit()
        flash('Product edited successfully.', category='success')
    if edit_form.errors != {}: #If there are not errors from the validations
        for err_msg in edit_form.errors.values():
            flash(*err_msg, category='danger')
    return redirect(url_for('views.inventory'))

@mods.route('/delete/<int:id>')
@login_required
def delete(id):
    product = Products.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted.', category='warning')

    return redirect(url_for('views.inventory'))
    