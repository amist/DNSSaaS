'''
DNSS client updates
'''
import time
import re
import os
import requests
import random
import json
DEFAULT_JSON = {"DNSS_Server": "http://10.149.208.98/",
                "etc_hosts": '/etc/hosts',
                "sleep_time": 5,
                'secret': 'my_very_long_secret_stuff',
                'service': "s1",
               }

CONFIG_FILE = os.path.join(os.path.dirname(__file__), r'config.json')
def load_config():
  if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
      f.write(json.dumps(DEFAULT_JSON, indent=2))
  with open(CONFIG_FILE) as f:
    try:
      conf = json.load(f)
      return conf
    except Exception as e:
      print("Could not load config ", CONFIG_FILE)
    exit(1)

class DNSSClient(object):
  def __init__(self, conf):
    s = self.server_url = conf['DNSS_Server']
    if s[-1] == '/':
      self.server_url = s[:-1]
    self.etc_hosts = conf['etc_hosts']
    self.sleep_time = conf['sleep_time']
    self.secret = conf['secret']
    self.conf = conf
    with open(self.etc_hosts) as f: 
      backup = f.read()
    template = re.sub("#DSNSaaSection.*DSNSaaSectionEND",
                      '', backup, flags=re.DOTALL)
    self.etc_hosts_template = template+ """
#DSNSaaSection
{new_hosts}
#DSNSaaSectionEND
"""
    with open('hosts.backup', 'w') as f:
      f.write(backup)

  def run(self):
    counter = 0
    params = {'secret': self.secret}
    while 1:
      time.sleep(self.sleep_time)
      if counter == 0:
        r = requests.get(self.server_url + '/register/{secret}/{service}'.format(**self.conf))
        print(r.text)
        status = r.text
        if 'OK 'not in status: continue
      counter += 1
      r = requests.get(self.server_url + '/resolve/%s' % self.secret)
      stuff = r.json()
      hosts = stuff['hosts']
      self.handle_hosts(hosts, self.etc_hosts)

  def handle_hosts(self, hosts):
    new_etchosts = "\n".join("%s : %s" % (ip, host) 
                             for host, ip in sorted(hosts.items))
    with open(self.etchosts, 'w') as f:
       f.write(self.etc_hosts_template.format(hosts=new_etchosts))
              
    
      

def main():
  conf = load_config()
  DNSSClient(conf).run()


if __name__ == '__main__':
  main()




