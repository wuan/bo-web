
import time
import blitzortung
import socket
import json
import datetime
import pytz
import subprocess

from flask import Response, Blueprint, render_template, abort, current_app, jsonify

data = Blueprint('data', __name__, url_prefix='/data')

def get_raw_files():
  cache = current_app.config['cache']
  cache_item = 'boweb_raw_files'

  raw_files = cache.get(cache_item)

  if not raw_files:
    raw_data_path='/var/cache/blitzortung/raw'
    raw_files = blitzortung.files.Raw(raw_data_path)
    cache.set(cache_item, raw_files, timeout=300)

  return raw_files
  
@data.route('/')
def index():
  return render_template('data/index.html')

@data.route('/_get_date')
def get_dates():
  date_strings = []
  for date in get_raw_files().get_dates():
    date_strings.append(date.strftime('%Y-%m-%d'))
  date_strings.reverse()
  return jsonify(result=date_strings)

@data.route('/_get_date/<date>')
def get_date(date):
  date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
  data_file = get_raw_files().get(date)

  data = subprocess.Popen(['bo-data', '-i', data_file, '--mode=statistics'], stdout=subprocess.PIPE)
  (output, _) = data.communicate()
  results = output.strip().split(' ')
  return jsonify(total=int(results[0]), avg_amp=float(results[1]))

@data.route('/_get_histogram/<date>')
def get_histogram(date):
  date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
  data_file = get_raw_files().get(date)

  data = subprocess.Popen(['bo-data', '-i', data_file, '--mode=histogram'], stdout=subprocess.PIPE)
  (output, _) = data.communicate()
  x=[]
  y=[]
  for line in output.splitlines():
    result = line.strip().split(' ')
    x.append(float(result[0]))
    y.append(int(result[1]))
  return jsonify(x=x, y=y)

@data.route('/data/raw/<start>')
@data.route('/data/raw/<start>/<length>')
def get_data_raw(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--json'],
                            stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output


@data.route('/data/raw/time/<start>')
@data.route('/data/raw/time/<start>/<end>')
def get_data_raw_time(start, end=""):
    start_time = int(start)
    now = datetime.datetime.utcnow()
    date = now.date()
    if start_time < 0:
        start_timestamp = now + datetime.timedelta(minutes=start_time)
        if now.date() != start_timestamp.date():
            start_timestamp = datetime.datetime.combine(now.date(), datetime.time(0, 0, 0))
        start = start_timestamp.strftime("%H%M%S")
    data_file = get_raw_files().get(date)

    cache = current_app.config['cache']
    cache_item = 'boweb_raw_time_%s_%s' % (start, end)

    data = cache.get(cache_item)
    if not data:
        pipe = subprocess.Popen(['bo-data', '-i', data_file, '-s', start, '--json'], stdout=subprocess.PIPE)
        data, _ = pipe.communicate()
        cache.set(cache_item, data, timeout=300)

    return data


@data.route('/data/raw/long/<start>')
@data.route('/data/raw/long/<start>/<length>')
def get_data_raw_long(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(['bo-data', '-i', data_file, '--start', start, '--number', length, '--long-data', '--json'],
                            stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output


@data.route('/data/raw/normalized/<start>')
@data.route('/data/raw/normalized/<start>/<length>')
def get_data_raw_normalized(start, length="-1"):
    date = datetime.datetime.utcnow().date()
    data_file = get_raw_files().get(date)

    data = subprocess.Popen(
        ['bo-data', '-i', data_file, '--start', start, '--number', length, '--long-data', '--normalize', '--json'],
        stdout=subprocess.PIPE)
    (output, _) = data.communicate()
    return output


def get_raw_files():
    cache = current_app.config['cache']
    cache_item = 'boweb_raw_files'

    raw_files = cache.get(cache_item)

    if not raw_files:
        raw_data_path = '/var/cache/blitzortung/raw'
        raw_files = blitzortung.files.Raw(raw_data_path)
        cache.set(cache_item, raw_files, timeout=300)

    return raw_files
