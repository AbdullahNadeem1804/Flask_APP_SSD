import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect # For CSRF protection

# --- App Configuration ---
app = Flask(__name__)
# SECRET_KEY is crucial for sessions and CSRF protection
app.config['SECRET_KEY'] = 'a-very-secret-key'
# Set up the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Library Initialization ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app) # Initialize CSRF protection

# --- (TASK 5) Models: Secure Password Storage ---
# Stored the *hashed* password, not the plain text [cite: 188]
class User(db.Model): #Abdullah Nadeem , 22i-1597
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(100))
    message = db.Column(db.Text)

# --- (TASK 1) Forms: Secure Input Handling ---
# Using Flask-WTF automatically validates input [cite: 155]
# and prevents XSS by auto-escaping content in templates.
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Your Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Your Phone Number (optional)')
    website = StringField('Your Web Site (optional)')
    message = TextAreaField('Type your message here...', validators=[DataRequired()])
    submit = SubmitField('Submit')

# --- (TASK 4) Secure Error Handling ---
# Custom error pages prevent leaking sensitive info [cite: 177, 180]
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() # Ensure bad database sessions don't persist
    return render_template('500.html'), 500

# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # (TASK 5) Use the set_password method to hash
        #Abdullah Nadeem , 22i-1597
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) 
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # (TASK 2) Parameterized Queries
        # SQLAlchemy's ORM (filter_by) automatically creates
        # parameterized queries, preventing SQLi[cite: 163, 167].
        # This is NOT a raw query: "SELECT * FROM user WHERE username = '" + user_input + "'"
        user = User.query.filter_by(username=form.username.data).first()
        # Abdullah Nadeem i22-1597
        # (TASK 5) Use check_password to compare hashes
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id # Secure session management
            flash('Login successful!', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Login failed. Check username and password.', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # (TASK 3) Session check
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
        
    form = ContactForm()
    if form.validate_on_submit():
        # (TASK 1 & 2) Input is validated by the form 
        # and this ORM call is parameterized[cite: 161].
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            website=form.website.data,
            message=form.message.data
        )
        db.session.add(new_contact)
        db.session.commit()
        flash('Your contact details have been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True) # Keep debug=True for lab, turn off for production