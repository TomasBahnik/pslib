import json
import sys
from pathlib import Path

import requests

from cpt.common import ELK_BASE_URL, error_print


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


def post_elk_events(elk_events):
    cnt = 0
    length = len(elk_events)
    for elk_event in elk_events:
        post_elk_event(elk_event)
        if cnt % 100 != 0:
            print('.', end='')
        else:
            print(f'{cnt}/{length}')
        cnt += 1


def elk_events_from_file(event_file: Path):
    with open(event_file) as f:
        elk_events = json.loads(f.read())
    print(f"elk base URL = {ELK_BASE_URL}")
    print(f"elk events size = {len(elk_events)}")
    post_elk_events(elk_events)


if __name__ == '__main__':
    file = Path(sys.argv[1])
    if file.exists():
        print(f"events from {file}")
        elk_events_from_file(file)
