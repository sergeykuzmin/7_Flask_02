from email.policy import default

from app import db
from datetime import datetime
import secrets

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	email = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(64), nullable=False)
	token = db.Column(db.String(128), nullable=True)
	created = db.Column(db.DateTime, default=datetime.now())

	def check_password(self, password):
		if password == self.password:
			return True

		return False

	def generate_token(self):
		self.token = secrets.token_hex(16)
		return self.token