import signal
import urllib

import psutil
import time
import sys
import json

from pip._vendor import requests

def cpu():
    return psutil.cpu_percent(interval=0.5)

def ram():
    return psutil.virtual_memory()[2]

def handler(sig_num,frame):
    kanalaHustu()
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on ''https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)



def kanalaSortutaAlaEz():
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': 'YJYOOFOU0YKE2ZI9'}

    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    edukia = json.loads(erantzuna.content)

    if(len(edukia)):
        emaitza = True
        kanalID = edukia[0]['id']
        kanalAPI = edukia[0]['api_keys'][0]['api_key']
    else:
        emaitza = False

    return emaitza,kanalID,kanalAPI

def kanalaSortu():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key':'YJYOOFOU0YKE2ZI9', 'name':'Kanala', 'field1': "%CPU",'field2': "%RAM"}

    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    edukia = json.loads(erantzuna.content)

    kanalID = edukia[0]['id']
    kanalAPI = edukia[0]['api_keys'][0]['api_key']

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

    return kanalID,kanalAPI


def datuIgoera(kanalAPI):
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key':kanalAPI, '%CPU':cpu(), '%RAM':ram()}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)


def kanalaHustu():

    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/"+kanalID+"/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': 'YJYOOFOU0YKE2ZI9'}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)



if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')

    emaitza,kanalID,kanalAPI = kanalaSortutaAlaEz()

    if(emaitza == False):
        kanalID,kanalAPI = kanalaSortu()

    while(True):
        datuIgoera(kanalAPI)
        time.sleep(15)






