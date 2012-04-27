import time
import blitzortung
import socket
import json
import datetime
import pytz

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
    print start, length
    return start + " " + length
