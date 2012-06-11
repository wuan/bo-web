
import time
import blitzortung
import socket
import json
import datetime
import pytz
import logging

from flask import Response, Blueprint, render_template, abort, current_app

import boweb

tracker = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker.route('/')
def index():
  info = {}

  return render_template('tracker/index.html', info=info)

