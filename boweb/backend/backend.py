import time
import blitzortung
import socket
import json
import datetime
import pytz
import subprocess

from flask import Response, Blueprint, render_template, abort, current_app, jsonify

import boweb

backend = Blueprint('backend', __name__, url_prefix='/backend')

@backend.route('/tracker/info')
def get_tracker_status():
    connection = boweb.lib.tracker.Connection('getInfo')
    return json.dumps(connection.get_result())

@backend.route('/tracker/activity')
def get_tracker_activity():
    connection = boweb.lib.tracker.Connection('getActivity')
    return json.dumps(connection.get_result('activity'))

@backend.route('/data/raw/<start>')
@backend.route('/data/raw/<start>/<length>')
def get_data_raw(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--json'], stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output

@backend.route('/data/raw/time/<start>')
@backend.route('/data/raw/time/<start>/<end>')
def get_data_raw_time(start, end=""):
    starttime = int(start)
    now = datetime.datetime.utcnow()
    date = now.date()
    if starttime < 0:
        starttimestamp = now + datetime.timedelta(minutes=starttime)
        if now.date() != starttimestamp.date():
	    starttimestamp = datetime.datetime.combine(now.date(), datetime.time(0,0,0))
	start = starttimestamp.strftime("%H%M%S")
    data_file = get_raw_files().get(date)

    cache = current_app.config['cache']
    cache_item = 'boweb_raw_time_%s_%s' %(start, end)

    data = cache.get(cache_item)

    if not data:
	pipe = subprocess.Popen(['bo-data', '-i', data_file, '-s', start, '--json'], stdout=subprocess.PIPE)

	(data, _) = pipe.communicate()
	cache.set(cache_item, data, timeout=300)

    return data

@backend.route('/data/raw/long/<start>')
@backend.route('/data/raw/long/<start>/<length>')
def get_data_raw_long(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--long-data', '--json'], stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output

@backend.route('/data/raw/normalized/<start>')
@backend.route('/data/raw/normalized/<start>/<length>')
def get_data_raw_normalized(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--long-data', '--normalize', '--json'], stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output

def get_raw_files():
  cache = current_app.config['cache']
  cache_item = 'boweb_raw_files'

  raw_files = cache.get(cache_item)

  if not raw_files:
    raw_data_path='/var/cache/blitzortung/raw'
    raw_files = blitzortung.files.Raw(raw_data_path)
    cache.set(cache_item, raw_files, timeout=300)

  return raw_files
  
