import logging

from flask import Flask, render_template

logger = logging.getLogger('app')

logger.debug('before start of flask app')

app = Flask(__name__)

from trackerweb.views.tracker import tracker
from trackerweb.views.data import data
from trackerweb.backend.backend import backend

logger.debug('app started, registering blueprints')

app.register_blueprint(tracker)
app.register_blueprint(data)
app.register_blueprint(backend)

logger.debug('app setup finished')

@app.route('/')
def index():
  logger.debug('render main index')
  return render_template('index.html')
