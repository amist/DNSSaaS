from bottle import default_app, route, run, request, get
import pickle, json
import random
import os

DICT_FILE = 'dict.p'
if not os.path.isfile(DICT_FILE):
    with open("dict.p", 'w') as f:
        f.write("{}")  
   
table = json.load(open(DICT_FILE, "r"))
print (table)
@route('/')
def root():
    return "server is alive. table = {}".format(table)
    
    
@get('/register/<secret>/<service>')
def register(secret, service):
    global table
    client_ip = request.environ.get('REMOTE_ADDR')
    if secret not in table:
        table[secret] = {}
    if service not in table[secret]:
        table[secret][service] = set()
    table[secret][service].add(client_ip)
    
    #json.dump(table, open(DICT_FILE, "w"))
    print ("COOL")
    return {'status': 'OK'}
    
    
@route('/resolve/<secret>')
def resolve(secret):
    client_ip = request.environ.get('REMOTE_ADDR')
    services = table.get(secret, {})
    
    return {'hosts': dict(( [service, random.choice(list(ips))] 
                           for service, ips
                           in services.items()))
            
           }
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000)
    
