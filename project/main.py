from flask import render_template, redirect, request

from models.notes import Notes
from app import app, db

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/dairy")
def dairy():
	data = Notes.query.order_by(Notes.created.desc()).all()
	return render_template("notes.html", notes=data)

@app.route("/dairy/add-note", methods=["POST"])
def addDairyNote():
	note = Notes(title=request.form["title"], text=request.form["text"])
	db.session.add(note)
	db.session.commit()

	return redirect('/dairy', code=302)

if __name__ == '__main__':
	app.run(debug=True)