import os
from flask import Flask, flash, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, CreateUserForm

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "you should have a password in your config file")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///flask_login')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

from models import connect_db, User
connect_db(app)

# instantiate and initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# connects flask-login users with database users
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            user = User.create_user(form.username.data, form.password.data)

            if not user:
                raise AssertionError("Unable to insert user into database.")
            
            login_user(user)

            return redirect('/')
        except:
            flash('Unable to create user.')
            return redirect('/createuser')
    return render_template('create_user.html', form=form)


# GET request returns login page with login
# POST request authenticates user and redirects to admin page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin')
    form = LoginForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data

            user = User.is_valid(username=username, password=password)
            login_user(user)
            
            flash('Logged in successfully.')
            return redirect('/admin')
        except:
            flash('Invalid username/password')
            return redirect('/login')

    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful.')
    return redirect('/')