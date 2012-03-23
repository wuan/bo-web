import blitzortung
import datetime
import pytz

import numpy as np

from flask import current_app

import trackerweb.lib.tracker

class CachedPlot(blitzortung.plot.Plot):

  def __init__(self):
    super(CachedPlot, self).__init__(self)
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
  def plot(self, *args):
    tracker_activity = trackerweb.lib.tracker.Activity()
    
    axes = self.figure.add_subplot(111, xlabel='minute', ylabel='# of measured local events')

    activity = np.array(tracker_activity.get())
    width = 1.0
    left = np.arange(-len(activity)+width/2, width/2, width)
  
    axes.bar(left, activity, width=width)

class RawData(CachedPlot):
  def fetch_data(self):
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=pytz.UTC)
    delta = datetime.timedelta(minutes=5)
    fileNames = blitzortung.files.Raw("/var/cache/blitzortung/raw")
    timeInterval = blitzortung.data.TimeRange(now, delta)
    data = blitzortung.files.Data(fileNames, timeInterval)
    lines = data.get(True)
    time = []
    x = []
    y = []
    for line in lines:
      if line and line[0] != '#':
	fields = line.split(' ')
	time.append(float(fields[2])/1000.0)
	x.append(float(fields[3]))
	y.append(float(fields[4]))
      else:
	time.append(float('nan'))
	x.append(float('nan'))
	y.append(float('nan'))
    self.time = np.array(time)
    self.x = np.array(x)
    self.y = np.array(y)

class Waveform(RawData):
  def plot(self, *args):
    self.fetch_data()

    axes = self.figure.add_subplot(111, xlabel='time [us]')
    axes.plot(self.time, self.x)
    axes.plot(self.time, self.y)

class XY(RawData):
  def plot(self, *args):
    self.fetch_data()

    axes = self.figure.add_subplot(111)
    axes.plot(self.x, self.y)

