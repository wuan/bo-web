import json

from flask import Blueprint, render_template

import blitzortung
import boweb

SERVER = Blueprint('server', __name__, url_prefix='/server')


@SERVER.route('/')
def index():
    info = {}

    return render_template('server/index.html', info=info)


@SERVER.route('/info')
def get_server_status():
    info = boweb.lib.server.Info()
    return json.dumps(info.get_result())


@SERVER.route('/activity')
def get_server_activity():
    activity = boweb.lib.server.Activity()
    return json.dumps(activity.get_result())
