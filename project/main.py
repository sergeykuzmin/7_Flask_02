from flask import Flask, render_template, redirect, json, request

app = Flask(__name__)

def saveNotes(data):
	with open('notes.json', "w", encoding = "UTF8") as file:
		json.dump(data, file)

def getNotes():
	data = {}

	try:
		with open('notes.json', "r+", encoding = "UTF8") as file:
			data = json.load(file)

	except FileNotFoundError:
		saveNotes(data)

	return data

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/dairy")
def dairy():
	data = getNotes()
	return render_template("notes.html", notes=dict(reversed(data.items())))

@app.route("/dairy/add-note", methods=["POST"])
def addDairyNote():
	title = request.form["title"]
	text = request.form["text"]
	data = getNotes()
	data[title] = text
	saveNotes(data)

	return redirect('/dairy', code=302)

if __name__ == '__main__':
	app.run(debug=True)