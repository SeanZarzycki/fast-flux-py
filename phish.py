import dns.query
import dns.name
import dns.resolver
import urllib.parse

from urllib.parse import urlparse

import json

json_data = open("sites.json").read()
data = json.loads(json_data)
data = data[:500]
dns_list = [  {'url':x['url'], 
			  'ip':x['details'][0]['ip_address'], 
			  'dns':dns.name.from_text(urlparse(x['url']).netloc)} for x in data ] 


def ff_find(dns_list):
	fluxes = []
	for name in dns_list:
		try:
			a = dns.resolver.query(name[2], 'A')
			name.append(str(a[0]))
		
		except dns.resolver.NXDOMAIN: 
			name.append("")
		except dns.resolver.NoNameservers:
			name.append("")
		except dns.resolver.NoAnswer:
			name.append("")
			
	return fluxes

ff = ff_find(dns_list)
