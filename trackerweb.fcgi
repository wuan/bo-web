#!/usr/bin/env python

activate_this = 'bo-web/bin/activate_this.py'
execfile(activate_this, dict(__file__ = activate_this))

from flup.server.fcgi import WSGIServer
from trackerweb import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/trackerweb-fcgi.sock').run()
