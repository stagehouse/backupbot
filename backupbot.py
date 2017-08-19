#!/usr/bin/env python3
# coding: utf-8

import requests
import datetime
import zlib
import logging
import keyring

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/Users/jsm/Public/Stagehouse/Flex/Backups/FlexBackup.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

authUrl = "https://stagehouse.flexrentalsolutions.com/rest/core/authenticate"
authPayload = {'username':'backupbot', 'password':keyring.get_password('Flex', 'backupbot')}


def createDateString():
	date = datetime.date.today()
	dateString = date.strftime("%B-%d-%Y")
	return dateString

backupUrl = "https://stagehouse.flexrentalsolutions.com/backup?filename=stagehouse-backup-" \
             + createDateString()\
             + ".tar.gz"

#Login 
try:
	r_auth = requests.post(authUrl, data=authPayload)
except Exception as e:
	print(e)

print("URL:" + r_auth.url)
print("Status Code: " + str(r_auth.status_code))
print("Authentication Response: " + r_auth.text)
c = r_auth.cookies
print(c)
v = str(c.get('JSESSIONID'))
print(v)
cookies = dict(JSESSIONID=v)
#cookies = dict(JSESSIONID='siuhoiweoiweiwiejiowd')
print(cookies)

if r_auth.status_code == 200:
	try:
		r_file = requests.get(url=backupUrl, cookies=cookies)
	except Exception as e:
		print(e)
print("FILE URL: " + r_file.url)
r_file.raise_for_status()
print("FILE STATUS: " + str(r_file.status_code))


data = zlib.decompress(r_file.content, zlib.MAX_WBITS|32)


if __name__ == "__main__":
	logger.info('This part worked')
	with open('/Users/jsm/Public/Stagehouse/Flex/Backups/Flex-backup-' + createDateString() + '.tar','wb') as outFile:
		outFile.write(data)
