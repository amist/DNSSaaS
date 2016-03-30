#encoding=utf8

from bottle import default_app, route, response
import time, random, urllib2, os

MAX_SLEEP_TIME = 10

@route('/v1/fortune/')
@route('/v1/fortune')

def fortuneGenerator():
    return {"result": os.popen("fortune", "r").readlines()}

application = default_app()

if __name__ == '__main__':
    application.run(debug=True, reload=True, host="0.0.0.0", port=9999)

