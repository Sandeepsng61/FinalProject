from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=128)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=16)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=64)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=64)])
    zipcode = StringField('ZIP Code', validators=[DataRequired(), Length(min=5, max=10)])
    country = SelectField('Country', choices=[
        ('IN', 'India'), 
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia')
    ], validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery')
    ], validators=[DataRequired()])
    submit = SubmitField('Proceed to Payment')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[Length(min=0, max=16)])  # min=0 allows empty for COD
    card_holder = StringField('Card Holder Name', validators=[Length(min=0, max=128)])  # min=0 allows empty for COD
    expiration_month = SelectField('Month', choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), 
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')])
    expiration_year = SelectField('Year', choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025'), 
                                                ('2026', '2026'), ('2027', '2027'), ('2028', '2028')])
    cvv = StringField('CVV', validators=[Length(min=0, max=4)])  # min=0 allows empty for COD
    submit = SubmitField('Complete Payment')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
