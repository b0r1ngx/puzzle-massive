"""Api - Puzzle api

Usage: api run [--config <file>]
       api serve [--config <file>]
       api --help
       api --version

Options:
  -h --help         Show this screen.
  --config <file>   Set config file. [default: site.cfg]

Subcommands:
    run     - Start the web server in the foreground. Don't use for production.
    serve   - Starts a daemon web server with Gevent.
"""
from docopt import docopt
from setuptools_scm import get_version
#from ConfigParser import RawConfigParser

from app import make_app
from api.tools import loadConfig

api_version = get_version()

def main():
    ""
    args = docopt(__doc__, version=api_version)
    config_file = args['--config']
    # parse args and pass to run, server, etc.
    #site_config = RawConfigParser()
    #site_config.read('site.cfg')

    appconfig = loadConfig(config_file)
    cookie_secret = appconfig.get('SECURE_COOKIE_SECRET')

    if args['run']:
        run(config_file, cookie_secret=cookie_secret) # TODO: can't use app.run when using websockets

    if args['serve']:
        serve(config_file, cookie_secret=cookie_secret)

if __name__ == '__main__':
    main()

def run(config, cookie_secret):
    "Start the web server in the foreground. Don't use for production."
    app = make_app(config=config, cookie_secret=cookie_secret)

    app.run(
            host=app.config.get('HOSTAPI'),
            port=app.config.get('PORTAPI'),
            use_reloader=True,
            )

def serve(config, cookie_secret):
    from gevent import pywsgi
    #from geventwebsocket.handler import WebSocketHandler
    #from geventwebsocket import WebSocketServer, Resource

    app = make_app(config=config, cookie_secret=cookie_secret)

    host = app.config.get('HOSTAPI')
    port = app.config.get('PORTAPI'),

    print(u'serving on {host}:{port}'.format(**locals()))
    server = pywsgi.WSGIServer((host, port), app)

    server.serve_forever(stop_timeout=10)
