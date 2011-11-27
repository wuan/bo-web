import blitzortung
import datetime
import pytz

from flask import current_app

import trackerweb.lib.tracker

class CachedPlot(blitzortung.plot.Plot):

  def __init__(self):
    blitzortung.plot.Plot.__init__(self)
    self.cache = current_app.config['cache']

  def get_item_name(self):
    return self.__class__.__module__.lower() + "." + self.__class__.__name__.lower() + "_plot"

  def read(self):
    item_name = self.get_item_name()
    data = self.cache.get(item_name)

    if data is None:
      self.create()
      data = self.output
      self.cache.set(item_name, data, timeout=60)

    return data

class Activity(CachedPlot):
  def plot(self):
    tracker_activity = trackerweb.lib.tracker.Activity()

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

class RawData(CachedPlot):
  def fetch_data(self):
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.UTC)
    delta = datetime.timedelta(minutes=5)
    fileNames = blitzortung.files.RawFiles("/var/cache/blitzortung/raw")
    timeInterval = blitzortung.data.TimeRange(now, delta)
    data = blitzortung.files.Data(fileNames, timeInterval)
    self.lines = data.get(True)

class Waveform(RawData):
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

class XY(RawData):
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

