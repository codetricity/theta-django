from django.shortcuts import render
import requests
from requests.auth import HTTPDigestAuth
import json
import os
import pprint
from django.http import HttpResponse


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


def generate_image_list():
    url = f"{THETA_URL}commands/execute"
    command_string = "camera.listFiles"
    payload = {
                "name": command_string,
                "parameters": {
                    "fileType": "image",
                    "entryCount": 20,
                    "maxThumbSize": 0

                }}
    resp = requests.post(
                        url,
                        json=payload,
                        auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))

    data = resp.json()
    imageEntries = data["results"]["entries"]
    images = []
    for imageEntry in imageEntries:
        print(imageEntry["fileUrl"])
        images.append(imageEntry["fileUrl"])
    return images


def image_urls(request):
    images = generate_image_list()

    return render(request, 'image_listing.html', {'image_list': images})


def getImage(url):
    imageName = url.split("/")[6]
    print("saving " + imageName + " to file")
    with open(f'{PROJECT_MEDIA_DIR}{imageName}', 'wb') as handle:
        response = requests.get(
                    url,
                    stream=True,
                    auth=(HTTPDigestAuth(THETA_ID, THETA_PASSWORD)))

        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


# def download_image(request):
#     test_url = "http://192.168.2.101/files/150100525831424d42079d18e0b6c300/100RICOH/R0010056.JPG"
#     getImage(test_url)
#     return HttpResponse('wrote file')


def download_all_images(request):
    print("start download tester")
    images = generate_image_list()
    for imageLocation in images:
        getImage(imageLocation)
    return HttpResponse(f'wrote {str(len(images))} files')
