from bottle import default_app, route, run, request
import pickle

DICT_FILE = 'dict.p'

dict = pickle.load(open(DICT_FILE, "rb"))

@route('/')
def root():
    return "server is alive. dict = {}".format(str(dict))
    
    
@route('/register/<secret>/<service>')
def register(secret, service):
    client_ip = request.environ.get('REMOTE_ADDR')
    if secret not in dict:
        dict[secret] = {}
    if service not in dict[secret]:
        dict[secret][service] = set([])
    dict[secret][service].add(client_ip)
    
    pickle.dump(dict, open(DICT_FILE, "wb"))
    
    return {'status': 'OK'}
    
    
@route('/resolve/<secret>/<service>')
def resolve(secret, service):
    client_ip = request.environ.get('REMOTE_ADDR')
    ips_set = dict.get(secret, {}).get(service, set([]))
    if client_ip in ips_set:
        return client_ip
    if len(ips_set) > 0:
        return list(ips_set)[0]
    return ''
    
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=80)
    