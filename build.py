from app import db
from models import User

db.drop_all()
db.create_all()

db.session.add(User(username="PracticeUser", password="Passwords1"))

db.session.commit()

print('DB flask_login created with sample user with an unencrypted password')