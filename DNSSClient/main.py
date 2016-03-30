'''
DNSS client updates
'''
import time
import re
import os
import requests
import random
import json
DEFAULT_JSON = {"DNSS_Server": "http://10.149.208.98:8000/",
                "etc_hosts": '/etc/hosts',
                "sleep_time": 5,
                'secret': 'my_very_long_secret_stuff',
                'services': ["s1", "s2"],
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
    while 1:
      time.sleep(self.sleep_time)
      if counter == 0:
        for service in self.conf['services']:
          try:
            r = requests.get(self.server_url + '/register/{secret}/{service}'.format(
                                                     service=service, **self.conf))
          except Exception as e:
            print ("error registering... %s" % e)
            continue
        status = r.text
        print(status)
        if 'OK' not in status: continue
      counter = (counter + 1) % 50
      try:
        r = requests.get(self.server_url + '/resolve/%s' % self.secret)
      except Exception as e:
        print("error resolving hosts... %s"%e)
      stuff = r.text
      print("stuff =>", stuff)
      stuff = json.loads(stuff)
      print ("got stuff %s" % stuff)
      hosts = stuff['hosts']
      self.handle_hosts(hosts)

  def handle_hosts(self, hosts):
    new_etchosts = "\n".join("%s : %s" % (ip, host) 
                             for host, ip in sorted(hosts.items()))
    new_hosts = self.etc_hosts_template.format(new_hosts=new_etchosts)
    print(new_hosts)
    with open(self.etc_hosts, 'w') as f:
       f.write(new_hosts)
              
    
      

def main():
  conf = load_config()
  DNSSClient(conf).run()


if __name__ == '__main__':
  main()




