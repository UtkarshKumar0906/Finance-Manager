from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import secrets
from flask_mysqldb import MySQL
from flask import flash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secret key

# Define the registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Define the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.htm')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get form data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        except Exception as e:
            flash('An error occurred during registration. Please try again later.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle form submission (e.g., authenticate user, set session variables)
        return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
    return render_template('login.html', form=form)

@app.route('/success')
def success_page():
    return 'Registration Successful!'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Raone@2011'
app.config['MYSQL_DB'] = 'finance_manager_db'

mysql = MySQL()
mysql.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
