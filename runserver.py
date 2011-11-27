#!/usr/bin/env python

from werkzeug.contrib.cache import MemcachedCache
from trackerweb import app

app.config['cache'] = MemcachedCache(['127.0.0.1:11211'])

app.run(host='0.0.0.0', debug=True)
