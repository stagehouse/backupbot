#!/usr/bin/env python3
# coding: utf-8

import requests
import datetime
import zlib
import logging
import keyring
import json
import os.path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/Users/jsm/Public/Stagehouse/Flex/Backups/FlexBackup.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

auth_url = 'https://stagehouse.flexrentalsolutions.com/f5/api/auth'
auth_payload = {'username': 'jmusarra', 'password': '', 'source':'FLEX5_EXTJS_CLIENT_SOURCE'}
headers = {'Content-Type':'application/json'}
bytes_transferred = 0

def createDateString():
    date = datetime.date.today()
    dateString = date.strftime("%B-%d-%Y")
    return dateString

def makedc(size):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])

backupUrl = "https://stagehouse.flexrentalsolutions.com/backup?filename=stagehouse-backup-" \
             + createDateString()\
             + ".tar.gz"

# Old backup file - only 1.7MB, use for testing:
fakeBackupUrl = 'https://stagehouse.flexrentalsolutions.com/backup?filename=stagehouse-backup-July-01-2017.tar.gz'

logger.info(f'Beginning backup - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
#Login 
try:
    r_auth = requests.post(auth_url, data=json.dumps(auth_payload), headers=headers)
except Exception as e:
    print(e)

print("URL:" + r_auth.url)
print("Status Code: " + str(r_auth.status_code))
#print("Authentication Response: " + r_auth.text)
# COOKIE NONSENSE
#c = r_auth.cookies
#print(c)
#v = str(c.get('JSESSIONID'))
#print(v)
#cookies = dict(JSESSIONID=v)
#cookies = dict(JSESSIONID='siuhoiweoiweiwiejiowd')
#print(cookies)

if r_auth.status_code == 200:
    response = json.loads(r_auth.text)
    auth_token = response['token']
    headers = {'Host':'stagehouse.flexrentalsolutions.com',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate, br',
                'Cookie':'JSESSIONID=1i0fvn9h59gcqop2f3sn2zssp',
                'Connection':'keep-alive',
                'Upgrade-Insecure-Requests':'1'}
    print('Logged in as: ', response['user']['userName'])
    try:
        r_file = requests.get(url=backupUrl, headers=headers, stream=True)
    except Exception as e:
        print(e)
#print("FILE URL: " + r_file.url)
#if len(r_file.text) < 2048:
#    print("r_file body: " + r_file.text)
#print(r_file.headers)
#r_file.raise_for_status()
#print("FILE STATUS: " + str(r_file.status_code))


#data = r_file.iter_content()
saveName = f'/Users/jsm/Public/Stagehouse/Flex/Backups/Flex-backup-{createDateString()}.tar.gz'
with open(saveName,'wb') as outFile:
    for chunk in r_file.iter_content(chunk_size=32768):
        outFile.write(chunk)
        bytes_transferred += len(chunk)
        print("Downloaded {0} bytes".format(bytes_transferred), end='\r', flush=True)
#data = zlib.decompress(r_file.iter_content(), zlib.MAX_WBITS|32)
print(f'File size: {bytes_transferred} bytes.')
logger.info(f'File size: {bytes_transferred} bytes.')
if os.path.isfile(saveName):
    print(f'Backup file saved at {saveName}')
    logger.info(f'Backup file saved at {saveName}')




if __name__ == "__main__":
    logger.info('This part worked')
#    with open('/Users/jsm/Public/Stagehouse/Flex/Backups/Flex-backup-' + createDateString() + '.tar.gz','wb') as outFile:
#        outFile.write(data)
