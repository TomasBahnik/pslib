import json
import sys
from pathlib import Path

from cpt.common import ELK_BASE_URL
from cpt.elk_events import post_elk_event


def post_elk_events(elk_events):
    for elk_event in elk_events:
        post_elk_event(elk_event)


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
