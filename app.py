from flask import *
import api


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "jfie3p3rjw"


## Blueprint
app.register_blueprint(api.api)


## Pages
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


@app.route("/booking")
def booking():
	return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(host="0.0.0.0", port=3000)