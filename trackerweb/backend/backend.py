import time
import blitzortung
import socket
import json
import datetime
import pytz
import subprocess

from flask import Response, Blueprint, render_template, abort, current_app, jsonify

import trackerweb.lib.cache
import trackerweb.lib.tracker

backend = Blueprint('backend', __name__, url_prefix='/backend')

@backend.route('/tracker/activity')
def get_tracker_activity():
    connection = trackerweb.lib.tracker.Connection('getActivity')
    return json.dumps(connection.get('activity'))

@backend.route('/tracker/raw/<start>')
@backend.route('/tracker/raw/<start>/<length>')
def get_tracker_raw(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--long-data', '--json'], stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output


def get_raw_files():
  cache = current_app.config['cache']
  cache_item = 'trackerweb_raw_files'

  raw_files = cache.get(cache_item)

  if not raw_files:
    raw_data_path='/var/cache/blitzortung/raw'
    raw_files = blitzortung.files.Raw(raw_data_path)
    cache.set(cache_item, raw_files, timeout=300)

  return raw_files
  
