
import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app, jsonify

import trackerweb.lib.cache
import trackerweb.lib.plot

data = Blueprint('data', __name__, url_prefix='/data')

@data.route('/')
def index():
  activity = {}

  raw_data_path='/var/cache/blitzortung/raw'
  raw_files = blitzortung.files.Raw(raw_data_path)
  date_strings = []
  for date in raw_files.get_dates():
    activity[date.strftime('%Y-%m-%d')] = 0
  return render_template('data/index.html', activity=activity)

@data.route('/_get_dates')
def get_dates():
  config = blitzortung.Config()
  raw_data_path='/var/cache/blitzortung/raw'
  raw_files = blitzortung.files.Raw(raw_data_path)
  date_strings = []
  for date in raw_files.get_dates():
    date_strings.append(date.strftime('%Y-%m-%d'))
  return jsonify(result=date_strings, path=raw_data_path)
