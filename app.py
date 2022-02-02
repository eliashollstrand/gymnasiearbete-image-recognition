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
    files = os.listdir("detected_images")
    return jsonify(files)

@app.route("/get_images")
def get_images():
    filenames = os.listdir("detected_images")

    for f in filenames:
        shutil.copy("detected_images/" + f, "static")

    print(len(filenames))
    return jsonify(filenames)

if __name__ == "__main__":
    app.run()