import json

from flask import Blueprint, render_template

import blitzortung
import boweb


tracker = Blueprint('tracker', __name__, url_prefix='/tracker')


@tracker.route('/')
def index():
    info = {}

    return render_template('tracker/index.html', info=info)


@tracker.route('/info')
def get_tracker_status():
    info = boweb.lib.tracker.Info()
    return json.dumps(info.get_result())


@tracker.route('/activity')
def get_tracker_activity():
    activity = boweb.lib.tracker.Activity()
    return json.dumps(activity.get_result())
