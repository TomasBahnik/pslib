import requests

from cpt.common import ELK_BASE_URL, error_print


class ELKEvent:
    def __init__(self, event_type: str, event: dict, timestamp):
        self.eventType = event_type
        self.event = event
        self.timestamp = timestamp
        self.eventBuildInfo = None
        self.eventSourceHost = None


def post_elk_event(elk_event):
    event_type = elk_event['eventType']
    event_detail = None
    # fe events do not have testMethod
    try:
        event_detail = elk_event['event']['testMethod']
    except KeyError as e:
        error_print(e)
    try:
        event_detail = elk_event['event']['scriptName']
    except KeyError as e:
        error_print(e)
    elk_url = ELK_BASE_URL + event_type
    event_timestamp = elk_event['timestamp']
    r = requests.post(elk_url, verify=False, json=elk_event, timeout=10)  # in seconds
    if r.status_code != 200:
        print(f"POST event: {r.status_code},{event_type},{event_timestamp},{event_detail}")
