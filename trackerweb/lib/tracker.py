import socket
import json
import datetime
import pytz

from flask import current_app

class Connection(object):
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

class Activity(Connection):
  def __init__(self, socket_file = '/tmp/.blitzortung-tracker'):
    Connection.__init__(self, 'getActivity', socket_file)

  def get(self):
    if self.json_object != None:
      if self.json_object.has_key('activity'):
	return self.json_object['activity']
    return []
      
class Info(Connection):
  def __init__(self, socket_file = '/tmp/.blitzortung-tracker'):
    Connection.__init__(self, 'getInfo', socket_file)
    
