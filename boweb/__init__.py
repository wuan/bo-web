import logging

import lib
import backend

from flask import Flask, render_template

all = ['lib', 'backend']

logger = logging.getLogger('app')

app = Flask(__name__)

from boweb.views.tracker import tracker
from boweb.views.data import data
from boweb.backend.backend import backend

app.register_blueprint(tracker)
app.register_blueprint(data)
app.register_blueprint(backend)

@app.route('/')
def index():
  return render_template('index.html')
