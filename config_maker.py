# Python 3

import requests
import json

CENTRAL_MANAGER_ADDRESS = "192.168.0.101" # the ip address of the central manger
HOST_NETWORK = "*" # the IP address network - * can be used, but is possibly insecure. Comma separated list of IP addresses.

text = """CONDOR_HOST = {host}
ALLOW_WRITE = {host_network}
ALLOW_NEGOTIATOR = $(CONDOR_HOST)
ALLOW_NEGOTIATOR_SCHEDD = $(ALLOW_NEGOTIATOR)
HOSTALLOW_CONFIG = $(CONDOR_HOST)
CONDOR_ADMIN = medialab@$(CONDOR_HOST)
DISCARD_SESSION_KEYRING_ON_STARTUP=false
NEGOTIATOR_HOST = $(CONDOR_HOST)
#SLOT_TYPE_1 = cpus=2, ram=2048
#NUM_SLOTS_TYPE_1 = 1
""".format(host = CENTRAL_MANAGER_ADDRESS, host_network = HOST_NETWORK)

post_data = {
	'description': 'Condor Configuration File',
	'public': 'true',
	'files': {
		'condor_config.local': {
			'content': text
		}
	}
}

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.post("https://api.github.com/gists", data=json.dumps(post_data), headers=headers)

j = json.loads(r.text)

print("Please use this URL in the Dockerfile: " + j['files']['condor_config.local']['raw_url'])