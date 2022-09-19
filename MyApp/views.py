from time import sleep
from django.shortcuts import render
from ensurepip import version
from wsgiref import headers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
import json


# Create your views here.


def linkedin(request):
    url = 'https://www.linkedin.com/oauth/v2/authorization'    
    ad_data = {
                "response_type": "code",
                "client_id": "12345", #Not real client_id
                "redirect_uri": "http://127.0.0.1:8000/linkedin/editor/auth/",
                "status": "ACTIVE",
                "state": ":LinkClicksLinkedIn",
                "scope": "rw_ads"
                }

    accesscode = requests.get(url, params=ad_data)
    accesscodeurl = accesscode.url

    return HttpResponseRedirect(accesscodeurl)

def authcode(request):
    e = request.build_absolute_uri()
    z = 1
    a = 0
    for x in e:
        if x == '=':
            if a == 0:
                a = z
            else:
                b = z-7
        z += 1
    authcode = str(e[a:b])

    url_access_token = 'https://www.linkedin.com/oauth/v2/accessToken'

    payload = {
        'grant_type' : 'authorization_code',
        'code' : authcode,
        'client_id' : '12345', #Not real client_id
        'client_secret' : '12345', #Not real client_secret
        'redirect_uri' : 'http://127.0.0.1:8000/linkedin/editor/auth/',
    }

    response = requests.post(url=url_access_token, params=payload)
    response_json = response.json()
    # Extract the access_token from the response_json
    global access_token
    global expires_in
    access_token = response_json['access_token']
    expires_in = response_json['expires_in']
    template = loader.get_template('linkedin.html')
    return HttpResponse(template.render({}, request))

def editor(request):
    ad_data = {
        "account": "urn:li:sponsoredAccount:509496546",
        "name": "CampaignGRoup",
        "runSchedule": {
            "end": 9876543210123,
            "start": 1662626049057
        },
        "status": "ACTIVE",
        "totalBudget": {
            "amount": "600.00",
            "currencyCode": "CAD"
        }
    }

    access = "Bearer " + access_token
    print(access)
    version_header = {
        'header': 'X-Restli-Protocol-Version: 2.0.0',
        'Linkedin-Version': '202207',
        "Authorization": str(access),
    }
    #Error if there is too little a time delay between generation of access token and the post request   
    sleep(7)
    r = requests.post('https://api.linkedin.com/rest/adCampaignGroups',
                      headers=version_header, json=ad_data)

    return HttpResponse(r)
