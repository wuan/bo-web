import json
import datetime
from blitzortung.db.query import TimeInterval

from flask import Blueprint, render_template

import blitzortung.db
import pytz
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


@SERVER.route('/data/strikes')
def get_strikes_data():
    strike_db = blitzortung.db.strike()
    strike_db.set_srid(3857)

    interval_duration = datetime.timedelta(minutes=10)

    current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

    strikes = strike_db.select(TimeInterval(current_time - datetime.timedelta(minutes=60)))

    features = [
        {
            'type': 'Feature',
            'geometry': {"type": "Point", "coordinates": [strike.get_x(), strike.get_y()]},
            'properties': {'timedelta': int(
                (current_time - strike.get_timestamp()).total_seconds() / interval_duration.total_seconds())}
        } for strike in strikes]

    result = {
        'type': 'FeatureCollection',
        'features': features
    }
    return json.dumps(result)


@SERVER.route('/data/clusters')
def get_clusters_data():
    cluster_db = blitzortung.db.strike_cluster()
    cluster_db.set_srid(3857)

    last_cluster_time = cluster_db.get_latest_time()

    current_time = datetime.datetime.utcnow().replace(
        second=0,
        microsecond=0,
        tzinfo=pytz.UTC
    )

    if current_time - last_cluster_time == datetime.timedelta(minutes=1):
        current_time = last_cluster_time

    interval_duration = datetime.timedelta(minutes=10)
    clusters = cluster_db.select(current_time, interval_duration, 6, interval_duration)

    features = [
        {
            'type': 'Feature',
            'geometry': mapping(cluster.get_shape()),
            'properties': {'timedelta': int(
                (current_time - cluster.get_timestamp()).total_seconds() / interval_duration.total_seconds())}
        } for cluster in clusters]

    result = {
        'type': 'FeatureCollection',
        'features': features
    }
    return json.dumps(result)


@SERVER.route('/activity')
def get_server_activity():
    activity = boweb.lib.server.Activity()
    return json.dumps(activity.get_result())
