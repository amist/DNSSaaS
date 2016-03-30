from bottle import default_app, route, run, request
import pickle

DICT_FILE = 'dict.p'
SECRETS_FILE = 'secrets.p'

dict = pickle.load(open(DICT_FILE, "rb"))
secrets = pickle.load(open(SECRETS_FILE, "rb"))

@route('/')
def root():
    return "server is alive. dict = {}, secrets = {}".format(str(dict), str(secrets))
    
    
@route('/register/<secret>/<domain>/<service>')
def register(secret, domain, service):
    client_ip = request.environ.get('REMOTE_ADDR')
    if domain not in dict:
        dict[domain] = {}
        secrets[domain] = secret
    if secrets[domain] == secret:
        if service not in dict[domain]:
            dict[domain][service] = set([])
        dict[domain][service].add(client_ip)
    
    pickle.dump(dict, open(DICT_FILE, "wb"))
    pickle.dump(secrets, open(SECRETS_FILE, "wb"))
    
    return "registration from {}".format(client_ip)
    
    
@route('/resolve/<domain>/<service>')
def resolve(domain, service):
    client_ip = request.environ.get('REMOTE_ADDR')
    ips_set = dict.get(domain, {}).get(service, set([]))
    if client_ip in ips_set:
        return client_ip
    if len(ips_set) > 0:
        return list(ips_set)[0]
    return ''
    
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=80)
    