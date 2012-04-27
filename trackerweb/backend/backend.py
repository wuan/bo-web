import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app, jsonify

import trackerweb.lib.cache
import trackerweb.lib.plot

backend = Blueprint('backend', __name__, url_prefix='/backend')

@backend.route('/tracker/activity')
def get_tracker_activity():
    return json.dumps([1, 2, 3, 1, 5, 4, 6])
