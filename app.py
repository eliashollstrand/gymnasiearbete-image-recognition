import os
import shutil
from flask import Flask, render_template, jsonify


app = Flask(__name__)

filenames = []

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/data")
def data():
    files = os.listdir("application_data/detected_images")
    return jsonify(files)

@app.route("/get_images")
def get_images():
    filenames = os.listdir("application_data/detected_images")

    for f in filenames:
        shutil.copy("application_data/detected_images/" + f, "static")

    return jsonify(filenames)

if __name__ == "__main__":
    app.run()