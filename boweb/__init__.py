import logging

import lib

from flask import Flask, render_template

logger = logging.getLogger('app')

app = Flask(__name__)

from boweb.views.tracker import tracker
from boweb.views.data import data

app.register_blueprint(tracker)
app.register_blueprint(data)

@app.route('/')
def index():
    return render_template('index.html')
