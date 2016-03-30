#encoding=utf8
'''
Created on Feb 25, 2016

@author: yglazner
​
Sleeper Micro-Service

You can make you application sleep for 2 seconds like this:
GET http://yglazner.pythonanywhere.com/v1/sleeper/2
 returns:
{"result": "slept for 2.0 seconds"}​

Also supports random sleepiness!!!
http://yglazner.pythonanywhere.com/v1/sleeper/random​

 
This way you can outsource your application sleep time!!!


'''

from bottle import default_app, route, response
import time, random, urllib2

MAX_SLEEP_TIME = 10

@route('/MachineC/<letters>')
def LetterC(letters):
    letter = letters + chr(random.randint(65,90))
    return {"result": letter}
'''
@route('/v1/sleeper/random')
def sleep_random():

    sleeptime = random.randint(0, MAX_SLEEP_TIME-1) + random.random()
    #all good
    time.sleep(sleeptime)
    return {"result": "slept for %s seconds" % sleeptime}
'''
application = default_app()

if __name__ == '__main__':
    application.run(debug=True, reload=True, host="localhost", port=999)

