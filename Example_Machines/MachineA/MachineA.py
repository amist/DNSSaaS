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
import time, random, urllib2, json

MAX_SLEEP_TIME = 10

@route('/MachineA/<flag>')
@route('/MachineA/<flag>/')
def LetterA(flag):
    letter = chr(random.randint(65,90))
    if flag.lower() == 'd':
        req = urllib2.Request('http://localhost:8777/MachineB/%s' % letter)
    else:
        req = urllib2.Request('http://machineb:8777/MachineB/%s' % letter)
    response = urllib2.urlopen(req)
    data = json.load(response)
    return {"result": data['result']}
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
    application.run(debug=True, reload=True, host="0.0.0.0", port=888)

