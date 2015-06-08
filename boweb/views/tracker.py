import json

from flask import Blueprint, render_template

import boweb


TRACKER = Blueprint('tracker', __name__, url_prefix='/tracker')


@TRACKER.route('/')
def index():
    info = {}

    return render_template('tracker/index.html', info=info)


@TRACKER.route('/info')
def get_tracker_status():
    info = boweb.lib.tracker.Info()
    return json.dumps(info.get_result())

@TRACKER.route('/activity')
def get_tracker_activity():
    activity = boweb.lib.tracker.Activity()
    return json.dumps(activity.get_result())
