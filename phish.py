import dns.query
import dns.name
import dns.resolver

from urlparse import urlparse

import json
import time

json_data = open("sites.json").read()
data = json.loads(json_data)
#data = data[500:1000]
dns_list = [ {
				'url':x['url'], 
		  		'ip':x['details'][0]['ip_address'], 
		  		'dns':dns.name.from_text(urlparse(x['url']).netloc)
	  		} for x in data ] 


def ff_find(dns_list):
	ff = dns_list
	for name in ff:
		name['lookup'] = []
		try:
			a = dns.resolver.query(name['dns'], 'A')
			for i in range(0, len(a)):
				name['lookup'].append(str(a[i]))
		
		except dns.resolver.NXDOMAIN: 
			name['lookup'].append("NXDOMAIN")
		except dns.resolver.NoNameservers:
			name['lookup'].append("NoNameservers")
		except dns.resolver.NoAnswer:
			name['lookup'].append("NoAnswer")
		except dns.exception.Timeout:
			name['lookup'].append("Timeout")

	return ff

ff_initial = ff_find(dns_list)
time.sleep(300)
ff_stop = ff_find(dns_list)
print "\a"
ffs = []

for i in range(0, len(dns_list)):
	ffs.append({'url'   : dns_list[i]['url'], 
				'is_ff' : len(set(ff_initial[i]['lookup'])
				  .intersection(ff_stop[i]['lookup'])) != len(dns_list[i]['lookup'])
				})


for i in ffs:
	if i['is_ff']:
		print i