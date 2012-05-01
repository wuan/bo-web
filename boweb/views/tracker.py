
import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app

import boweb

tracker = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker.route('/')
def index():
  info = {}

  tracker_info = boweb.lib.tracker.Info()

  info['uptime'] = tracker_info.get('process/uptime')
  info['numberofevents'] = tracker_info.get('process/numberOfEvents')
  info['eventspersecond'] = tracker_info.get('process/eventsPerSecond')
  info['minutes'] = tracker_info.get('process/numberOfSeconds') / 60

  info['firmware'] = tracker_info.get('hardware/firmware')
  info['baudrate'] = "%d/%d" %(tracker_info.get('hardware/comm/baudRate'), tracker_info.get('hardware/gps/baudRate'))
  info['version'] = tracker_info.get('software/version').replace('&nbsp;',' ')
  info['gps_hardware'] = tracker_info.get('hardware/gps/type')

  return render_template('tracker/index.html', info=info)

