#!/usr/bin/env python

import sys,os
import logging, logging.handlers

activate_this = os.path.join(sys.path[0], 'bo-web/bin/activate_this.py')
execfile(activate_this, dict(__file__ = activate_this))

filename="/tmp/trackerweb.log"
file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=10*1024*1024, backupCount=5,encoding='utf-8')

root_logger = logging.getLogger('')
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)

from werkzeug.contrib.cache import MemcachedCache
from flup.server.fcgi import WSGIServer
from trackerweb import app

app.config['cache'] = MemcachedCache(['127.0.0.1:11211'])

if __name__ == '__main__':
    root_logger.debug('starting application')
    WSGIServer(app).run()

root_logger.debug('exiting')
