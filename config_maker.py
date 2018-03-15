# Python 3

import requests
import json

text = """CONDOR_HOST = {host}
ALLOW_WRITE = 192.168.0.*
ALLOW_NEGOTIATOR = $(CONDOR_HOST)
ALLOW_NEGOTIATOR_SCHEDD = $(ALLOW_NEGOTIATOR)
HOSTALLOW_CONFIG = $(CONDOR_HOST)
CONDOR_ADMIN = medialab@$(CONDOR_HOST)
DISCARD_SESSION_KEYRING_ON_STARTUP=false
NEGOTIATOR_HOST = $(CONDOR_HOST)
#SLOT_TYPE_1 = cpus=2, ram=2048
#NUM_SLOTS_TYPE_1 = 1
"""

post_data = {
	'description': 'Condor Configuration File',
	'public': 'true',
	'files': {
		'condor_config.local': {
			'content': text
		}
	}
}
print(post_data)

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.post("https://api.github.com/gists", data=json.dumps(post_data), headers=headers)


print(r.status_code)
print(r.text)