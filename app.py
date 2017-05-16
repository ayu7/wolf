from flask import Flask, render_template, url_for, request, redirect
#from utils import mathpix, math
import json

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/draw")
def draw():
    return render_template("draw.html")

@app.route("/type")
def type():
    return render_template("type.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/operations")
def operations():
    return render_template("operations.html")

# Turn off before release
if __name__ == "__main__":
    app.run( debug=True );
