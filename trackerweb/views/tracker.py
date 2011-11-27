
import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app

import trackerweb.lib.cache
import trackerweb.lib.tracker
import trackerweb.lib.plot

tracker = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker.route('/')
def index():
  info = {}

  tracker_info = trackerweb.lib.tracker.Info()

  info['uptime'] = tracker_info.get('process/uptime')
  info['numberofevents'] = tracker_info.get('process/numberOfEvents')
  info['eventspersecond'] = tracker_info.get('process/eventsPerSecond')

  return render_template('tracker/index.html', info=info)

@tracker.route('/graph/<type>')
def graph(type):
  plot = None

  if type == "activity":
    plot = trackerweb.lib.plot.Activity().read()
  elif type == "waveform":
    plot = trackerweb.lib.plot.Waveform().read()
  elif type == "xy":
    plot = trackerweb.lib.plot.XY().read()
  else:
    abort(404)

  if plot:
    return Response(plot, mimetype='image/png')

