from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

from flask_bcrypt import Bcrypt


# instantiate bcrypt
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    """Define user"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
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
        return user
    
    # @classmethod
    # def authenticate(cls, username, password):
    #     """Find user with 'username' and 'password'.
        


def connect_db(app):
    """Connect this database to provided Flask App"""

    db.app = app
    db.init_app(app)