from flask import Flask
from flask import render_template
from flask import request
import map_creator
from flask import url_for, redirect

app = Flask(__name__)


@app.route('/created_map', methods=["POST"])
def form():
    """

    :return:
    """

    name = request.form['name']
    js = map_creator.get_json_data(name)
    map_creator.create_map(js)
    return redirect(url_for("static", filename="map.html"))


@app.route('/')
def start():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
