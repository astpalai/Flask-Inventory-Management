from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from website.models import User, Products

class LoginForm(FlaskForm):        
    username = StringField(label = 'Username', validators=[DataRequired()])
    password = PasswordField(label = 'Password', validators=[DataRequired()])
    submit = SubmitField(label = 'Log in')

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
        
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists!')

    username = StringField(label = 'Username', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label = 'Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label = 'Password', validators=[Length(min=1), DataRequired()]) # FOR SPEED I HAVE PASSWORD LENGTH TO 1
    password_confirm = PasswordField(label = 'Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label = 'Create Account')

class AddProductForm(FlaskForm):
    def validate_barcode(self, barcode_to_check):
        barcode = Products.query.filter_by(barcode = barcode_to_check.data).first()
        if barcode:
            raise ValidationError('Barcode already exists!')

    product_name = StringField(label = 'Product Name', validators=[DataRequired()])
    price = StringField(label = 'Price', validators=[DataRequired()])
    barcode = StringField(label = 'Barcode', validators=[DataRequired(), Length(min=6, max=6)])
    quantity = StringField(label = 'Quantity', validators=[DataRequired()])
    submit = SubmitField(label = 'Add product')

class EditProductForm(FlaskForm):
    product_name = StringField(label = 'Product Name', validators=[DataRequired()])
    price = StringField(label = 'Price', validators=[DataRequired()])
    barcode = HiddenField()
    quantity = StringField(label = 'Quantity', validators=[DataRequired()])
    submit = SubmitField(label = 'Add product')
