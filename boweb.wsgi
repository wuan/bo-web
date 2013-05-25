#!/usr/bin/env python

import sys
import os

sys.path.insert(0, '/var/www/boweb')

# uncomment these lines in order to use a virtualenv for the appllication
activate_this = os.path.join(sys.path[0], 'bowebenv/bin/activate_this.py')
execfile(activate_this, dict(__file__ = activate_this))

from boweb import app as application
from werkzeug.contrib.cache import MemcachedCache

application.config['cache'] = MemcachedCache(['127.0.0.1:11211'])
