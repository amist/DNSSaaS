from bottle import default_app, route, run, request, get
import requests

def get_fortune():
    return requests.get('http://fortune_generator/v1/fortune').text
    
    
def get_cow(text):
    return requests.post('http://cow_provider/v1/cow', data = "{'text': '%s'}" % text)
    

@route('/')
def main():
    return {'result': get_cow(get_fortune())}
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=9100)