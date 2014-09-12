import logging

import lib

from flask import Flask, render_template

logger = logging.getLogger('app')

app = Flask(__name__)

from boweb.views.tracker import TRACKER
from boweb.views.data import DATA
from boweb.views.server import SERVER

app.register_blueprint(TRACKER)
app.register_blueprint(DATA)
app.register_blueprint(SERVER)


@app.route('/')
def index():
    return render_template('index.html')
