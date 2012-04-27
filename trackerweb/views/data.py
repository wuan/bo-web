
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
  cache_item = 'trackerweb_raw_files'

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

  data = subprocess.Popen(['blitzortung-data', '-i', data_file, '--mode=statistics'], stdout=subprocess.PIPE)
  (output, _) = data.communicate()
  results = output.strip().split(' ')
  return jsonify(total=int(results[0]), avg_amp=float(results[1]))

@data.route('/_get_histogram/<date>')
def get_histogram(date):
  date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
  data_file = get_raw_files().get(date)

  data = subprocess.Popen(['blitzortung-data', '-i', data_file, '--mode=histogram'], stdout=subprocess.PIPE)
  (output, _) = data.communicate()
  x=[]
  y=[]
  for line in output.splitlines():
    result = line.strip().split(' ')
    x.append(float(result[0]))
    y.append(int(result[1]))
  return jsonify(x=x, y=y)
