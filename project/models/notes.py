from app import db
from datetime import datetime

class Notes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	subtitle = db.Column(db.String(256))
	text = db.Column(db.String(), nullable=False)
	created = db.Column(db.DateTime, default=datetime.now())
