from flask import Flask, render_template

app = Flask(__name__)

from trackerweb.views.tracker import tracker
from trackerweb.views.data import data

app.register_blueprint(tracker)
app.register_blueprint(data)

@app.route('/')
def index():
  return render_template('index.html')

