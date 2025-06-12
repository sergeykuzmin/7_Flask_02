from datetime import timedelta, datetime

from flask import render_template, redirect, request, flash, session

from models.notes import Notes
from models.users import Users
from app import app, db

@app.route("/")
def index():
	if check_auth() == False:
		return redirect('/login', code=302)

	return render_template("index.html")

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		user = Users(username=request.form["username"], email=request.form["email"], password=request.form["password"])
		db.session.add(user)

		try:
			db.session.commit()
		except:
			flash("Registration failed")
			return render_template("register.html")

		flash("Registration success")
		return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		user = Users.query.filter_by(email=request.form["email"]).first()

		if user and user.check_password(request.form["password"]):
			token = user.generate_token()
			db.session.commit()
			expiration = datetime.now().timestamp() + 60*60*30
			session['expiration'] = expiration
			session['token'] = token
			return redirect('/', code=302)
		else:
			flash("Login failed")
			return render_template('login.html')

# @app.before_request
def check_auth():
	token = session.get("token")
	expiration = session.get("expiration")
	print(expiration)
	print(datetime.now().timestamp())

	if not token or datetime.now().timestamp() > expiration:
		return False
	return True

@app.route("/logout")
def logout():
	session.pop("token", None)
	session.pop("expiration", None)
	return redirect('/home', code=302)

@app.route("/dairy")
def dairy():
	if check_auth() == False:
		return redirect('/login', code=302)

	data = Notes.query.order_by(Notes.created.desc()).all()
	return render_template("notes.html", notes=data)

@app.route("/dairy/add-note", methods=["POST"])
def addDairyNote():
	if check_auth() == False:
		return redirect('/login', code=302)

	note = Notes(title=request.form["title"], text=request.form["text"])
	db.session.add(note)
	db.session.commit()

	return redirect('/dairy', code=302)

if __name__ == '__main__':
	app.run(debug=True)