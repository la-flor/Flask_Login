from app import db
from flask_login import UserMixin

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    """Define user"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True)
    
    username = db.Column(db.Text,
                            unique=True,
                            nullable=False)

    password = db.Column(db.Text,
                            unique=True,
                            nullable=False)

    @classmethod
    def create_user(cls, username, password):
        """Create a new user.  Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()

        return user
    
    @classmethod
    def is_valid(cls, username, password):
        """Find user with 'username' and 'password'."""

        user = cls.query.filter_by(username=username).first()
        is_authorized = bcrypt.check_password_hash(user.password, password)
        if is_authorized:
            return user
        else:
            raise AssertionError("Unable to validate user info.")
        


def connect_db(app):
    """Connect this database to provided Flask App"""

    db.app = app
    db.init_app(app)