#!/usr/bin/env python

import os

if os.path.exists('bowebenv'):
    activate_this = 'bowebenv/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))

from boweb import app

try:
    from werkzeug.contrib.cache import MemcachedCache

    app.config['cache'] = MemcachedCache(['127.0.0.1:11211'])
except RuntimeError, ImportError:
    pass

app.run(host='0.0.0.0', debug=True)
