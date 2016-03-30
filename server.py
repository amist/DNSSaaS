from bottle import default_app, route, run, request
import pickle

DICT_FILE = 'dict.p'

dict = pickle.load(open(DICT_FILE, "rb"))

@route('/')
def root():
    return "server is alive. dict = {}".format(str(dict))
    
    
@route('/register/<domain>/<service>')
def register(domain, service):
    client_ip = request.environ.get('REMOTE_ADDR')
    if domain not in dict:
        dict[domain] = {}
    if service not in dict[domain]:
        dict[domain][service] = set([])
    dict[domain][service].add(client_ip)
    
    pickle.dump(dict, open(DICT_FILE, "wb"))
    
    return "registration from {}".format(client_ip)
    
    
@route('/<domain>/<service>')
def resolve(domain, service):
    return list(dict[domain][service])[0]
    
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=80)
    