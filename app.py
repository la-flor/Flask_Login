import os
from flask import Flask, request, flash, render_template, redirect
from forms import LoginForm
from flask_login import LoginManager, login_required

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')

        if not is_safe_url(next):
            return flask.abort(400)
        
        return flask.redirect(next or flask.url_for('index'))
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
    return redirect('/')