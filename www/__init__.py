from flask import Flask, render_template, request, flash, jsonify
import sys
from interfacing.classes.SimManager import SimManager

start = ['begin', 'start', 'lets go']

manager = SimManager()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/home/')
def homepage():
	return render_template('about.html')

@app.route('/about/')
def about():
	return render_template('about.html')


@app.route('/background_process')
def process():
	try:
		inp = request.args.get('input_data')
		response = manager.send(inp)
		if type(response) != str:
			response = "".join(response)
		response = _replace_newlines(response)
		return jsonify(result=response, rep_input=inp)

	except Exception as e:
		return str(e)


@app.route('/app', methods=['POST', 'GET'])
def action():
	response = []
	try:
		if request.method == "POST":
			data = request.form['data']
			response = manager.send(data)
			return render_template("app.html", response=response, inp=data)
		else:
			startup = manager.connect()
			print(startup)
			return render_template("app.html", response=startup)
	except Exception as e:
		print(e)
		flash(e)
		return render_template("app.html", error=e)

def _replace_newlines(inp):
	if isinstance(inp, str):
		inp = inp.replace("\n", "<br>")
	elif isinstance(inp,list):
		for s in inp:
			s = s.replace("\n","<br>")

	return inp



if __name__ == "__main__":
    app.run()
