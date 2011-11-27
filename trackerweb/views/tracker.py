
import time
import blitzortung
import socket
import json
import datetime
import pytz

from flask import Response, Blueprint, render_template, abort, current_app

class Cache(object):

  def __init__(self):
    self.cache = current_app.config['cache']

  def get_item(self):
    item = self.cache.get(self.get_item_name())

    if item is None:
      item = self.generate_item()
      self.cache.set(self.get_item_name(), item, timeout=60)

    return item

class ActivityPlotCache(Cache):

  def get_item_name(self):
    return "trackerweb_plot_activity"

  def generate_item(self):
    return ActivityPlot().read()

class WaveformPlotCache(Cache):

  def get_item_name(self):
    return "trackerweb_plot_waveform"

  def generate_item(self):
    return WaveformPlot().read()

class XYPlotCache(Cache):

  def get_item_name(self):
    return "trackerweb_plot_xy"

  def generate_item(self):
    return XYPlot().read()

class TrackerIPC(object):
  def __init__(self, command, socket_file = '/tmp/.blitzortung-tracker'):
    cache = current_app.config['cache']
    cache_item = 'trackerweb_ipc_%s' % command

    self.json_object = cache.get(cache_item)

    if self.json_object is None:
      try:
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect("/tmp/.blitzortung-tracker")
	s.send(json.dumps({'cmd':command}))
	self.json_object = json.loads(s.recv(10240))
        cache.set(cache_item, self.json_object, timeout=60)
	s.close()
      except socket.error:
	pass

  def get(self, path):
    json_object = self.json_object

    if json_object is not None:
      for component in path.split('/'):
        if json_object.has_key(component):
	  json_object = json_object[component]
	else:
	  json_object = None
	  break
    return json_object

class TrackerActivity(TrackerIPC):
  def __init__(self, socket_file = '/tmp/.blitzortung-tracker'):
    TrackerIPC.__init__(self, 'getActivity', socket_file)

  def get(self):
    if self.json_object != None:
      if self.json_object.has_key('activity'):
	return self.json_object['activity']
    return []
      
class TrackerInfo(TrackerIPC):
  def __init__(self, socket_file = '/tmp/.blitzortung-tracker'):
    TrackerIPC.__init__(self, 'getInfo', socket_file)
    
class ActivityPlot(blitzortung.plot.Plot):
  def plot(self):
    tracker_activity = TrackerActivity()

    self.write('set xlabel "minute"')
    self.write('set ylabel "# of measured local events"')
    activity = tracker_activity.get()
    if len(activity) == 0:
      activity.append(0)
    left_pos = -len(activity) + 1
    self.write('set xr[%f:%f]' %(left_pos - 0.5, 0.5))
    self.write('set yr[0:]')
    self.write('plot "-" not w boxes lt 3 fs solid 0.5')

    for index, value in enumerate(activity):
      self.write('%d %d' %(-index, value))
    self.write('e')

class RawDataPlot(blitzortung.plot.Plot):
  def fetch_data(self):
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.UTC)
    delta = datetime.timedelta(minutes=5)
    fileNames = blitzortung.files.RawFiles("/var/cache/blitzortung/raw")
    timeInterval = blitzortung.data.TimeRange(now, delta)
    data = blitzortung.files.Data(fileNames, timeInterval)
    self.lines = data.get(True)

class WaveformPlot(RawDataPlot):
  def plot(self):
    self.fetch_data()

    self.write('set yr[-1:1]')
    self.write('set xlabel "time [us]')
    self.write('plot "-" u ($3/1000):4 ti "x" w l lt 2, "-" u ($3/1000):5 ti "y" w l lt 6')
    for line in self.lines:
      self.write(line)
    self.write('e')
    for line in self.lines:
      self.write(line)
    self.write('e')

class XYPlot(RawDataPlot):
  def plot(self):
    self.fetch_data()

    self.write('set xr[-1:1]')
    self.write('set yr[-1:1]')
    self.write('set size square')
    self.write('plot "-" u 4:5 not w l lt 3')
    for line in self.lines:
      self.write(line)
    self.write('e')
    for line in self.lines:
      self.write(line)
    self.write('e')

tracker = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker.route('/')
def index():
  info = {}

  tracker_info = TrackerInfo()

  info['uptime'] = tracker_info.get('process/uptime')
  info['numberofevents'] = tracker_info.get('process/numberOfEvents')
  info['eventspersecond'] = tracker_info.get('process/eventsPerSecond')

  return render_template('tracker/index.html', info=info)

@tracker.route('/graph/<type>')
def graph(type):
  plot = None

  if type == "activity":
    plot = ActivityPlotCache().get_item()
  elif type == "waveform":
    plot = WaveformPlotCache().get_item()
  elif type == "xy":
    plot = XYPlotCache().get_item()
  else:
    abort(404)

  if plot:
    return Response(plot, mimetype='image/png')

    
