# com.ataccama.one.performance.service.ELKService.ELKEvent
import requests

from cpt.common import ELK_BASE_URL


class ELKEvent:
    def __init__(self, eventType, event, timestamp):
        self.eventType = eventType
        self.event = event
        self.timestamp = timestamp
        self.eventBuildInfo = {}
        self.eventSourceHost = None


def post_elk_event(elk_event):
    event_type = elk_event['eventType']
    event_detail = None
    # fe events do not have testMethod
    try:
        event_detail = elk_event['event']['testMethod']
    except KeyError as e:
        print("post_elk_event assigning 'event_detail' : KeyError {}".format(e))
    try:
        event_detail = elk_event['event']['scriptName']
    except KeyError as e:
        print("post_elk_event assigning 'event_detail' : KeyError {}".format(e))
    elk_url = ELK_BASE_URL + event_type
    event_timestamp = elk_event['timestamp']
    r = requests.post(elk_url, verify=False, json=elk_event, timeout=10)  # in seconds
    print("POST event : type {}, detail : {}, timestamp {}, status code {}".
          format(event_type, event_detail, event_timestamp, r.status_code))