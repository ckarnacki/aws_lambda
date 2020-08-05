#!/usr/bin/env python
from botocore.vendored import requests
import json

# --- Variables ---
# UPDATE API KEYS FOR CURRENT ACCOUNT
PD_API_key = "irhJFYYbGb2xYTcXEE3P"
API_user = "ckarnacki@pagerduty.com"  # This will appear in the timeline as the user who ran the response play

P1_response_play = '15485624-c461-52f9-40ff-5b49ba63615f'
P2_response_play = '14fdd158-24f6-d04e-9b52-9b7df897b6b6'


# --- Helper functions ---
def runResponsePlay(play, incident, userName):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.pagerduty+json;version=2',
               'From': API_user, 'Authorization': 'Token token=' + PD_API_key}

    payload = buildResponsePlayPayload(incident)
    endpoint = 'https://api.pagerduty.com/response_plays/' + play + '/run'
    print(endpoint)

    resp = requests.post(endpoint, headers=headers, data=json.dumps(payload))

    json_resp = resp.json()


def buildResponsePlayPayload(incident):
    payload = {
        "incident": {
            "id": incident,
            "type": "incident_reference"
        }
    }
    return payload


# --- Core logic ---
def lambda_handler(event, context):
    # Only run response plays when incident is triggered
    if event['detail']['event'] == "incident.trigger":

        # Get incident ID
        inc_id = event['detail']['incident']['id']

        if event['detail']['incident']['priority']['summary'] == 'P1':
            runResponsePlay(P1_response_play, inc_id, API_user)

        if event['detail']['incident']['priority']['summary'] == 'P2':
            runResponsePlay(P2_response_play, inc_id, API_user)

    return 1
