from bottle import default_app, route, run, request, get, view
import bottle
import random
import os
import time

bottle.TEMPLATE_PATH.insert(0, 'templates/')

MAX_IDLE_TIME = 10

table = {}


@route('/')
def root():
    return "table = {}".format(table)
    
    
@get('/register/<secret>/<service>')
def register(secret, service):
    global table
    client_ip = request.environ.get('REMOTE_ADDR')
    if secret not in table:
        table[secret] = {}
    if service not in table[secret]:
        table[secret][service] = dict()
    table[secret][service][client_ip] = {'last_time': time.time()}
    
    return {'status': 'OK'}

def clear_old(services):
    current_time = time.time()
    for s, hosts in list(services.items()):
        for host, data in list(hosts.items()):
            if current_time - data['last_time'] > MAX_IDLE_TIME: 
                del hosts[host]
        if not hosts:
            del services[s]
@route('/resolve/<secret>')
def resolve(secret):
    client_ip = request.environ.get('REMOTE_ADDR')
    services = table.get(secret, {})
    clear_old(services)
    return {'hosts': dict(( [service, random.choice(list(ips))] 
                           for service, ips
                           in services.items()))
            
           }
    

@view('monitor.tpl')
@route('/monitor/<secret>')
def monitor(secret):
    return table.get(secret, {})
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000)
    
