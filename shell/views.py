from django.shortcuts import render
import requests
from requests.auth import HTTPDigestAuth
import json
import os
import pprint


THETA_IP = '192.168.2.101'
PROJECT_MEDIA_DIR = os.getcwd() + "/media/"
# global constants specific to your THETA. Change for your camera.
THETA_ID = 'THETAYL00105377'
THETA_PASSWORD = '00105377'  # default password. may have been changed
THETA_URL = f'http://{THETA_IP}/osc/'


def homepage(request):
    return render(request, 'home.html')


def get(osc_command):
    url = THETA_URL + osc_command
    resp = requests.get(url, auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))
    pprint.pprint(resp.json())


def post(osc_command):
    url = THETA_URL + osc_command
    resp = requests.post(url,
                         auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))
    pprint.pprint(resp.json())


def state(request):
    url = f"{THETA_URL}state"
    resp = requests.post(url, auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))
    data = resp.json()
    print(data)
    return render(request, 'commandhome.html', {'data': data})


def info(request):
    url = f"{THETA_URL}info"
    # url = f"http://{THETA_IP}/osc/info"
    # URL below is for testing only
    # url = "https://httpbin.org/get"
    # r = requests.request('GET', url)
    resp = requests.get(url, auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))
    data = resp.json()
    print(data)
    return render(request, 'commandhome.html', {'data': data})


def take_picture(request):
    url = f"{THETA_URL}commands/execute"
    payload = {"name": "camera.takePicture"}
    resp = requests.post(
                        url,
                        json=payload,
                        auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))
                        
    data = resp.json()
    pprint.pprint(data)
    return render(request, 'commandhome.html', {'data': data})
