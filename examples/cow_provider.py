#encoding=utf8
'''
Created on Feb 25, 2016

@author: yglazner
​
Cow Provider Micro-Service

Get A cow ASCII that says what you want 
GET http://yglazner.pythonanywhere.com/v1/cow/hello mate!
 returns:
{"result": "a cow that says 'hello mate!'"}



'''

from bottle import default_app, post, response, request
import subprocess


@post('/v1/cow/')
@post('/v1/cow')
def cow():
    text = request.json['text']
    output = subprocess.check_output(["cowsay", text])
    print ("output")
    return {"result": output}

application = default_app()

if __name__ == '__main__':
    application.run(debug=True, reload=True, host="0.0.0.0", port=8777)

