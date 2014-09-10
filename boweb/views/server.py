import json
import datetime

from flask import Blueprint, render_template

import blitzortung.db
import boweb
from shapely.geometry import mapping

SERVER = Blueprint('server', __name__, url_prefix='/server')


@SERVER.route('/')
def index():
    info = {}

    return render_template('server/index.html', info=info)


@SERVER.route('/info')
def get_server_status():
    info = boweb.lib.server.Info()
    return json.dumps(info.get_result())


@SERVER.route('/data/current')
def get_current_data():
    cluster_db = blitzortung.db.strike_cluster()
    cluster_db.set_srid(3857)

    current_time = cluster_db.get_latest_time()

    interval_duration = datetime.timedelta(minutes=10)
    clusters = cluster_db.select(current_time, interval_duration, 6, interval_duration)

    features = [
        {
            'type': 'Feature',
            'geometry': mapping(cluster.get_shape()),
            'properties': {'timedelta': int((current_time - cluster.get_timestamp()).total_seconds() / interval_duration.total_seconds())}
        } for cluster in clusters]

    result = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features
    }
    return json.dumps(result)


@SERVER.route('/activity')
def get_server_activity():
    activity = boweb.lib.server.Activity()
    return json.dumps(activity.get_result())
