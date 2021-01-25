import os
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, CreateUserForm

from flask_login import LoginManager, login_required, login_user, current_user
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "you should have a password in your config file")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///flask_login')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)


db = SQLAlchemy()
from models import connect_db, User
connect_db(app)

# instantiate and initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

# instantiate bcrypt
bcrypt = Bcrypt()

# connects flask-login users with database users
@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(user_id)
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
                raise
            
            # login_user(user)

            return redirect('/')
        except:
            print('Unable to create user.')
            return redirect('/')
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
            user = User.query.filter_by(username=form.username.data).first()
            is_authorized = bcrypt.check_password_hash(user.password, form.password.data)

            if not user and not is_authorized:
                raise

            login_user(user)

            flash('Logged in successfully.')
            return redirect('/admin')
        except:
            print('Invalid username/password')
            return redirect('/')
    print(form.errors)
    return render_template('login.html', form=form)

@app.route('/admin', methods=['GET'])
@login_required
def admin_page():
    return render_template('admin.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flask.flash('Logout successful.')
    return redirect('/')