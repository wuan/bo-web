from flask import Flask, render_template

app = Flask(__name__)

from trackerweb.views.tracker import tracker

app.register_blueprint(tracker)

@app.route('/')
def index():
  return render_template('index.html')

