from bottle import default_app, route, run, request

# dict = {'yoav': {'s1': set(['10.10.10.10']), 's2': set(['11.11.11.11'])}}
dict = {}

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
    return "registration from {}".format(client_ip)
    
    
@route('/<domain>/<service>')
def resolve(domain, service):
    return list(dict[domain][service])[0]
    
    
application = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=80)
    