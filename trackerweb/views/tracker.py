
import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app

import trackerweb.lib.cache
import trackerweb.lib.tracker

tracker = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker.route('/')
def index():
  info = {}

  tracker_info = trackerweb.lib.tracker.Info()

  info['uptime'] = tracker_info.get('process/uptime')
  info['numberofevents'] = tracker_info.get('process/numberOfEvents')
  info['eventspersecond'] = tracker_info.get('process/eventsPerSecond')
  info['minutes'] = tracker_info.get('process/numberOfSeconds') / 60

  return render_template('tracker/index.html', info=info)

